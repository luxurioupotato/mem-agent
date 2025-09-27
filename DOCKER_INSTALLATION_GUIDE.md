# 🐳 MEM_AGENT DOCKER INSTALLATION GUIDE
## Complete Docker Setup for Windows

### 📊 **DOCKER STATUS**
**Current Status**: Docker not installed on Windows system  
**Required**: Docker Desktop for Windows with WSL2 backend  
**Alternative**: Direct deployment to GCP VM (recommended)  

---

## 🔧 **DOCKER INSTALLATION OPTIONS**

### **📋 OPTION 1: DOCKER DESKTOP (RECOMMENDED)**

#### **Prerequisites:**
- Windows 10/11 with WSL2 support
- Administrator privileges
- 4GB+ RAM available

#### **Installation Steps:**
1. **Download Docker Desktop**
   - Go to: https://www.docker.com/products/docker-desktop/
   - Download Docker Desktop for Windows
   - Run installer as Administrator

2. **Enable WSL2 Backend**
   - During installation, select "Use WSL 2 instead of Hyper-V"
   - Enable WSL2 integration

3. **Verify Installation**
   ```bash
   docker --version
   docker compose version
   ```

### **📋 OPTION 2: WSL2 + DOCKER ENGINE**

#### **Enable WSL2:**
```powershell
# Run as Administrator
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
wsl --install
```

#### **Install Docker in WSL2:**
```bash
# In WSL2 terminal
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

---

## 🚀 **ALTERNATIVE: GCP VM DEPLOYMENT (RECOMMENDED)**

### **📋 DIRECT VM DEPLOYMENT (NO LOCAL DOCKER NEEDED)**

#### **Advantages:**
- ✅ No local Docker installation required
- ✅ Production-ready environment
- ✅ Automatic setup via `startup.sh`
- ✅ All services pre-configured

#### **Deployment Steps:**
1. **Upload to GCP VM**
   ```bash
   scp -r . <vm-user>@<vm-ip>:/opt/mem-agent/
   ```

2. **SSH to VM and Deploy**
   ```bash
   ssh <vm-user>@<vm-ip>
   cd /opt/mem-agent
   chmod +x startup.sh
   ./startup.sh
   ```

3. **Access Services**
   - API: `http://<vm-ip>:8000`
   - n8n: `http://<vm-ip>:5678`
   - Mautic: `http://<vm-ip>:8888`

---

## 🔧 **DOCKER CONFIGURATION FILES READY**

### **📁 COMPLETE DOCKER SETUP:**

#### **1. Dockerfile**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### **2. docker-compose.yml**
```yaml
version: '3.9'
services:
  n8n:
    image: n8nio/n8n:latest
    ports: ["5678:5678"]
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_BASIC_AUTH_USER}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_BASIC_AUTH_PASSWORD}
    depends_on: [postgres]
  
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=${N8N_DB_PASSWORD}
      - POSTGRES_DB=n8n
  
  mautic:
    image: mautic/mautic:5-apache
    ports: ["8888:80"]
    depends_on: [mautic-db]
  
  mautic-db:
    image: mariadb:10
    environment:
      - MYSQL_ROOT_PASSWORD=${MAUTIC_DB_PASSWORD}
      - MYSQL_DATABASE=${MAUTIC_DB_NAME}
      - MYSQL_USER=${MAUTIC_DB_USER}
      - MYSQL_PASSWORD=${MAUTIC_DB_PASSWORD}
  
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
  
  mem-agent-api:
    build: .
    ports: ["8000:8000"]
    environment:
      - GCP_PROJECT_ID=${GCP_PROJECT_ID}
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
    depends_on: [redis, postgres]
```

#### **3. startup.sh (VM Bootstrap)**
```bash
#!/bin/bash
# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Start services
docker-compose up -d
```

---

## 🎯 **RECOMMENDED APPROACH**

### **📋 FOR IMMEDIATE DEPLOYMENT:**

#### **Option A: GCP VM (Recommended)**
- ✅ No local Docker installation needed
- ✅ Production environment
- ✅ Automatic setup
- ✅ All services configured

#### **Option B: Local Docker**
- ⚠️ Requires Docker Desktop installation
- ⚠️ Windows WSL2 setup required
- ⚠️ Local development only

### **📋 NEXT STEPS:**

1. **Choose Deployment Method:**
   - **GCP VM**: Use `startup.sh` script
   - **Local Docker**: Install Docker Desktop first

2. **Configure Environment:**
   - Copy `env.template` to `.env`
   - Set up secrets in Google Secret Manager

3. **Deploy Services:**
   - **VM**: `./startup.sh`
   - **Local**: `docker compose up -d`

---

## 🚀 **DEPLOYMENT READY**

### **✅ DOCKER AUTOMATION COMPLETE:**
- ✅ **Dockerfile**: Application containerization ready
- ✅ **docker-compose.yml**: Multi-service orchestration ready
- ✅ **startup.sh**: VM bootstrap automation ready
- ✅ **Environment**: Configuration templates ready
- ✅ **Documentation**: Complete setup guide ready

### **🎯 RESULT:**
**Complete Docker setup with multiple deployment options - choose GCP VM for production or install Docker Desktop for local development!**

