# 🚀 MEM_AGENT Production Quickstart
## Complete Deployment Guide for GCP VM

### 📋 **CONFIRMED INFRASTRUCTURE**
- **GCP Project**: hardy-canyon-470416-q9
- **VM IP**: 34.28.159.240 (browser-use-server)
- **SSH User**: pixxelcartel
- **Domains**: pixelcartelhq.com, m.pixelcartelhq.com
- **SSL**: Let's Encrypt (Certbot)

---

## 🎯 **IMMEDIATE DEPLOYMENT**

### **Step 1: Deploy to VM**
```bash
# From your local machine
./scripts/deploy-to-vm.sh
```

### **Step 2: Configure Production Secrets**
```bash
# SSH to VM
ssh pixxelcartel@34.28.159.240

# Edit environment file
cd /opt/mem-agent
nano .env
```

**Required .env updates:**
- `MAUTIC_DB_PASSWORD` - Set secure password
- `N8N_BASIC_AUTH_PASSWORD` - Set admin password
- `POSTGRES_PASSWORD` - Set database password
- `REDIS_PASSWORD` - Set Redis password
- `SMTP_*` - Configure email settings
- `JWT_SECRET_KEY` - Generate secure key
- `ENCRYPTION_KEY` - Generate secure key
- `SESSION_SECRET` - Generate secure key

### **Step 3: Restart Services**
```bash
# On VM
cd /opt/mem-agent
docker-compose restart
```

---

## 🌐 **SERVICE ACCESS**

### **Production URLs:**
- **API**: https://pixelcartelhq.com/api/
- **n8n**: https://pixelcartelhq.com/n8n/
- **Mautic**: https://m.pixelcartelhq.com

### **Local Development:**
- **API**: http://localhost:8000
- **n8n**: http://localhost:5678
- **Mautic**: http://localhost:8888

---

## 🔧 **SERVICE CONFIGURATION**

### **n8n Setup:**
1. Open https://pixelcartelhq.com/n8n/
2. Create admin account
3. Import workflows from `config/automated-n8n-setup.json`

### **Mautic Setup:**
1. Open https://m.pixelcartelhq.com
2. Complete web installer:
   - **DB Host**: mautic-db
   - **DB Name**: mauticPixC
   - **DB User**: mPixC
   - **DB Password**: (from .env)
3. Configure SMTP settings
4. Import campaigns from `config/automated-mautic-setup.json`

### **API Configuration:**
- CORS configured for production domains
- Redis authentication enabled
- JWT security implemented
- Logging to `/app/logs/`

---

## 📊 **MONITORING & MANAGEMENT**

### **Health Checks:**
```bash
# Check all services
docker-compose ps

# View logs
docker-compose logs -f

# API health
curl https://pixelcartelhq.com/api/health
```

### **Service Management:**
```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart mem-agent-api

# View service logs
docker-compose logs -f mem-agent-api
```

---

## 🔒 **SECURITY CONFIGURATION**

### **SSL Certificates:**
- Automatically configured via Certbot
- Domains: pixelcartelhq.com, www.pixelcartelhq.com, m.pixelcartelhq.com
- Auto-renewal enabled

### **Firewall:**
- Port 80 (HTTP) - Redirects to HTTPS
- Port 443 (HTTPS) - Production access
- Port 22 (SSH) - Management access

### **Database Security:**
- All databases password protected
- Redis authentication enabled
- No external database access

---

## 📋 **ENVIRONMENT VARIABLES**

### **Production Template:**
```bash
# Copy and configure
cp env.production.template .env
nano .env
```

### **Key Variables:**
- `API_BASE_URL=https://pixelcartelhq.com`
- `MAUTIC_WEB_URL=https://m.pixelcartelhq.com`
- `ALLOWED_CORS_ORIGINS` - Production domains
- `SMTP_*` - Email configuration
- `*_PASSWORD` - All service passwords

---

## 🚀 **STREAMLIT CLOUD DEPLOYMENT**

### **Dashboard Configuration:**
1. Create new Streamlit Cloud app
2. Connect to your GitHub repository
3. Set main file: `dashboard/app.py`
4. Configure environment variables:
   - `API_BASE_URL=https://pixelcartelhq.com`
   - `SUPABASE_URL` (if using)
   - `SUPABASE_KEY` (if using)

---

## 🔧 **TROUBLESHOOTING**

### **Common Issues:**
1. **Services not starting**: Check .env configuration
2. **SSL errors**: Run `sudo certbot --nginx` on VM
3. **Database connection**: Verify credentials in .env
4. **CORS errors**: Check ALLOWED_CORS_ORIGINS

### **Logs Location:**
- **Application**: `/opt/mem-agent/logs/`
- **Docker**: `docker-compose logs -f`
- **Nginx**: `/var/log/nginx/`
- **System**: `journalctl -u nginx`

---

## ✅ **DEPLOYMENT CHECKLIST**

- [ ] VM accessible via SSH
- [ ] Application files uploaded
- [ ] .env configured with production secrets
- [ ] Docker services running
- [ ] SSL certificates installed
- [ ] n8n admin account created
- [ ] Mautic installer completed
- [ ] API health check passing
- [ ] All services accessible via HTTPS

---

## 🎯 **NEXT STEPS**

1. **Complete service setup** (n8n, Mautic)
2. **Configure workflows** and campaigns
3. **Deploy Streamlit dashboard**
4. **Set up monitoring** and alerts
5. **Test end-to-end functionality**

**🚀 MEM_AGENT Production System Ready!**
