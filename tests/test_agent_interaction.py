# test_agent_interaction.py

import unittest
from core.registry import AgentRegistry
from core.message_bus import MessageBus
from core.scheduler import Scheduler
from core.shared_context import SharedContext
from agents.example_agent.main import ExampleAgent

class TestAgentInteraction(unittest.TestCase):

    def setUp(self):
        self.message_bus = MessageBus()
        self.scheduler = Scheduler()
        self.shared_context = SharedContext()
        self.registry = AgentRegistry(self.message_bus, self.scheduler)
        self.agent = ExampleAgent("test_agent")

        # Register the agent
        self.registry.agents["test_agent"] = self.agent
        self.message_bus.register_agent("test_agent", self.agent)

    def test_agent_initialization(self):
        self.assertFalse(self.agent.is_running)
        self.agent.initialize()
        self.assertTrue(self.agent.is_running)

    def test_agent_execution(self):
        self.agent.initialize()
        self.agent.start()
        self.assertTrue(self.agent.is_running)

        # Simulate execution
        self.agent.execute()
        self.assertGreater(self.agent.counter, 0)

    def test_message_handling(self):
        self.agent.initialize()
        self.agent.start()

        # Send a message to the agent
        self.agent.handle_message("other_agent", {"type": "ping"})
        self.assertEqual(self.agent.counter, 1)

    def tearDown(self):
        self.agent.stop()
        self.assertFalse(self.agent.is_running)

if __name__ == "__main__":
    unittest.main()