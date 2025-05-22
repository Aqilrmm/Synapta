# File: /home/mazeluna/Codingan/asalasal/agentframework/core/agent_base.py

"""
Base Agent Class
All agents must inherit from this class
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from utils.helpers import load_yaml_config

class AgentBase(ABC):
    """Base class for all agents in the framework"""
    
    def __init__(self, agent_name: str, config_path: str = None):
        self.agent_name = agent_name
        self.logger = logging.getLogger(f"agent.{agent_name}")
        self.is_running = False
        self.message_bus = None
        self.shared_context = None
        
        # Load agent-specific configuration
        if config_path:
            self.config = load_yaml_config(config_path)
        else:
            self.config = {}
    
    def set_message_bus(self, message_bus):
        """Set the message bus for inter-agent communication"""
        self.message_bus = message_bus
    
    def set_shared_context(self, shared_context):
        """Set shared context for data sharing between agents"""
        self.shared_context = shared_context
    
    async def start(self):
        """Start the agent"""
        self.logger.info(f"🟢 Starting agent: {self.agent_name}")
        self.is_running = True
        await self.initialize()
        
        # Start the main agent loop
        asyncio.create_task(self._agent_loop())
    
    async def stop(self):
        """Stop the agent"""
        self.logger.info(f"🔴 Stopping agent: {self.agent_name}")
        self.is_running = False
        await self.cleanup()
    
    async def _agent_loop(self):
        """Main agent execution loop"""
        while self.is_running:
            try:
                await self.execute()
                await asyncio.sleep(self.config.get('execution_interval', 60))
            except Exception as e:
                self.logger.error(f"❌ Agent execution error: {e}")
                await asyncio.sleep(5)
    
    def send_message(self, target_agent: str, message: Dict[str, Any]):
        """Send message to another agent"""
        if self.message_bus:
            self.message_bus.send_message(self.agent_name, target_agent, message)
    
    def broadcast_message(self, message: Dict[str, Any]):
        """Broadcast message to all agents"""
        if self.message_bus:
            self.message_bus.broadcast_message(self.agent_name, message)
    
    @abstractmethod
    async def initialize(self):
        """Initialize agent resources"""
        pass
    
    @abstractmethod
    async def execute(self):
        """Main agent execution logic"""
        pass
    
    @abstractmethod
    async def cleanup(self):
        """Cleanup agent resources"""
        pass
    
    @abstractmethod
    async def handle_message(self, sender: str, message: Dict[str, Any]):
        """Handle incoming messages from other agents"""
        pass