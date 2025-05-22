import asyncio
import logging
from typing import Dict, Any
from core.agent_base import AgentBase

class ExampleAgent(AgentBase):
    """
    Example agent template
    Copy this to create new agents
    """
    
    def __init__(self, agent_name: str, config_path: str = None):
        super().__init__(agent_name, config_path)
        self.counter = 0
    
    async def initialize(self):
        """Initialize agent resources"""
        self.logger.info("🔧 Initializing Example Agent...")
        
        # Example: Subscribe to message bus topics
        if self.message_bus:
            self.message_bus.subscribe("example_topic", self._handle_topic_message)
        
        # Example: Set shared context data
        if self.shared_context:
            await self.shared_context.set("example_agent_status", "initialized")
        
        self.logger.info("✅ Example Agent initialized")
    
    async def execute(self):
        """Main agent execution logic"""
        self.counter += 1
        self.logger.info(f"🔄 Example Agent execution #{self.counter}")
        
        # Example: Update shared context
        if self.shared_context:
            await self.shared_context.set("example_counter", self.counter)
        
        # Example: Send message to other agents
        if self.counter % 5 == 0:
            self.broadcast_message({
                "type": "status_update",
                "counter": self.counter,
                "message": f"Example Agent has executed {self.counter} times"
            })
        
        # Example: Custom logic based on configuration
        if self.config.get('custom_action_enabled', False):
            await self._perform_custom_action()
    
    async def cleanup(self):
        """Cleanup agent resources"""
        self.logger.info("🧹 Cleaning up Example Agent...")
        
        # Example: Update shared context
        if self.shared_context:
            await self.shared_context.set("example_agent_status", "stopped")
        
        self.logger.info("✅ Example Agent cleaned up")
    
    async def handle_message(self, sender: str, message: Dict[str, Any]):
        """Handle incoming messages from other agents"""
        self.logger.info(f"📨 Received message from {sender}: {message.get('type', 'unknown')}")
        
        message_type = message.get('type')
        
        if message_type == "ping":
            # Respond to ping messages
            self.send_message(sender, {
                "type": "pong",
                "original_message": message,
                "response_from": self.agent_name
            })
        
        elif message_type == "request_status":
            # Send status information
            self.send_message(sender, {
                "type": "status_response",
                "agent": self.agent_name,
                "counter": self.counter,
                "is_running": self.is_running
            })
    
    async def _handle_topic_message(self, message: Dict[str, Any]):
        """Handle messages from subscribed topics"""
        self.logger.info(f"📢 Topic message received: {message}")
    
    async def _perform_custom_action(self):
        """Example custom action"""
        self.logger.info("⚡ Performing custom action...")
        
        # Example: Access shared data from other agents
        if self.shared_context:
            other_data = await self.shared_context.get("other_agent_data")
            if other_data:
                self.logger.info(f"📊 Found shared data: {other_data}")
