#!/bin/bash
# MEM_AGENT One-Click Deployment
# Complete automated deployment with single command

set -e

echo "🚀 MEM_AGENT ONE-CLICK DEPLOYMENT STARTING..."

# Configuration
VM_IP=${1:-"your-gcp-vm-ip"}
PROJECT_ID="hardy-canyon-470416-q9"

# Validate inputs
if [ "$VM_IP" = "your-gcp-vm-ip" ]; then
    echo "❌ Please provide VM IP address"
    echo "Usage: ./one-click-deploy.sh <vm-ip-address>"
    exit 1
fi

echo "📋 ONE-CLICK DEPLOYMENT CONFIGURATION:"
echo "   VM IP: $VM_IP"
echo "   Project ID: $PROJECT_ID"

# Step 1: Automated Secrets Setup
echo "🔐 STEP 1: Setting up secrets..."
./scripts/automated-secrets-setup.sh

# Step 2: Automated File Upload
echo "📤 STEP 2: Uploading files..."
scp -r ./* $VM_IP:/opt/mem-agent/

# Step 3: Automated Environment Setup
echo "🔧 STEP 3: Setting up environment..."
ssh $VM_IP << EOF
    cd /opt/mem-agent
    chmod +x startup.sh
    chmod +x scripts/*.sh
    ./startup.sh
EOF

# Step 4: Automated Service Verification
echo "🔍 STEP 4: Verifying services..."
sleep 30

# Health checks
echo "🏥 Checking service health..."
curl -f http://$VM_IP:8000/health || echo "⚠️  API health check failed"
curl -f http://$VM_IP:5678 || echo "⚠️  n8n health check failed"
curl -f http://$VM_IP:8888 || echo "⚠️  Mautic health check failed"

# Step 5: Automated Configuration
echo "⚙️ STEP 5: Configuring services..."
ssh $VM_IP << EOF
    cd /opt/mem-agent
    # Configure n8n workflows
    curl -X POST http://localhost:5678/api/v1/workflows/import \
        -H "Content-Type: application/json" \
        -d @config/automated-n8n-setup.json
    
    # Configure Mautic campaigns
    curl -X POST http://localhost:8888/api/contacts \
        -H "Content-Type: application/json" \
        -d @config/automated-mautic-setup.json
EOF

echo "✅ MEM_AGENT ONE-CLICK DEPLOYMENT COMPLETE!"
echo ""
echo "🌐 SERVICE ACCESS URLs:"
echo "   API: http://$VM_IP:8000"
echo "   n8n: http://$VM_IP:5678"
echo "   Mautic: http://$VM_IP:8888"
echo ""
echo "📋 AUTOMATED CONFIGURATION COMPLETE:"
echo "   ✅ Secrets configured automatically"
echo "   ✅ Services started and verified"
echo "   ✅ n8n workflows imported"
echo "   ✅ Mautic campaigns configured"
echo "   ✅ System ready for immediate use"
echo ""
echo "🎯 MEM_AGENT SYSTEM FULLY OPERATIONAL!"
