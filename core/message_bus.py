# The contents of the file: /ai-agent-framework/ai-agent-framework/core/message_bus.py

"""
Message Bus for Inter-Agent Communication
Handles routing messages between agents
"""

import asyncio
import logging
from typing import Dict, Any, Callable, List
from collections import defaultdict

class MessageBus:
    """Message bus for inter-agent communication"""
    
    def __init__(self):
        self.logger = logging.getLogger("message_bus")
        self.subscribers = defaultdict(list)  # topic -> [handlers]
        self.agents = {}  # agent_name -> agent_instance
        self.message_queue = asyncio.Queue()
        self.is_running = False
    
    def register_agent(self, agent_name: str, agent_instance):
        """Register an agent with the message bus"""
        self.agents[agent_name] = agent_instance
        self.logger.info(f"📡 Registered agent: {agent_name}")
    
    def unregister_agent(self, agent_name: str):
        """Unregister an agent from the message bus"""
        if agent_name in self.agents:
            del self.agents[agent_name]
            self.logger.info(f"📡 Unregistered agent: {agent_name}")
    
    def subscribe(self, topic: str, handler: Callable):
        """Subscribe to a message topic"""
        self.subscribers[topic].append(handler)
        self.logger.info(f"📢 New subscription to topic: {topic}")
    
    def send_message(self, sender: str, target: str, message: Dict[str, Any]):
        """Send message to specific agent"""
        if target in self.agents:
            asyncio.create_task(
                self.agents[target].handle_message(sender, message)
            )
        else:
            self.logger.warning(f"⚠️  Target agent not found: {target}")
    
    def broadcast_message(self, sender: str, message: Dict[str, Any]):
        """Broadcast message to all agents"""
        for agent_name, agent in self.agents.items():
            if agent_name != sender:
                asyncio.create_task(
                    agent.handle_message(sender, message)
                )
    
    def publish(self, topic: str, message: Dict[str, Any]):
        """Publish message to topic subscribers"""
        if topic in self.subscribers:
            for handler in self.subscribers[topic]:
                asyncio.create_task(handler(message))
    
    async def start(self):
        """Start the message bus processing loop"""
        self.is_running = True
        self.logger.info("🚌 Message bus started")
    
    async def stop(self):
        """Stop the message bus"""
        self.is_running = False
        self.logger.info("🚌 Message bus stopped")