#!/usr/bin/env python3
"""
AI Agent Framework - Command Line Interface
Interactive CLI for managing and monitoring agents
"""

import asyncio
import argparse
import sys
import os
from pathlib import Path
from typing import Dict, Any
import yaml
import json

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.registry import AgentRegistry
from core.message_bus import MessageBus
from core.scheduler import Scheduler
from utils.logger import setup_logger, get_logger
from utils.helpers import load_config, load_yaml_config

class AgentFrameworkCLI:
    """Command line interface for the AI Agent Framework"""
    
    def __init__(self):
        self.logger = setup_logger()
        self.registry = None
        self.message_bus = None
        self.scheduler = None
        self.is_running = False
    
    async def initialize(self):
        """Initialize the framework components"""
        try:
            config = load_config()
            self.message_bus = MessageBus()
            self.scheduler = Scheduler()
            self.registry = AgentRegistry(self.message_bus, self.scheduler)
            
            await self.message_bus.start()
            await self.scheduler.start()
            
            self.logger.info("🚀 Framework components initialized")
            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize framework: {e}")
            return False
    
    async def discover_agents(self):
        """Discover available agents"""
        if not self.registry:
            print("❌ Framework not initialized")
            return
        
        print("🔍 Discovering agents...")
        await self.registry.discover_agents()
        
        agents = list(self.registry.agents.keys())
        if agents:
            print(f"✅ Found {len(agents)} agents:")
            for agent in agents:
                status = "🟢 Running" if self.registry.agents[agent].is_running else "🔴 Stopped"
                print(f"  • {agent} - {status}")
        else:
            print("⚠️  No agents found")
    
    async def start_agent(self, agent_name: str):
        """Start a specific agent"""
        if not self.registry:
            print("❌ Framework not initialized")
            return
        
        agent = self.registry.get_agent(agent_name)
        if not agent:
            print(f"❌ Agent '{agent_name}' not found")
            return
        
        if agent.is_running:
            print(f"⚠️  Agent '{agent_name}' is already running")
            return
        
        try:
            await agent.start()
            print(f"✅ Started agent: {agent_name}")
        except Exception as e:
            print(f"❌ Failed to start agent '{agent_name}': {e}")
    
    async def stop_agent(self, agent_name: str):
        """Stop a specific agent"""
        if not self.registry:
            print("❌ Framework not initialized")
            return
        
        agent = self.registry.get_agent(agent_name)
        if not agent:
            print(f"❌ Agent '{agent_name}' not found")
            return
        
        if not agent.is_running:
            print(f"⚠️  Agent '{agent_name}' is not running")
            return
        
        try:
            await agent.stop()
            print(f"✅ Stopped agent: {agent_name}")
        except Exception as e:
            print(f"❌ Failed to stop agent '{agent_name}': {e}")
    
    async def start_all_agents(self):
        """Start all discovered agents"""
        if not self.registry:
            print("❌ Framework not initialized")
            return
        
        print("🚀 Starting all agents...")
        await self.registry.start_all_agents()
        active_agents = self.registry.get_active_agents()
        print(f"✅ Started {len(active_agents)} agents")
    
    async def stop_all_agents(self):
        """Stop all running agents"""
        if not self.registry:
            print("❌ Framework not initialized")
            return
        
        print("🛑 Stopping all agents...")
        await self.registry.stop_all_agents()
        print("✅ All agents stopped")
    
    async def show_status(self):
        """Show framework and agent status"""
        if not self.registry:
            print("❌ Framework not initialized")
            return
        
        print("\n📊 AI Agent Framework Status")
        print("=" * 40)
        
        # Framework status
        print(f"Framework Status: {'🟢 Running' if self.is_running else '🔴 Stopped'}")
        print(f"Message Bus: {'🟢 Active' if self.message_bus else '🔴 Inactive'}")
        print(f"Scheduler: {'🟢 Active' if self.scheduler else '🔴 Inactive'}")
        
        # Agent status
        total_agents = len(self.registry.agents)
        active_agents = len(self.registry.get_active_agents())
        
        print(f"\nAgents: {active_agents}/{total_agents} active")
        
        if self.registry.agents:
            print("\nAgent Details:")
            for name, agent in self.registry.agents.items():
                status = "🟢 Running" if agent.is_running else "🔴 Stopped"
                config_info = f"(Interval: {agent.config.get('execution_interval', 'N/A')}s)" if agent.config else ""
                print(f"  • {name} - {status} {config_info}")
        
        # Shared context info
        if hasattr(self.registry.shared_context, '_data'):
            context_keys = await self.registry.shared_context.get_all_keys()
            print(f"\nShared Context: {len(context_keys)} keys")
            if context_keys:
                print("  Keys:", ", ".join(context_keys[:5]))
                if len(context_keys) > 5:
                    print(f"  ... and {len(context_keys) - 5} more")
    
    async def send_message(self, sender: str, target: str, message_type: str, content: str):
        """Send a message between agents"""
        if not self.registry:
            print("❌ Framework not initialized")
            return
        
        if target not in self.registry.agents:
            print(f"❌ Target agent '{target}' not found")
            return
        
        message = {
            "type": message_type,
            "content": content,
            "cli_sender": True
        }
        
        self.message_bus.send_message(sender, target, message)
        print(f"📨 Message sent from {sender} to {target}")
    
    async def create_agent(self, agent_name: str):
        """Create a new agent from template"""
        agents_dir = Path("agents")
        new_agent_dir = agents_dir / agent_name
        
        if new_agent_dir.exists():
            print(f"❌ Agent '{agent_name}' already exists")
            return
        
        # Create agent directory structure
        new_agent_dir.mkdir(parents=True)
        features_dir = new_agent_dir / "features"
        features_dir.mkdir()
        
        # Copy template files
        template_dir = agents_dir / "example_agent"
        if template_dir.exists():
            # Copy and modify main.py
            template_main = template_dir / "main.py"
            new_main = new_agent_dir / "main.py"
            
            with open(template_main, 'r') as f:
                content = f.read()
            
            # Replace class name and references
            content = content.replace("ExampleAgent", f"{agent_name.title().replace('_', '')}Agent")
            content = content.replace("Example Agent", f"{agent_name.replace('_', ' ').title()} Agent")
            content = content.replace("example_agent", agent_name)
            
            with open(new_main, 'w') as f:
                f.write(content)
            
            # Copy and modify config.yaml
            template_config = template_dir / "config.yaml"
            new_config = new_agent_dir / "config.yaml"
            
            with open(template_config, 'r') as f:
                config = yaml.safe_load(f)
            
            config['name'] = agent_name
            
            with open(new_config, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            
            # Create __init__.py files
            (new_agent_dir / "__init__.py").touch()
            (features_dir / "__init__.py").touch()
            
            print(f"✅ Created new agent: {agent_name}")
            print(f"📁 Location: {new_agent_dir}")
            print("💡 Edit the files to customize your agent's functionality")
        else:
            print("❌ Template agent not found")
    
    async def interactive_mode(self):
        """Run interactive CLI mode"""
        print("🎯 AI Agent Framework - Interactive Mode")
        print("Type 'help' for available commands, 'quit' to exit")
        
        await self.initialize()
        await self.discover_agents()
        
        while True:
            try:
                command = input("\n🤖 > ").strip().lower()
                
                if command in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                elif command == 'help':
                    self.print_help()
                
                elif command == 'status':
                    await self.show_status()
                
                elif command == 'discover':
                    await self.discover_agents()
                
                elif command == 'start-all':
                    await self.start_all_agents()
                
                elif command == 'stop-all':
                    await self.stop_all_agents()
                
                elif command.startswith('start '):
                    agent_name = command.split(' ', 1)[1]
                    await self.start_agent(agent_name)
                
                elif command.startswith('stop '):
                    agent_name = command.split(' ', 1)[1]
                    await self.stop_agent(agent_name)
                
                elif command.startswith('create '):
                    agent_name = command.split(' ', 1)[1]
                    await self.create_agent(agent_name)
                
                elif command.startswith('message '):
                    parts = command.split(' ')
                    if len(parts) >= 4:
                        _, target, msg_type, content = parts[0], parts[1], parts[2], ' '.join(parts[3:])
                        await self.send_message('cli', target, msg_type, content)
                    else:
                        print("Usage: message <target_agent> <message_type> <content>")
                
                elif command == '':
                    continue
                
                else:
                    print(f"❌ Unknown command: {command}")
                    print("Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        if self.registry:
            await self.stop_all_agents()
    
    def print_help(self):
        """Print help information"""
        help_text = """
🎯 Available Commands:

Agent Management:
  discover              - Discover all available agents
  status               - Show framework and agent status
  start <agent_name>   - Start a specific agent
  stop <agent_name>    - Stop a specific agent
  start-all            - Start all agents
  stop-all             - Stop all agents
  create <agent_name>  - Create new agent from template

Communication:
  message <target> <type> <content> - Send message to agent

General:
  help                 - Show this help message
  quit                 - Exit the CLI

Examples:
  start example_agent
  message example_agent ping hello
  create my_custom_agent
        """
        print(help_text)
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.registry:
            await self.registry.stop_all_agents()
        if self.scheduler:
            await self.scheduler.stop()
        if self.message_bus:
            await self.message_bus.stop()

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="AI Agent Framework CLI")
    parser.add_argument('--interactive', '-i', action='store_true', 
                       help='Run in interactive mode')
    parser.add_argument('--discover', action='store_true',
                       help='Discover available agents')
    parser.add_argument('--start', metavar='AGENT',
                       help='Start specific agent')
    parser.add_argument('--stop', metavar='AGENT',
                       help='Stop specific agent')
    parser.add_argument('--start-all', action='store_true',
                       help='Start all agents')
    parser.add_argument('--stop-all', action='store_true',
                       help='Stop all agents')
    parser.add_argument('--status', action='store_true',
                       help='Show status information')
    parser.add_argument('--create', metavar='AGENT_NAME',
                       help='Create new agent from template')
    
    args = parser.parse_args()
    
    cli = AgentFrameworkCLI()
    
    async def run_cli():
        try:
            if args.interactive:
                await cli.interactive_mode()
            else:
                await cli.initialize()
                
                if args.discover:
                    await cli.discover_agents()
                
                if args.status:
                    await cli.show_status()
                
                if args.start:
                    await cli.start_agent(args.start)
                
                if args.stop:
                    await cli.stop_agent(args.stop)
                
                if args.start_all:
                    await cli.start_all_agents()
                
                if args.stop_all:
                    await cli.stop_all_agents()
                
                if args.create:
                    await cli.create_agent(args.create)
                
                # If no specific action, show help
                if not any([args.discover, args.status, args.start, args.stop, 
                           args.start_all, args.stop_all, args.create]):
                    parser.print_help()
        
        finally:
            await cli.cleanup()
    
    try:
        asyncio.run(run_cli())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ CLI Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()