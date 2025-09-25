#!/bin/bash
# MEM_AGENT VM Bootstrap Script
# Installs Docker, Python SDKs, and launches containers on GCP VM

set -e

echo "🚀 MEM_AGENT System Bootstrap Starting..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get install -y curl wget git

# Install Docker
echo "🐳 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
echo "🔧 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

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
mkdir -p /opt/mem-agent
cd /opt/mem-agent

# Copy application files (assuming they're uploaded to the VM)
echo "📋 Copying application files..."
# Note: In production, files would be copied from a repository or uploaded

# Set up environment variables
echo "🔧 Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.template .env
    echo "⚠️  Please configure .env file with your secrets"
fi

# Start Docker services
echo "🚀 Starting Docker services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to initialize..."
sleep 30

# Check service health
echo "🔍 Checking service health..."
docker-compose ps

# Display access information
echo "✅ MEM_AGENT System Bootstrap Complete!"
echo ""
echo "🌐 Service Access URLs:"
echo "   n8n Workflow Automation: http://$(curl -s ifconfig.me):5678"
echo "   Mautic Marketing Automation: http://$(curl -s ifconfig.me):8888"
echo "   MEM_AGENT API: http://$(curl -s ifconfig.me):8000"
echo ""
echo "🔐 Default Credentials:"
echo "   n8n: Check .env file for N8N_BASIC_AUTH_USER and N8N_BASIC_AUTH_PASSWORD"
echo "   Mautic: Check .env file for MAUTIC_DB_USER and MAUTIC_DB_PASSWORD"
echo ""
echo "📋 Next Steps:"
echo "   1. Configure .env file with your secrets"
echo "   2. Access n8n to set up workflows"
echo "   3. Access Mautic to configure marketing automation"
echo "   4. Deploy Streamlit dashboard to Streamlit Cloud"
echo ""
echo "🎯 MEM_AGENT System is ready for deployment!"
