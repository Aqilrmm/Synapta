import unittest
from agents.bug_hunter.main import BugHunterAgent

class TestBugHunterAgent(unittest.TestCase):
    
    def setUp(self):
        self.agent = BugHunterAgent("test_bug_hunter", config_path=None)

    def test_initialization(self):
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.agent_name, "test_bug_hunter")
        self.assertIsInstance(self.agent, BugHunterAgent)

    def test_execute(self):
        # Assuming the execute method returns a result
        result = self.agent.execute()
        self.assertIsNotNone(result)
        self.assertIn("status", result)

    def test_handle_message(self):
        test_message = {"type": "ping"}
        response = self.agent.handle_message("test_sender", test_message)
        self.assertEqual(response["type"], "pong")

    def tearDown(self):
        self.agent = None

if __name__ == "__main__":
    unittest.main()