# 🤖 Synapta

A comprehensive, modular framework for building and managing AI agents with inter-agent communication, shared context, and task scheduling capabilities.

## 🌟 Features

- **Modular Agent Architecture**: Easy-to-extend base class for creating custom agents
- **Inter-Agent Communication**: Message bus system for seamless agent communication
- **Shared Context**: Thread-safe shared data storage between agents
- **Task Scheduling**: Built-in scheduler for periodic and one-time tasks
- **Auto-Discovery**: Automatic agent detection and loading
- **CLI Management**: Interactive command-line interface for agent management
- **Configuration-Driven**: YAML-based configuration for easy customization
- **Async/Await Support**: Modern Python async programming model
- **Comprehensive Logging**: Structured logging with file and console output

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Agent A       │    │   Message Bus    │    │   Agent B       │
│                 │◄──►│                  │◄──►│                 │
│ ┌─────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│ │ Features    │ │    │ │ Routing      │ │    │ │ Features    │ │
│ │ • Scanner   │ │    │ │ • Topics     │ │    │ │ • Analyzer  │ │
│ │ • Analyzer  │ │    │ │ • Broadcast  │ │    │ │ • Reporter  │ │
│ └─────────────┘ │    │ └──────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         ▲                        ▲                        ▲
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  ▼
                    ┌──────────────────────────┐
                    │    Shared Context        │
                    │ ┌──────────────────────┐ │
                    │ │ • Global State       │ │
                    │ │ • Cross-Agent Data   │ │
                    │ │ • TTL Support        │ │
                    │ └──────────────────────┘ │
                    └──────────────────────────┘
```

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Aqilrmm/Synapta
   cd Synapta
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp config/env.example .env
   # Edit .env with your API keys and configurations
   ```

4. **Run the framework**:
   ```bash
   python main.py
   ```

### Using the CLI

The framework includes a powerful CLI for managing agents:

```bash
# Interactive mode
python interface/cli.py --interactive

# Discover available agents
python interface/cli.py --discover

# Start all agents
python interface/cli.py --start-all

# Start specific agent
python interface/cli.py --start example_agent

# Check status
python interface/cli.py --status

# Create new agent from template
python interface/cli.py --create my_new_agent
```

## 📁 Project Structure

```
Synapta/
├── agents/                     # Agent implementations
│   ├── bug_hunter/            # Bug hunting agent
│   ├── client_finder/         # Client finding agent
│   └── example_agent/         # Template agent
├── core/                      # Framework core
│   ├── agent_base.py         # Base agent class
│   ├── message_bus.py        # Inter-agent messaging
│   ├── registry.py           # Agent discovery & management
│   ├── scheduler.py          # Task scheduling
│   └── shared_context.py     # Shared data storage
├── utils/                     # Utilities
│   ├── logger.py             # Logging configuration
│   └── helpers.py            # Helper functions
├── config/                    # Configuration files
│   ├── config.yaml           # Main configuration
│   └── env.example          # Environment template
├── interface/                 # User interfaces
│   └── cli.py               # Command-line interface
├── tests/                    # Test files
├── logs/                     # Log files (auto-created)
├── main.py                   # Main entry point
├── requirements.txt          # Dependencies
└── README.md                # This file
```

## 🛠️ Creating a New Agent

### Method 1: Using the CLI (Recommended)

```bash
python interface/cli.py --create my_awesome_agent
```

This creates a new agent from the template with proper structure and configuration.

### Method 2: Manual Creation

1. **Create agent directory**:
   ```bash
   mkdir -p agents/my_agent/features
   ```

2. **Create main.py**:
   ```python
   from core.agent_base import AgentBase
   
   class MyAgent(AgentBase):
       async def initialize(self):
           self.logger.info("Initializing My Agent")
       
       async def execute(self):
           self.logger.info("Executing My Agent logic")
       
       async def cleanup(self):
           self.logger.info("Cleaning up My Agent")
       
       async def handle_message(self, sender, message):
           self.logger.info(f"Received message from {sender}")
   ```

3. **Create config.yaml**:
   ```yaml
   name: "my_agent"
   enabled: true
   execution_interval: 60
   ```

## 📨 Inter-Agent Communication

Agents can communicate through the message bus:

```python
# Send message to specific agent
self.send_message("target_agent", {
    "type": "request",
    "data": "some data"
})

# Broadcast to all agents
self.broadcast_message({
    "type": "announcement",
    "message": "Important update"
})

# Subscribe to topics
self.message_bus.subscribe("topic_name", self.handle_topic)
```

## 🗄️ Shared Context

Agents can share data through the shared context:

```python
# Set data
await self.shared_context.set("key", "value", ttl=3600)

# Get data
value = await self.shared_context.get("key", default="default_value")

# Update atomically
new_value = await self.shared_context.update(
    "counter", 
    lambda x: (x or 0) + 1
)
```

## ⏰ Task Scheduling

Schedule tasks using the built-in scheduler:

```python
# One-time task
self.scheduler.schedule_once(
    "my_task", 
    self.my_function, 
    delay_seconds=300
)

# Recurring task
self.scheduler.schedule_recurring(
    "periodic_task",
    self.periodic_function,
    interval_seconds=3600
)
```

## ⚙️ Configuration

### Framework Configuration (`config/config.yaml`)

```yaml
framework:
  name: "Synapta"
  version: "1.0.0"
  log_level: "INFO"

agents:
  discovery_paths:
    - "agents/"
  auto_start: true
  restart_on_failure: true
```

### Agent Configuration (`agents/my_agent/config.yaml`)

```yaml
name: "my_agent"
enabled: true
execution_interval: 30

# Custom settings
custom_settings:
  api_endpoint: "https://api.example.com"
  max_retries: 3
```

## 🧪 Testing

Run tests using pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core --cov=agents

# Run specific test file
pytest tests/test_agent_interaction.py
```

## 📊 Monitoring and Logging

The framework provides comprehensive logging:

- **Console Output**: Real-time colored output
- **File Logging**: Detailed logs with timestamps
- **Structured Logs**: JSON-formatted logs for parsing

Logs are stored in the `logs/` directory with timestamps.

## 🔒 Security Considerations

- **Environment Variables**: Store sensitive data in `.env` file
- **Agent Isolation**: Each agent runs in its own context
- **Message Validation**: Validate inter-agent messages
- **Resource Limits**: Configure memory and CPU limits

## 🚀 Example Agents

### Bug Hunter Agent
Scans websites for potential bugs and vulnerabilities:
- Web scraping capabilities
- Security scanning
- Report generation

### Client Finder Agent
Searches for potential clients based on criteria:
- Lead generation
- Contact information extraction
- CRM integration

### Example Agent
Template agent showing best practices:
- Proper initialization
- Message handling
- Resource cleanup

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -am 'Add my feature'`
4. Push to branch: `git push origin feature/my-feature`
5. Submit a Pull Request

## 📝 Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Include unit tests for new features
- Update documentation for API changes
- Use type hints where appropriate

## 🐛 Troubleshooting

### Common Issues

1. **Agents not starting**:
   - Check configuration files
   - Verify dependencies are installed
   - Check log files for errors

2. **Message delivery issues**:
   - Ensure target agent is running
   - Check message format
   - Verify message bus is active

3. **Shared context problems**:
   - Check for TTL expiration
   - Verify key names
   - Ensure proper async/await usage

### Debug Mode

Enable debug logging by setting in `config/config.yaml`:
```yaml
framework:
  log_level: "DEBUG"
```

## 📚 API Reference

### AgentBase Class

The base class all agents must inherit from:

```python
class AgentBase(ABC):
    async def initialize(self):
        """Initialize agent resources"""
        
    async def execute(self):
        """Main agent execution logic"""
        
    async def cleanup(self):
        """Cleanup agent resources"""
        
    async def handle_message(self, sender: str, message: Dict[str, Any]):
        """Handle incoming messages"""
```

### MessageBus Methods

```python
def send_message(sender: str, target: str, message: Dict[str, Any])
def broadcast_message(sender: str, message: Dict[str, Any])
def subscribe(topic: str, handler: Callable)
def publish(topic: str, message: Dict[str, Any])
```

### SharedContext Methods

```python
async def set(key: str, value: Any, ttl: Optional[int] = None)
async def get(key: str, default: Any = None) -> Any
async def delete(key: str)
async def update(key: str, updater_func, default: Any = None)
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with modern Python async/await patterns
- Inspired by microservices and actor model architectures
- Thanks to the open-source community for the dependencies

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Check the documentation
- Review existing issues and discussions

---

**Happy Agent Building! 🤖✨**