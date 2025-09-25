#!/usr/bin/env python3
"""
SSI Loop Prevention System - Windows Compatible
Prevents infinite loops and implements timeout protocols
"""

import time
import threading
from typing import Callable, Any, Optional
from datetime import datetime, timedelta

class SSILoopPreventionSystem:
    """SSI-compliant loop prevention and timeout system - Windows compatible"""
    
    def __init__(self, max_execution_time: int = 30, max_retries: int = 3):
        self.max_execution_time = max_execution_time
        self.max_retries = max_retries
        self.active_tasks = {}
        self.timeout_handlers = {}
        
    def execute_with_timeout(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with timeout protection - Windows compatible"""
        task_id = f"task_{int(time.time())}"
        result = None
        error = None
        
        def timeout_handler():
            raise TimeoutError(f"Task {task_id} exceeded {self.max_execution_time} seconds")
        
        # Use threading for timeout on Windows
        timeout_timer = threading.Timer(self.max_execution_time, timeout_handler)
        timeout_timer.start()
        
        try:
            result = func(*args, **kwargs)
        except TimeoutError as e:
            error = e
            print(f"⏰ TIMEOUT: {e}")
        except Exception as e:
            error = e
            print(f"❌ ERROR: {e}")
        finally:
            timeout_timer.cancel()
        
        return result, error
    
    def detect_loop_pattern(self, task_history: list, current_task: str) -> bool:
        """Detect if current task is part of a loop pattern"""
        if len(task_history) < 3:
            return False
        
        # Check for repeated patterns
        recent_tasks = task_history[-5:]  # Last 5 tasks
        if len(set(recent_tasks)) < len(recent_tasks) * 0.6:  # Less than 60% unique
            return True
        
        # Check for same task repeated
        if current_task in recent_tasks[-3:]:
            return True
        
        return False
    
    def prevent_loop(self, task: str, task_history: list) -> bool:
        """Prevent loop execution"""
        if self.detect_loop_pattern(task_history, task):
            print(f"🔄 LOOP DETECTED: Preventing execution of '{task}'")
            print(f"📊 Task History: {task_history[-5:]}")
            return False
        return True
    
    def safe_execute(self, func: Callable, task_name: str, *args, **kwargs) -> Any:
        """Safely execute function with loop prevention and timeout"""
        # Add to task history
        if not hasattr(self, 'task_history'):
            self.task_history = []
        
        self.task_history.append(task_name)
        
        # Check for loops
        if not self.prevent_loop(task_name, self.task_history):
            return None, "Loop prevented"
        
        # Execute with timeout
        result, error = self.execute_with_timeout(func, *args, **kwargs)
        
        return result, error

# Global loop prevention instance
loop_prevention = SSILoopPreventionSystem(max_execution_time=30, max_retries=3)

def ssi_safe_execute(func: Callable, task_name: str, *args, **kwargs) -> Any:
    """SSI-compliant safe execution with loop prevention"""
    return loop_prevention.safe_execute(func, task_name, *args, **kwargs)

# Test the loop prevention system
if __name__ == "__main__":
    def test_function():
        print("Testing function execution...")
        time.sleep(2)
        return "Success"
    
    def infinite_loop_function():
        print("This would loop forever...")
        while True:
            time.sleep(1)
    
    # Test normal execution
    result, error = ssi_safe_execute(test_function, "test_normal")
    print(f"Normal execution: {result}, Error: {error}")
    
    # Test timeout protection
    result, error = ssi_safe_execute(infinite_loop_function, "test_infinite")
    print(f"Infinite loop test: {result}, Error: {error}")
    
    # Test loop detection
    for i in range(5):
        result, error = ssi_safe_execute(test_function, "repeated_task")
        print(f"Repeated task {i}: {result}, Error: {error}")
