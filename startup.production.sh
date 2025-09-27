#!/bin/bash
# MEM_AGENT Production VM Bootstrap Script
# For GCP VM: 34.28.159.240 (browser-use-server)
# User: pixxelcartel

set -e

echo "🚀 MEM_AGENT Production System Bootstrap Starting..."
echo "📍 Target VM: browser-use-server (34.28.159.240)"
echo "👤 User: pixxelcartel"
echo ""

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get install -y curl wget git nginx certbot python3-certbot-nginx

# Install Docker
echo "🐳 Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
fi

# Install Docker Compose
echo "🔧 Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
sudo apt-get install -y python3-pip python3-venv
pip3 install --upgrade pip

# Install required Python packages
pip3 install --upgrade \
    google-cloud-secret-manager \
    google-genai \
    supabase \
    streamlit \
    requests \
    pandas \
    numpy

# Create application directory
echo "📁 Setting up application directory..."
sudo mkdir -p /opt/mem-agent
sudo chown $USER:$USER /opt/mem-agent
cd /opt/mem-agent

# Copy application files (assuming they're uploaded to the VM)
echo "📋 Copying application files..."
# Note: Files should be uploaded via scp or git clone

# Set up environment variables
echo "🔧 Setting up environment variables..."
if [ ! -f .env ]; then
    cp env.production.template .env
    echo "⚠️  Please configure .env file with your production secrets"
    echo "   Edit: nano .env"
    echo "   Required: Update all CHANGE_ME_* values"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs data temp

# Set up Nginx reverse proxy
echo "🌐 Setting up Nginx reverse proxy..."
sudo tee /etc/nginx/sites-available/mem-agent > /dev/null <<EOF
server {
    listen 80;
    server_name pixelcartelhq.com www.pixelcartelhq.com m.pixelcartelhq.com;

    # API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # n8n
    location /n8n/ {
        proxy_pass http://localhost:5678/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Mautic
    location / {
        proxy_pass http://localhost:8888/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/mem-agent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Start Docker services
echo "🚀 Starting Docker services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to initialize..."
sleep 30

# Check service health
echo "🔍 Checking service health..."
docker-compose ps

# Set up SSL certificates
echo "🔒 Setting up SSL certificates..."
sudo certbot --nginx -d pixelcartelhq.com -d www.pixelcartelhq.com -d m.pixelcartelhq.com --non-interactive --agree-tos --email admin@pixelcartelhq.com

# Display access information
echo "✅ MEM_AGENT Production System Bootstrap Complete!"
echo ""
echo "🌐 Service Access URLs:"
echo "   API: https://pixelcartelhq.com/api/"
echo "   n8n: https://pixelcartelhq.com/n8n/"
echo "   Mautic: https://m.pixelcartelhq.com"
echo ""
echo "🔐 Configuration:"
echo "   Edit .env file: nano /opt/mem-agent/.env"
echo "   View logs: docker-compose logs -f"
echo "   Restart services: docker-compose restart"
echo ""
echo "📋 Next Steps:"
echo "   1. Configure .env file with production secrets"
echo "   2. Access n8n to set up workflows"
echo "   3. Access Mautic to configure marketing automation"
echo "   4. Deploy Streamlit dashboard to Streamlit Cloud"
echo ""
echo "🎯 MEM_AGENT Production System is ready for deployment!"
