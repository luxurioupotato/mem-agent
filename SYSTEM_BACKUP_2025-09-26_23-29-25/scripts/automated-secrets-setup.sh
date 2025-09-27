#!/bin/bash
# MEM_AGENT Automated Secrets Setup
# Configures all secrets in Google Secret Manager automatically

set -e

echo "🔐 MEM_AGENT AUTOMATED SECRETS SETUP..."

# Configuration
PROJECT_ID="hardy-canyon-470416-q9"
SERVICE_ACCOUNT="ise-agent-sa@hardy-canyon-470416-q9.iam.gserviceaccount.com"

# Function to create secret
create_secret() {
    local secret_name=$1
    local secret_value=$2
    
    echo "Creating secret: $secret_name"
    gcloud secrets create $secret_name --data-file=- <<< "$secret_value" || echo "Secret $secret_name already exists"
}

# Create all required secrets
echo "📋 Creating secrets in Google Secret Manager..."

# GCP Service Account Key (placeholder - user must provide actual key)
create_secret "GCP_SA_KEY" "PLACEHOLDER_SERVICE_ACCOUNT_KEY"

# Supabase Configuration (placeholder - user must provide actual values)
create_secret "SUPABASE_URL" "PLACEHOLDER_SUPABASE_URL"
create_secret "SUPABASE_KEY" "PLACEHOLDER_SUPABASE_KEY"

# n8n Configuration
create_secret "N8N_BASIC_AUTH_USER" "admin"
create_secret "N8N_BASIC_AUTH_PASSWORD" "$(openssl rand -base64 32)"
create_secret "N8N_DB_PASSWORD" "$(openssl rand -base64 32)"

# Mautic Configuration
create_secret "MAUTIC_DB_USER" "mautic"
create_secret "MAUTIC_DB_PASSWORD" "$(openssl rand -base64 32)"

echo "✅ SECRETS SETUP COMPLETE!"
echo ""
echo "📋 MANUAL ACTIONS REQUIRED:"
echo "   1. Update GCP_SA_KEY with actual service account JSON"
echo "   2. Update SUPABASE_URL with actual Supabase URL"
echo "   3. Update SUPABASE_KEY with actual Supabase key"
echo ""
echo "🔐 All other secrets generated automatically!"
