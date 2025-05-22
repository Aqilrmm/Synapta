
import os
import importlib.util
import inspect
import logging
from typing import Dict, List
from pathlib import Path
from core.agent_base import AgentBase
from core.shared_context import SharedContext

class AgentRegistry:
    """Registry for managing all agents"""
    
    def __init__(self, message_bus, scheduler):
        self.logger = logging.getLogger("registry")
        self.message_bus = message_bus
        self.scheduler = scheduler
        self.shared_context = SharedContext()
        self.agents = {}  # agent_name -> agent_instance
        self.agent_configs = {}
    
    async def discover_agents(self):
        """Discover all available agents in the agents directory"""
        agents_dir = Path("agents")
        if not agents_dir.exists():
            self.logger.warning("⚠️  Agents directory not found")
            return
        
        for agent_dir in agents_dir.iterdir():
            if agent_dir.is_dir() and not agent_dir.name.startswith('_'):
                await self._load_agent(agent_dir)
    
    async def _load_agent(self, agent_dir: Path):
        """Load a single agent from directory"""
        agent_name = agent_dir.name
        main_py = agent_dir / "main.py"
        config_yaml = agent_dir / "config.yaml"
        
        if not main_py.exists():
            self.logger.warning(f"⚠️  No main.py found for agent: {agent_name}")
            return
        
        try:
            # Import agent module
            spec = importlib.util.spec_from_file_location(
                f"agents.{agent_name}.main", main_py
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find agent class
            agent_class = None
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, AgentBase) and 
                    obj != AgentBase):
                    agent_class = obj
                    break
            
            if agent_class:
                # Create agent instance
                config_path = str(config_yaml) if config_yaml.exists() else None
                agent = agent_class(agent_name, config_path)
                
                # Setup agent dependencies
                agent.set_message_bus(self.message_bus)
                agent.set_shared_context(self.shared_context)
                
                # Register agent
                self.agents[agent_name] = agent
                self.message_bus.register_agent(agent_name, agent)
                
                self.logger.info(f"✅ Loaded agent: {agent_name}")
            else:
                self.logger.warning(f"⚠️  No valid agent class found in: {agent_name}")
                
        except Exception as e:
            self.logger.error(f"❌ Failed to load agent {agent_name}: {e}")
    
    async def start_all_agents(self):
        """Start all registered agents"""
        for agent_name, agent in self.agents.items():
            try:
                await agent.start()
            except Exception as e:
                self.logger.error(f"❌ Failed to start agent {agent_name}: {e}")
    
    async def stop_all_agents(self):
        """Stop all running agents"""
        for agent_name, agent in self.agents.items():
            try:
                await agent.stop()
            except Exception as e:
                self.logger.error(f"❌ Failed to stop agent {agent_name}: {e}")
    
    def get_active_agents(self) -> List[str]:
        """Get list of active agent names"""
        return [name for name, agent in self.agents.items() if agent.is_running]
    
    def get_agent(self, agent_name: str) -> AgentBase:
        """Get specific agent instance"""
        return self.agents.get(agent_name)