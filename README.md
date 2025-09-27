<<<<<<< HEAD
# 🚀 MEM_AGENT - AI Business Intelligence Platform

## Overview
MEM_AGENT is a comprehensive AI business intelligence platform that combines advanced AI capabilities with automated workflows, marketing automation, and strategic business analysis.

## Features
- **AI Mentor Agent**: Gemini 1.5 Pro powered business mentor
- **Workflow Automation**: n8n integration for process automation
- **Marketing Automation**: Mautic integration for lead generation
- **Business Intelligence**: Strategic analysis and revenue optimization
- **Cloud Integration**: Google Cloud Platform with Secret Manager
- **Database Integration**: Supabase for persistent storage

## Quick Start

### Prerequisites
- Google Cloud Platform account
- GCP Project ID: `hardy-canyon-470416-q9`
- Service Account: `ise-agent-sa@hardy-canyon-470416-q9.iam.gserviceaccount.com`
- Supabase account
- Docker and Docker Compose

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/mem-agent.git
   cd mem-agent
   ```

2. **Configure secrets in Google Secret Manager**
   - `GCP_SA_KEY`: Service account JSON key
   - `SUPABASE_URL`: Supabase project URL
   - `SUPABASE_KEY`: Supabase service role key
   - `N8N_BASIC_AUTH_USER`: n8n admin username
   - `N8N_BASIC_AUTH_PASSWORD`: n8n admin password
   - `N8N_DB_PASSWORD`: PostgreSQL password
   - `MAUTIC_DB_USER`: Mautic database user
   - `MAUTIC_DB_PASSWORD`: Mautic database password

3. **Deploy to GCP VM**
   ```bash
   chmod +x scripts/one-click-deploy.sh
   ./scripts/one-click-deploy.sh <your-vm-ip>
   ```

4. **Access services**
   - API: `http://your-vm-ip:8000`
   - n8n: `http://your-vm-ip:5678`
   - Mautic: `http://your-vm-ip:8888`

## Architecture

### Core Components
- **Mentor Agent**: AI-powered business mentor with Gemini 1.5 Pro
- **Frontend**: Streamlit dashboard for user interaction
- **API**: FastAPI backend with GCP integration
- **Workflows**: n8n automation platform
- **Marketing**: Mautic marketing automation
- **Database**: Supabase for data persistence

### Technology Stack
- **AI**: Gemini 1.5 Pro, OpenAI, Anthropic
- **Backend**: Python, FastAPI, Streamlit
- **Database**: Supabase, PostgreSQL, Redis
- **Automation**: n8n, Docker Compose
- **Cloud**: Google Cloud Platform, Secret Manager
- **Marketing**: Mautic, MariaDB

## Usage

### Mentor Agent
The mentor agent provides strategic business intelligence and guidance:
- Business strategy analysis
- Revenue optimization recommendations
- Market intelligence insights
- Competitive analysis
- Lead generation strategies

### Workflow Automation
n8n workflows for automated processes:
- Competitive intelligence gathering
- Market signal detection
- Lead generation and scoring
- Business metrics analysis

### Marketing Automation
Mautic campaigns for lead nurturing:
- Welcome email sequences
- Lead scoring and qualification
- Automated follow-up campaigns
- Performance tracking

## Configuration

### Environment Variables
All secrets are managed through Google Secret Manager:
- `GCP_PROJECT_ID`: GCP project identifier
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_KEY`: Supabase service role key
- `API_BASE_URL`: Backend API URL

### Database Schema
Supabase tables for data persistence:
- `mentor_memory`: Conversation history
- `business_metrics`: Performance metrics
- `leads`: Lead generation data
- `workflow_executions`: Automation logs
- `system_health`: System monitoring

## Deployment

### Automated Deployment
Use the one-click deployment script:
```bash
./scripts/one-click-deploy.sh <vm-ip-address>
```

### Manual Deployment
1. Upload files to GCP VM
2. Run `./startup.sh`
3. Configure secrets in Secret Manager
4. Start services with `docker-compose up -d`

## Monitoring

### Health Checks
- API health endpoint: `/health`
- Service status monitoring
- Performance metrics tracking
- Error detection and alerting

### Logs
- Application logs in `/app/logs`
- Docker container logs
- System health monitoring
- Performance analytics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Contact the development team

## Roadmap

- [ ] Advanced AI model integration
- [ ] Enhanced workflow automation
- [ ] Improved marketing automation
- [ ] Advanced analytics dashboard
- [ ] Mobile application
- [ ] API documentation
- [ ] Performance optimization

---

**🚀 MEM_AGENT - Your AI Business Intelligence Platform**
=======
# mem-agent
>>>>>>> 28d80c099877d7f3bae639dc216089a7c7fdfe32
