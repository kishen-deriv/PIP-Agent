# Memory-Enabled Agent

This directory contains an implementation of a memory-enabled agent that can maintain conversation history across multiple sessions.

## Features

- Persistent conversation memory using file-based storage
- Support for multiple conversation threads
- Command-line interface for interactive chat
- Thread management (create, switch, clear, list)

## Files

- `new_agent.py`: Core implementation of the memory-enabled agent
- `chat_cli.py`: Command-line interface for interacting with the agent
- `agent.py`: Original agent implementation (for reference)

## Usage

### Basic Usage

```bash
# Start a chat session with the default thread
python src/chat_cli.py

# Start a chat session with a specific thread
python src/chat_cli.py --thread work

# Clear the conversation history before starting
python src/chat_cli.py --clear

# List all available conversation threads
python src/chat_cli.py --list
```

### CLI Commands

During a chat session, you can use the following commands:

- `!help`: Show available commands
- `!clear`: Clear the current conversation history
- `!list`: List all messages in the current thread
- `!switch NAME`: Switch to a different conversation thread
- `exit`, `quit`: Exit the application

### Programmatic Usage

```python
from src.new_agent import chat_with_memory

# Chat with the agent using the default thread
response = chat_with_memory("Hello, how are you?")
print(response)

# Chat with the agent using a specific thread
response = chat_with_memory("What's the weather like?", thread_id="weather")
print(response)
```

## How It Works

The agent uses a file-based storage system to maintain conversation history. Each conversation is stored in a JSON file with the following structure:

```json
{
  "thread-id": {
    "messages": [
      {"role": "human", "content": "Hello, how are you?"},
      {"role": "ai", "content": "I'm doing well, thank you for asking!"}
    ]
  }
}
```

When a new message is received, the agent:

1. Loads the conversation history for the specified thread
2. Adds the new message to the history
3. Converts the history to LangChain message format
4. Invokes the agent with the conversation history
5. Adds the agent's response to the history
6. Saves the updated history

This approach allows the agent to maintain context across multiple interactions, even if the application is restarted.
