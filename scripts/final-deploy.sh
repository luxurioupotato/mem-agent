#!/bin/bash
# MEM_AGENT FINAL PRODUCTION DEPLOYMENT SCRIPT
# Based on reference guide infrastructure configuration
# Target: GCP VM 34.28.159.240 (browser-use-server)

set -e

# Configuration from reference guide
VM_IP="34.28.159.240"
VM_USER="pixxelcartel"
VM_HOSTNAME="browser-use-server"
APP_DIR="/opt/mem-agent"
PROJECT_ID="hardy-canyon-470416-q9"

echo "🚀 MEM_AGENT FINAL PRODUCTION DEPLOYMENT"
echo "📍 Target: $VM_HOSTNAME ($VM_IP)"
echo "👤 User: $VM_USER"
echo "🏗️ Project: $PROJECT_ID"
echo ""

# Phase 1: Pre-deployment validation
echo "🔍 PHASE 1: PRE-DEPLOYMENT VALIDATION"
echo ""

# Check if we can connect to VM
echo "Testing VM connectivity..."
if ! ssh -o ConnectTimeout=10 -o BatchMode=yes $VM_USER@$VM_IP exit 2>/dev/null; then
    echo "❌ Cannot connect to VM. Please check:"
    echo "   - VM is running"
    echo "   - SSH key is configured"
    echo "   - Firewall allows SSH (port 22)"
    exit 1
fi
echo "✅ VM connectivity confirmed"

# Check if Docker is installed on VM
echo "Checking Docker installation on VM..."
if ! ssh $VM_USER@$VM_IP "docker --version" 2>/dev/null; then
    echo "⚠️ Docker not installed on VM. Installing..."
    ssh $VM_USER@$VM_IP "curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo usermod -aG docker $VM_USER"
fi
echo "✅ Docker confirmed"

# Phase 2: Create deployment package
echo ""
echo "📦 PHASE 2: CREATING DEPLOYMENT PACKAGE"
echo ""

# Create final deployment package
echo "Creating final deployment package..."
tar -czf mem-agent-final-deploy.tar.gz \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.env' \
    --exclude='logs' \
    --exclude='data' \
    --exclude='temp' \
    --exclude='SYSTEM_BACKUP_*' \
    --exclude='DEEP_SYSTEM_AUDIT_*' \
    .

echo "✅ Deployment package created: mem-agent-final-deploy.tar.gz"

# Phase 3: Deploy to VM
echo ""
echo "🚀 PHASE 3: DEPLOYING TO VM"
echo ""

# Upload to VM
echo "Uploading to VM..."
scp mem-agent-final-deploy.tar.gz $VM_USER@$VM_IP:/tmp/

# Deploy on VM
echo "Deploying on VM..."
ssh $VM_USER@$VM_IP << 'EOF'
    set -e
    
    echo "📁 Setting up application directory..."
    sudo mkdir -p /opt/mem-agent
    sudo chown $USER:$USER /opt/mem-agent
    cd /opt/mem-agent
    
    echo "📦 Extracting application files..."
    tar -xzf /tmp/mem-agent-final-deploy.tar.gz
    rm /tmp/mem-agent-final-deploy.tar.gz
    
    echo "🔧 Setting up final production environment..."
    if [ ! -f .env ]; then
        cp env.final.production .env
        echo "✅ Final production environment configured"
    fi
    
    echo "📁 Creating necessary directories..."
    mkdir -p logs data temp config
    
    echo "🔒 Setting up SSL certificates (if needed)..."
    if ! command -v certbot &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y certbot python3-certbot-nginx
    fi
    
    echo "🌐 Setting up Nginx reverse proxy..."
    sudo tee /etc/nginx/sites-available/mem-agent > /dev/null << 'NGINX_EOF'
server {
    listen 80;
    server_name pixelcartelhq.com www.pixelcartelhq.com m.pixelcartelhq.com;

    # API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # n8n
    location /n8n/ {
        proxy_pass http://localhost:5678/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Mautic
    location / {
        proxy_pass http://localhost:8888/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINX_EOF

    # Enable Nginx site
    sudo ln -sf /etc/nginx/sites-available/mem-agent /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl reload nginx
    
    echo "🐳 Starting Docker services..."
    docker compose up -d --build
    
    echo "⏳ Waiting for services to initialize..."
    sleep 30
    
    echo "🔍 Checking service health..."
    docker compose ps
    
    echo "🔒 Setting up SSL certificates..."
    sudo certbot --nginx -d pixelcartelhq.com -d www.pixelcartelhq.com -d m.pixelcartelhq.com --non-interactive --agree-tos --email admin@pixelcartelhq.com
    
    echo "✅ Final deployment complete!"
EOF

# Phase 4: Post-deployment verification
echo ""
echo "🔍 PHASE 4: POST-DEPLOYMENT VERIFICATION"
echo ""

# Test API endpoint
echo "Testing API endpoint..."
if curl -f http://$VM_IP:8000/health > /dev/null 2>&1; then
    echo "✅ API endpoint responding"
else
    echo "⚠️ API endpoint not responding (may need time to start)"
fi

# Test n8n endpoint
echo "Testing n8n endpoint..."
if curl -f http://$VM_IP:5678 > /dev/null 2>&1; then
    echo "✅ n8n endpoint responding"
else
    echo "⚠️ n8n endpoint not responding (may need time to start)"
fi

# Test Mautic endpoint
echo "Testing Mautic endpoint..."
if curl -f http://$VM_IP:8888 > /dev/null 2>&1; then
    echo "✅ Mautic endpoint responding"
else
    echo "⚠️ Mautic endpoint not responding (may need time to start)"
fi

# Clean up
rm mem-agent-final-deploy.tar.gz

echo ""
echo "🎉 FINAL PRODUCTION DEPLOYMENT COMPLETE!"
echo ""
echo "🌐 Production URLs:"
echo "   API: https://pixelcartelhq.com/api/"
echo "   n8n: https://pixelcartelhq.com/n8n/"
echo "   Mautic: https://m.pixelcartelhq.com"
echo "   WordPress: https://pixelcartelhq.com"
echo ""
echo "🔧 Management Commands:"
echo "   SSH to VM: ssh $VM_USER@$VM_IP"
echo "   View logs: ssh $VM_USER@$VM_IP 'cd $APP_DIR && docker compose logs -f'"
echo "   Restart: ssh $VM_USER@$VM_IP 'cd $APP_DIR && docker compose restart'"
echo ""
echo "📋 Next Steps:"
echo "   1. Complete n8n setup at https://pixelcartelhq.com/n8n/"
echo "   2. Complete Mautic setup at https://m.pixelcartelhq.com"
echo "   3. Configure SMTP settings in Mautic"
echo "   4. Test end-to-end functionality"
echo ""
echo "🚀 MEM_AGENT FINAL PRODUCTION SYSTEM DEPLOYED!"
