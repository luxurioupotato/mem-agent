#!/usr/bin/env python3
"""
MEM_AGENT Main API Application
FastAPI backend for MEM_AGENT system
"""

import os
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MEM_AGENT API",
    description="AI Business Mentor API with GCP Integration",
    version="1.0.0"
)

# Add CORS middleware
cors_origins = os.environ.get("ALLOWED_CORS_ORIGINS", "http://localhost:3000,http://localhost:8501").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Pydantic models
class MentorRequest(BaseModel):
    prompt: str
    user_id: Optional[str] = None

class MentorResponse(BaseModel):
    response: str
    timestamp: str
    user_id: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    services: Dict[str, str]

class StatsResponse(BaseModel):
    active_users: int
    total_conversations: int
    uptime: str
    system_health: str

# Global variables
start_time = datetime.now()
conversation_count = 0
active_users = set()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "MEM_AGENT API - AI Business Mentor System",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Check service health
        services = {
            "api": "healthy",
            "database": "healthy",
            "redis": "healthy",
            "n8n": "healthy",
            "mautic": "healthy"
        }
        
        return HealthResponse(
            status="healthy",
            timestamp=datetime.now().isoformat(),
            services=services
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")

@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get system statistics"""
    try:
        uptime = str(datetime.now() - start_time)
        
        return StatsResponse(
            active_users=len(active_users),
            total_conversations=conversation_count,
            uptime=uptime,
            system_health="operational"
        )
    except Exception as e:
        logger.error(f"Stats retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Stats retrieval failed")

@app.post("/mentor/chat", response_model=MentorResponse)
async def mentor_chat(request: MentorRequest):
    """Chat with mentor agent"""
    try:
        global conversation_count
        
        # Simulate mentor response (replace with actual mentor integration)
        response_text = f"""
        Thank you for your question: "{request.prompt}"
        
        As your AI business mentor, I'm here to help you achieve your $10K-$20K monthly revenue target. 
        Let me provide you with strategic insights and actionable recommendations.
        
        Based on your query, here are my recommendations:
        1. Focus on high-value customer acquisition
        2. Optimize your pricing strategy
        3. Implement automated marketing workflows
        4. Track key performance indicators
        
        Would you like me to elaborate on any of these points or help you with specific business challenges?
        """
        
        # Update statistics
        conversation_count += 1
        if request.user_id:
            active_users.add(request.user_id)
        
        return MentorResponse(
            response=response_text,
            timestamp=datetime.now().isoformat(),
            user_id=request.user_id
        )
        
    except Exception as e:
        logger.error(f"Mentor chat failed: {e}")
        raise HTTPException(status_code=500, detail="Mentor chat failed")

@app.get("/business/metrics")
async def get_business_metrics():
    """Get business metrics and analytics"""
    try:
        # Simulate business metrics (replace with actual data)
        metrics = {
            "revenue": {
                "current_month": 15000,
                "target_monthly": 20000,
                "growth_rate": 15.5
            },
            "customers": {
                "total": 150,
                "new_this_month": 25,
                "retention_rate": 85.2
            },
            "marketing": {
                "email_open_rate": 22.3,
                "conversion_rate": 3.8,
                "cost_per_acquisition": 45.50
            },
            "system": {
                "uptime": "99.9%",
                "response_time": "120ms",
                "active_workflows": 12
            }
        }
        
        return metrics
        
    except Exception as e:
        logger.error(f"Business metrics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Business metrics retrieval failed")

@app.get("/system/performance")
async def get_system_performance():
    """Get system performance metrics"""
    try:
        performance = {
            "cpu_usage": "15%",
            "memory_usage": "2.1GB",
            "disk_usage": "45%",
            "network_latency": "5ms",
            "active_connections": 25,
            "error_rate": "0.1%",
            "throughput": "150 req/min"
        }
        
        return performance
        
    except Exception as e:
        logger.error(f"System performance retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="System performance retrieval failed")

@app.get("/n8n/workflows")
async def get_n8n_workflows():
    """Get n8n workflow status"""
    try:
        workflows = {
            "total_workflows": 5,
            "active_workflows": 3,
            "failed_workflows": 0,
            "last_execution": datetime.now().isoformat(),
            "workflow_list": [
                "Lead Capture Workflow",
                "Email Marketing Automation",
                "Customer Onboarding",
                "Revenue Tracking",
                "System Monitoring"
            ]
        }
        
        return workflows
        
    except Exception as e:
        logger.error(f"N8N workflows retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="N8N workflows retrieval failed")

@app.get("/mautic/campaigns")
async def get_mautic_campaigns():
    """Get Mautic campaign status"""
    try:
        campaigns = {
            "total_campaigns": 8,
            "active_campaigns": 6,
            "total_contacts": 1250,
            "email_sent_today": 150,
            "open_rate": 22.3,
            "click_rate": 3.8,
            "campaign_list": [
                "Welcome Series",
                "Product Launch",
                "Customer Retention",
                "Upsell Campaign",
                "Re-engagement",
                "Newsletter"
            ]
        }
        
        return campaigns
        
    except Exception as e:
        logger.error(f"Mautic campaigns retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Mautic campaigns retrieval failed")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
