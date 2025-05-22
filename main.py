
import asyncio
import logging
from core.registry import AgentRegistry
from core.message_bus import MessageBus
from core.scheduler import Scheduler
from utils.logger import setup_logger
from utils.helpers import load_config

async def main():
    """Main entry point for the Synapta"""
    
    # Setup logging
    logger = setup_logger()
    logger.info("🚀 Starting Synapta...")
    
    try:
        # Load global configuration
        config = load_config()
        
        # Initialize core components
        message_bus = MessageBus()
        scheduler = Scheduler()
        registry = AgentRegistry(message_bus, scheduler)
        
        # Discover and register all agents
        await registry.discover_agents()
        
        # Start all registered agents
        await registry.start_all_agents()
        
        logger.info("✅ All agents started successfully!")
        logger.info(f"📊 Active agents: {len(registry.get_active_agents())}")
        
        # Keep the framework running
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down Synapta...")
        await registry.stop_all_agents()
        logger.info("👋 Goodbye!")
    except Exception as e:
        logger.error(f"❌ Framework error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())