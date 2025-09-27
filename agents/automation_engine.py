"""
MEM_AGENT Automation Engine
Advanced automation and workflow management system
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
import schedule
import time
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class AutomationTask:
    """Data structure for automation tasks"""
    id: str
    name: str
    description: str
    function: Callable
    schedule: str  # Cron-like schedule
    priority: TaskPriority
    status: TaskStatus = TaskStatus.PENDING
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3
    parameters: Dict[str, Any] = None
    dependencies: List[str] = None
    created_at: datetime = None

@dataclass
class WorkflowStep:
    """Data structure for workflow steps"""
    step_id: str
    name: str
    action: str
    parameters: Dict[str, Any]
    condition: Optional[str] = None
    on_success: Optional[str] = None
    on_failure: Optional[str] = None
    timeout: int = 300  # seconds

class MEMAgentAutomationEngine:
    """Advanced automation engine for MEM_AGENT system"""
    
    def __init__(self):
        self.tasks = {}
        self.workflows = {}
        self.running_tasks = set()
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        
    def create_task(self, task_id: str, name: str, description: str, 
                   function: Callable, schedule: str, priority: TaskPriority = TaskPriority.MEDIUM,
                   parameters: Dict[str, Any] = None, dependencies: List[str] = None) -> AutomationTask:
        """Create a new automation task"""
        task = AutomationTask(
            id=task_id,
            name=name,
            description=description,
            function=function,
            schedule=schedule,
            priority=priority,
            parameters=parameters or {},
            dependencies=dependencies or [],
            created_at=datetime.now()
        )
        
        # Calculate next run time
        task.next_run = self._calculate_next_run(schedule)
        
        self.tasks[task_id] = task
        self.logger.info(f"Created task: {task_id}")
        
        return task
    
    def create_workflow(self, workflow_id: str, name: str, steps: List[WorkflowStep]) -> Dict[str, Any]:
        """Create a new workflow"""
        workflow = {
            'id': workflow_id,
            'name': name,
            'steps': {step.step_id: step for step in steps},
            'status': 'draft',
            'created_at': datetime.now(),
            'last_run': None,
            'next_run': None
        }
        
        self.workflows[workflow_id] = workflow
        self.logger.info(f"Created workflow: {workflow_id}")
        
        return workflow
    
    def schedule_task(self, task_id: str) -> bool:
        """Schedule a task for execution"""
        if task_id not in self.tasks:
            self.logger.error(f"Task not found: {task_id}")
            return False
        
        task = self.tasks[task_id]
        
        # Check dependencies
        if not self._check_dependencies(task):
            self.logger.warning(f"Dependencies not met for task: {task_id}")
            return False
        
        # Schedule the task
        if task.schedule == "immediate":
            asyncio.create_task(self._execute_task(task_id))
        else:
            # Use schedule library for recurring tasks
            schedule.every().do(self._execute_task_sync, task_id)
        
        self.logger.info(f"Scheduled task: {task_id}")
        return True
    
    def execute_workflow(self, workflow_id: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a workflow"""
        if workflow_id not in self.workflows:
            self.logger.error(f"Workflow not found: {workflow_id}")
            return {'success': False, 'error': 'Workflow not found'}
        
        workflow = self.workflows[workflow_id]
        workflow['status'] = 'running'
        workflow['last_run'] = datetime.now()
        
        results = {
            'workflow_id': workflow_id,
            'start_time': datetime.now(),
            'steps_completed': [],
            'steps_failed': [],
            'final_result': None,
            'success': True
        }
        
        try:
            # Execute steps in order
            for step_id, step in workflow['steps'].items():
                self.logger.info(f"Executing workflow step: {step_id}")
                
                # Check condition if exists
                if step.condition and not self._evaluate_condition(step.condition, parameters):
                    self.logger.info(f"Skipping step {step_id} due to condition")
                    continue
                
                # Execute step
                step_result = self._execute_workflow_step(step, parameters)
                
                if step_result['success']:
                    results['steps_completed'].append(step_id)
                    # Move to next step
                    if step.on_success:
                        # Handle success action
                        pass
                else:
                    results['steps_failed'].append(step_id)
                    results['success'] = False
                    
                    # Handle failure
                    if step.on_failure:
                        # Handle failure action
                        pass
                    break
            
            workflow['status'] = 'completed' if results['success'] else 'failed'
            results['end_time'] = datetime.now()
            
        except Exception as e:
            self.logger.error(f"Workflow execution failed: {str(e)}")
            workflow['status'] = 'failed'
            results['success'] = False
            results['error'] = str(e)
        
        return results
    
    def start_automation_engine(self):
        """Start the automation engine"""
        self.is_running = True
        self.logger.info("Starting MEM_AGENT Automation Engine")
        
        # Start the scheduler
        asyncio.create_task(self._run_scheduler())
    
    def stop_automation_engine(self):
        """Stop the automation engine"""
        self.is_running = False
        self.logger.info("Stopping MEM_AGENT Automation Engine")
    
    async def _run_scheduler(self):
        """Run the task scheduler"""
        while self.is_running:
            try:
                # Check for tasks that need to run
                current_time = datetime.now()
                
                for task_id, task in self.tasks.items():
                    if (task.status == TaskStatus.PENDING and 
                        task.next_run and 
                        current_time >= task.next_run and
                        task_id not in self.running_tasks):
                        
                        asyncio.create_task(self._execute_task(task_id))
                
                # Run scheduled tasks
                schedule.run_pending()
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Scheduler error: {str(e)}")
                await asyncio.sleep(60)
    
    async def _execute_task(self, task_id: str):
        """Execute a task asynchronously"""
        if task_id in self.running_tasks:
            return
        
        self.running_tasks.add(task_id)
        task = self.tasks[task_id]
        task.status = TaskStatus.RUNNING
        task.last_run = datetime.now()
        
        try:
            self.logger.info(f"Executing task: {task_id}")
            
            # Execute the task function
            if asyncio.iscoroutinefunction(task.function):
                result = await task.function(**task.parameters)
            else:
                result = task.function(**task.parameters)
            
            task.status = TaskStatus.COMPLETED
            task.retry_count = 0
            
            # Calculate next run time
            task.next_run = self._calculate_next_run(task.schedule)
            
            self.logger.info(f"Task completed: {task_id}")
            
        except Exception as e:
            self.logger.error(f"Task failed: {task_id} - {str(e)}")
            task.retry_count += 1
            
            if task.retry_count < task.max_retries:
                task.status = TaskStatus.PENDING
                task.next_run = datetime.now() + timedelta(minutes=5)  # Retry in 5 minutes
            else:
                task.status = TaskStatus.FAILED
            
        finally:
            self.running_tasks.discard(task_id)
    
    def _execute_task_sync(self, task_id: str):
        """Execute a task synchronously (for schedule library)"""
        asyncio.create_task(self._execute_task(task_id))
    
    def _execute_workflow_step(self, step: WorkflowStep, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        try:
            # Map action to function
            action_functions = {
                'http_request': self._execute_http_request,
                'data_processing': self._execute_data_processing,
                'email_send': self._execute_email_send,
                'database_query': self._execute_database_query,
                'file_operation': self._execute_file_operation,
                'api_call': self._execute_api_call
            }
            
            if step.action not in action_functions:
                return {'success': False, 'error': f'Unknown action: {step.action}'}
            
            result = action_functions[step.action](step.parameters, parameters)
            return {'success': True, 'result': result}
            
        except Exception as e:
            self.logger.error(f"Workflow step failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _execute_http_request(self, step_params: Dict, workflow_params: Dict) -> Dict[str, Any]:
        """Execute HTTP request action"""
        import requests
        
        url = step_params.get('url')
        method = step_params.get('method', 'GET')
        headers = step_params.get('headers', {})
        data = step_params.get('data')
        
        response = requests.request(method, url, headers=headers, json=data)
        
        return {
            'status_code': response.status_code,
            'content': response.text,
            'headers': dict(response.headers)
        }
    
    def _execute_data_processing(self, step_params: Dict, workflow_params: Dict) -> Dict[str, Any]:
        """Execute data processing action"""
        # Implement data processing logic
        return {'processed_data': 'Sample processed data'}
    
    def _execute_email_send(self, step_params: Dict, workflow_params: Dict) -> Dict[str, Any]:
        """Execute email sending action"""
        # Implement email sending logic
        return {'email_sent': True, 'recipient': step_params.get('to')}
    
    def _execute_database_query(self, step_params: Dict, workflow_params: Dict) -> Dict[str, Any]:
        """Execute database query action"""
        # Implement database query logic
        return {'query_result': 'Sample query result'}
    
    def _execute_file_operation(self, step_params: Dict, workflow_params: Dict) -> Dict[str, Any]:
        """Execute file operation action"""
        # Implement file operation logic
        return {'file_operation': 'completed'}
    
    def _execute_api_call(self, step_params: Dict, workflow_params: Dict) -> Dict[str, Any]:
        """Execute API call action"""
        # Implement API call logic
        return {'api_response': 'Sample API response'}
    
    def _calculate_next_run(self, schedule: str) -> Optional[datetime]:
        """Calculate next run time for a schedule"""
        if schedule == "immediate":
            return datetime.now()
        elif schedule == "daily":
            return datetime.now() + timedelta(days=1)
        elif schedule == "hourly":
            return datetime.now() + timedelta(hours=1)
        elif schedule.startswith("every_"):
            # Parse "every_X_minutes" or "every_X_hours"
            parts = schedule.split("_")
            if len(parts) >= 3:
                interval = int(parts[1])
                unit = parts[2]
                if unit == "minutes":
                    return datetime.now() + timedelta(minutes=interval)
                elif unit == "hours":
                    return datetime.now() + timedelta(hours=interval)
        
        return None
    
    def _check_dependencies(self, task: AutomationTask) -> bool:
        """Check if task dependencies are met"""
        for dep_id in task.dependencies:
            if dep_id not in self.tasks:
                return False
            
            dep_task = self.tasks[dep_id]
            if dep_task.status != TaskStatus.COMPLETED:
                return False
        
        return True
    
    def _evaluate_condition(self, condition: str, parameters: Dict[str, Any]) -> bool:
        """Evaluate a condition string"""
        try:
            # Simple condition evaluation
            # In a real implementation, you'd use a proper expression evaluator
            return eval(condition, {"parameters": parameters})
        except:
            return False
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific task"""
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        return {
            'id': task.id,
            'name': task.name,
            'status': task.status.value,
            'last_run': task.last_run.isoformat() if task.last_run else None,
            'next_run': task.next_run.isoformat() if task.next_run else None,
            'retry_count': task.retry_count,
            'created_at': task.created_at.isoformat()
        }
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific workflow"""
        if workflow_id not in self.workflows:
            return None
        
        workflow = self.workflows[workflow_id]
        return {
            'id': workflow['id'],
            'name': workflow['name'],
            'status': workflow['status'],
            'last_run': workflow['last_run'].isoformat() if workflow['last_run'] else None,
            'created_at': workflow['created_at'].isoformat()
        }
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """List all tasks"""
        return [self.get_task_status(task_id) for task_id in self.tasks.keys()]
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all workflows"""
        return [self.get_workflow_status(workflow_id) for workflow_id in self.workflows.keys()]

# Example usage and predefined automation tasks
def create_mem_agent_automations(engine: MEMAgentAutomationEngine):
    """Create predefined MEM_AGENT automation tasks"""
    
    # Health monitoring task
    async def health_monitor():
        """Monitor system health"""
        import requests
        try:
            response = requests.get("http://localhost:8000/health", timeout=10)
            if response.status_code == 200:
                print("System health check passed")
            else:
                print(f"System health check failed: {response.status_code}")
        except Exception as e:
            print(f"Health check error: {str(e)}")
    
    # Business metrics collection task
    async def collect_business_metrics():
        """Collect business metrics"""
        import requests
        try:
            response = requests.get("http://localhost:8000/business/metrics", timeout=10)
            if response.status_code == 200:
                metrics = response.json()
                print(f"Business metrics collected: {metrics}")
            else:
                print(f"Business metrics collection failed: {response.status_code}")
        except Exception as e:
            print(f"Business metrics error: {str(e)}")
    
    # Data scraping task
    async def daily_data_scrape():
        """Daily data scraping task"""
        from .data_scraper import MEMAgentDataScraper
        scraper = MEMAgentDataScraper()
        
        # Scrape business intelligence sources
        urls = [
            "https://example-business-news.com",
            "https://example-market-analysis.com"
        ]
        
        results = scraper.scrape_multiple_urls(urls)
        print(f"Daily scrape completed: {len(results)} items scraped")
    
    # Create tasks
    engine.create_task(
        task_id="health_monitor",
        name="System Health Monitor",
        description="Monitor system health every 5 minutes",
        function=health_monitor,
        schedule="every_5_minutes",
        priority=TaskPriority.HIGH
    )
    
    engine.create_task(
        task_id="business_metrics",
        name="Business Metrics Collector",
        description="Collect business metrics every hour",
        function=collect_business_metrics,
        schedule="every_1_hours",
        priority=TaskPriority.MEDIUM
    )
    
    engine.create_task(
        task_id="daily_scrape",
        name="Daily Data Scraper",
        description="Scrape business data daily",
        function=daily_data_scrape,
        schedule="daily",
        priority=TaskPriority.MEDIUM
    )

if __name__ == "__main__":
    # Example usage
    engine = MEMAgentAutomationEngine()
    
    # Create predefined automations
    create_mem_agent_automations(engine)
    
    # Start the engine
    engine.start_automation_engine()
    
    # List tasks
    print("Available tasks:")
    for task in engine.list_tasks():
        print(f"- {task['name']}: {task['status']}")
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        engine.stop_automation_engine()
        print("Automation engine stopped")
