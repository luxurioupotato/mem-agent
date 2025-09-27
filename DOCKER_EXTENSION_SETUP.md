# 🐳 DOCKER EXTENSION SETUP FOR MEM_AGENT
## Complete Docker Integration and Management

### 📊 **DOCKER EXTENSION STATUS**
**Current Status**: Docker Desktop not installed/running  
**Extension Available**: Docker configuration files ready  
**Alternative**: Direct Docker Compose execution  

---

## 🔧 **DOCKER EXTENSION CONFIGURATION**

### **📋 DOCKER DESKTOP INSTALLATION**

#### **Step 1: Install Docker Desktop**
1. **Download Docker Desktop**
   - Go to: https://www.docker.com/products/docker-desktop/
   - Download Docker Desktop for Windows
   - Run installer as Administrator

2. **Enable WSL2 Backend**
   - During installation, select "Use WSL 2 instead of Hyper-V"
   - Enable WSL2 integration
   - Restart computer if required

3. **Verify Installation**
   ```bash
   docker --version
   docker compose version
   ```

#### **Step 2: Start Docker Desktop**
- Launch Docker Desktop from Start Menu
- Wait for Docker to start (whale icon in system tray)
- Ensure "Docker Desktop is running" status

### **📋 DOCKER EXTENSION USAGE**

#### **Method 1: Docker Desktop GUI**
1. **Open Docker Desktop**
2. **Navigate to Containers**
3. **Import docker-compose.yml**
4. **Start Services**

#### **Method 2: Command Line**
```bash
# Navigate to project directory
cd E:\MEM_AGENT

# Start all services
docker compose up -d

# Check service status
docker compose ps

# View logs
docker compose logs -f
```

#### **Method 3: Individual Services**
```bash
# Build API service
docker build -t mem-agent-api .

# Run specific service
docker run -d --name mem-agent-api -p 8000:8000 mem-agent-api
```

---

## 🚀 **MEM_AGENT DOCKER SERVICES**

### **📁 SERVICE CONFIGURATION**

#### **1. MEM_AGENT API Service**
```yaml
mem-agent-api:
  build: .
  container_name: mem-agent-api
  ports:
    - "8000:8000"
  environment:
    - GCP_PROJECT_ID=${GCP_PROJECT_ID}
    - SUPABASE_URL=${SUPABASE_URL}
    - SUPABASE_KEY=${SUPABASE_KEY}
  depends_on:
    - redis
    - postgres
```

#### **2. n8n Workflow Automation**
```yaml
n8n:
  image: n8nio/n8n:latest
  container_name: mem-agent-n8n
  ports:
    - "5678:5678"
  environment:
    - N8N_BASIC_AUTH_ACTIVE=true
    - N8N_BASIC_AUTH_USER=${N8N_BASIC_AUTH_USER}
    - N8N_BASIC_AUTH_PASSWORD=${N8N_BASIC_AUTH_PASSWORD}
  depends_on:
    - postgres
```

#### **3. Mautic Marketing Automation**
```yaml
mautic:
  image: mautic/mautic:5-apache
  container_name: mem-agent-mautic
  ports:
    - "8888:80"
  depends_on:
    - mautic-db
```

#### **4. Database Services**
```yaml
postgres:
  image: postgres:15
  container_name: mem-agent-postgres
  environment:
    - POSTGRES_USER=n8n
    - POSTGRES_PASSWORD=${N8N_DB_PASSWORD}
    - POSTGRES_DB=n8n

mautic-db:
  image: mariadb:10
  container_name: mem-agent-mautic-db
  environment:
    - MYSQL_ROOT_PASSWORD=${MAUTIC_DB_PASSWORD}
    - MYSQL_DATABASE=${MAUTIC_DB_NAME}
    - MYSQL_USER=${MAUTIC_DB_USER}
    - MYSQL_PASSWORD=${MAUTIC_DB_PASSWORD}

redis:
  image: redis:7-alpine
  container_name: mem-agent-redis
  ports:
    - "6379:6379"
```

---

## 🔧 **DOCKER EXTENSION COMMANDS**

### **📋 ESSENTIAL COMMANDS**

#### **Service Management**
```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# Restart specific service
docker compose restart mem-agent-api

# View service logs
docker compose logs -f mem-agent-api
```

#### **Service Health Checks**
```bash
# Check service status
docker compose ps

# Check service health
docker inspect mem-agent-api | grep -i health

# Test API endpoint
curl http://localhost:8000/health
```

#### **Service Scaling**
```bash
# Scale specific service
docker compose up -d --scale mem-agent-api=2

# Update service configuration
docker compose up -d --force-recreate
```

---

## 🎯 **DOCKER EXTENSION WORKFLOW**

### **📋 COMPLETE SETUP PROCESS**

#### **Step 1: Environment Setup**
```bash
# Copy environment template
cp env.template .env

# Edit environment variables
notepad .env
```

#### **Step 2: Build and Deploy**
```bash
# Build all services
docker compose build

# Start all services
docker compose up -d

# Verify deployment
docker compose ps
```

#### **Step 3: Service Access**
- **API**: http://localhost:8000
- **n8n**: http://localhost:5678
- **Mautic**: http://localhost:8888
- **Redis**: localhost:6379

#### **Step 4: Monitoring**
```bash
# View all logs
docker compose logs -f

# View specific service logs
docker compose logs -f mem-agent-api

# Check resource usage
docker stats
```

---

## 🚀 **DOCKER EXTENSION BENEFITS**

### **✅ ADVANTAGES:**
- **Visual Management**: Docker Desktop GUI
- **Service Orchestration**: Multi-container management
- **Health Monitoring**: Built-in health checks
- **Volume Management**: Persistent data storage
- **Network Management**: Inter-service communication
- **Log Aggregation**: Centralized logging

### **📋 FEATURES:**
- **Container Management**: Start/stop/restart services
- **Resource Monitoring**: CPU, memory, network usage
- **Log Viewing**: Real-time log streaming
- **Volume Management**: Data persistence
- **Network Configuration**: Service communication
- **Health Checks**: Service status monitoring

---

## 🎯 **NEXT STEPS**

### **📋 IMMEDIATE ACTIONS:**
1. **Install Docker Desktop** (if not already installed)
2. **Start Docker Desktop** and wait for it to be ready
3. **Run deployment**: `docker compose up -d`
4. **Access services** via provided URLs
5. **Monitor services** using Docker Desktop GUI

### **📋 RESULT:**
**Complete Docker extension setup with full service orchestration, monitoring, and management capabilities!**

**🚀 DOCKER EXTENSION READY: All services configured for Docker Desktop management with visual interface and command-line control!**

