#!/bin/bash
# Deploy MEM_AGENT to GCP VM
# Target: 34.28.159.240 (browser-use-server)
# User: pixxelcartel

set -e

VM_IP="34.28.159.240"
VM_USER="pixxelcartel"
VM_HOSTNAME="browser-use-server"
APP_DIR="/opt/mem-agent"

echo "🚀 Deploying MEM_AGENT to GCP VM..."
echo "📍 Target: $VM_HOSTNAME ($VM_IP)"
echo "👤 User: $VM_USER"
echo ""

# Check if we can connect to VM
echo "🔍 Testing VM connectivity..."
if ! ssh -o ConnectTimeout=10 -o BatchMode=yes $VM_USER@$VM_IP exit 2>/dev/null; then
    echo "❌ Cannot connect to VM. Please check:"
    echo "   - VM is running"
    echo "   - SSH key is configured"
    echo "   - Firewall allows SSH (port 22)"
    exit 1
fi
echo "✅ VM connectivity confirmed"

# Create deployment package
echo "📦 Creating deployment package..."
tar -czf mem-agent-deploy.tar.gz \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.env' \
    --exclude='logs' \
    --exclude='data' \
    --exclude='temp' \
    .

# Upload to VM
echo "📤 Uploading to VM..."
scp mem-agent-deploy.tar.gz $VM_USER@$VM_IP:/tmp/

# Deploy on VM
echo "🚀 Deploying on VM..."
ssh $VM_USER@$VM_IP << 'EOF'
    set -e
    
    echo "📁 Setting up application directory..."
    sudo mkdir -p /opt/mem-agent
    sudo chown $USER:$USER /opt/mem-agent
    cd /opt/mem-agent
    
    echo "📦 Extracting application files..."
    tar -xzf /tmp/mem-agent-deploy.tar.gz
    rm /tmp/mem-agent-deploy.tar.gz
    
    echo "🔧 Setting up environment..."
    if [ ! -f .env ]; then
        cp env.production.template .env
        echo "⚠️  Please configure .env file with production secrets"
    fi
    
    echo "📁 Creating directories..."
    mkdir -p logs data temp
    
    echo "🐳 Starting Docker services..."
    docker-compose up -d --build
    
    echo "⏳ Waiting for services to initialize..."
    sleep 30
    
    echo "🔍 Checking service health..."
    docker-compose ps
    
    echo "✅ Deployment complete!"
EOF

# Clean up
rm mem-agent-deploy.tar.gz

echo ""
echo "✅ MEM_AGENT deployed successfully!"
echo ""
echo "🌐 Access URLs:"
echo "   API: https://pixelcartelhq.com/api/"
echo "   n8n: https://pixelcartelhq.com/n8n/"
echo "   Mautic: https://m.pixelcartelhq.com"
echo ""
echo "🔧 Management commands:"
echo "   SSH to VM: ssh $VM_USER@$VM_IP"
echo "   View logs: ssh $VM_USER@$VM_IP 'cd $APP_DIR && docker-compose logs -f'"
echo "   Restart: ssh $VM_USER@$VM_IP 'cd $APP_DIR && docker-compose restart'"
echo ""
echo "📋 Next steps:"
echo "   1. Configure .env file on VM with production secrets"
echo "   2. Set up SSL certificates (if not already done)"
echo "   3. Access services and complete setup"
