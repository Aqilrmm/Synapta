
import asyncio
import logging
from typing import Callable, Dict, Any
from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class ScheduledTask:
    """Represents a scheduled task"""
    task_id: str
    func: Callable
    next_run: datetime
    interval: timedelta = None
    args: tuple = ()
    kwargs: dict = None
    
    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}

class Scheduler:
    """Task scheduler for agents"""
    
    def __init__(self):
        self.logger = logging.getLogger("scheduler")
        self.tasks = {}  # task_id -> ScheduledTask
        self.is_running = False
        self._scheduler_task = None
    
    def schedule_once(self, task_id: str, func: Callable, 
                     delay_seconds: int, *args, **kwargs):
        """Schedule a task to run once after delay"""
        next_run = datetime.now() + timedelta(seconds=delay_seconds)
        task = ScheduledTask(task_id, func, next_run, None, args, kwargs)
        self.tasks[task_id] = task
        self.logger.info(f"⏰ Scheduled one-time task: {task_id}")
    
    def schedule_recurring(self, task_id: str, func: Callable, 
                          interval_seconds: int, *args, **kwargs):
        """Schedule a recurring task"""
        next_run = datetime.now() + timedelta(seconds=interval_seconds)
        interval = timedelta(seconds=interval_seconds)
        task = ScheduledTask(task_id, func, next_run, interval, args, kwargs)
        self.tasks[task_id] = task
        self.logger.info(f"🔄 Scheduled recurring task: {task_id} (every {interval_seconds}s)")
    
    def cancel_task(self, task_id: str):
        """Cancel a scheduled task"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.logger.info(f"❌ Cancelled task: {task_id}")
    
    async def start(self):
        """Start the scheduler"""
        if self.is_running:
            return
        
        self.is_running = True
        self._scheduler_task = asyncio.create_task(self._scheduler_loop())
        self.logger.info("⏰ Scheduler started")
    
    async def stop(self):
        """Stop the scheduler"""
        self.is_running = False
        if self._scheduler_task:
            self._scheduler_task.cancel()
            try:
                await self._scheduler_task
            except asyncio.CancelledError:
                pass
        self.logger.info("⏰ Scheduler stopped")
    
    async def _scheduler_loop(self):
        """Main scheduler loop"""
        while self.is_running:
            try:
                now = datetime.now()
                tasks_to_run = []
                
                for task_id, task in list(self.tasks.items()):
                    if now >= task.next_run:
                        tasks_to_run.append((task_id, task))
                
                # Execute due tasks
                for task_id, task in tasks_to_run:
                    try:
                        asyncio.create_task(
                            task.func(*task.args, **task.kwargs)
                        )
                        
                        # Reschedule if recurring
                        if task.interval:
                            task.next_run = now + task.interval
                        else:
                            # Remove one-time tasks
                            del self.tasks[task_id]
                            
                    except Exception as e:
                        self.logger.error(f"❌ Task execution error {task_id}: {e}")
                
                await asyncio.sleep(1)  # Check every second
                
            except Exception as e:
                self.logger.error(f"❌ Scheduler loop error: {e}")
                await asyncio.sleep(5)