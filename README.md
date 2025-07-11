# AIWand 🪄

> A simple and elegant Python package for AI-powered text processing using OpenAI and Google Gemini APIs.

[![PyPI version](https://img.shields.io/pypi/v/aiwand.svg)](https://pypi.org/project/aiwand/)
[![Python versions](https://img.shields.io/pypi/pyversions/aiwand.svg)](https://pypi.org/project/aiwand/)
[![License](https://img.shields.io/pypi/l/aiwand.svg)](https://github.com/onlyoneaman/aiwand/blob/main/LICENSE)

## ✨ Features

- **Smart Provider Selection** - Automatically uses OpenAI or Gemini based on available keys
- **Text Summarization** - Create concise, detailed, or bullet-point summaries  
- **AI Chat** - Have conversations with context history
- **Text Generation** - Generate content from prompts
- **Helper Utilities** - Random number and UUID generation
- **Zero Configuration** - Works with just environment variables
- **CLI Interface** - Optional command line usage

## 🚀 Quick Start

### Installation

```bash
pip install aiwand
```

### Configuration

Set your API keys as environment variables:

```bash
# Option 1: OpenAI only
export OPENAI_API_KEY="your-openai-key"

# Option 2: Gemini only  
export GEMINI_API_KEY="your-gemini-key"

# Option 3: Both (set preference)
export OPENAI_API_KEY="your-openai-key"
export GEMINI_API_KEY="your-gemini-key"
export AI_DEFAULT_PROVIDER="openai"  # or "gemini"
```

Or create a `.env` file in your project:
```env
OPENAI_API_KEY=your-openai-key
GEMINI_API_KEY=your-gemini-key
AI_DEFAULT_PROVIDER=openai
```

### Basic Usage

```python
import aiwand

# Summarize text
summary = aiwand.summarize("Your long text here...")

# Chat with AI  
response = aiwand.chat("What is machine learning?")

# Generate text
story = aiwand.generate_text("Write a poem about coding")

# Generate random number and UUID
random_num = aiwand.generate_random_number(8)  # 8-digit number
unique_id = aiwand.generate_uuid()  # UUID4
```

### Advanced Usage

```python
import aiwand

# Customized summarization
summary = aiwand.summarize(
    text="Your long text...",
    style="bullet-points",  # "concise", "detailed", "bullet-points"
    max_length=50,
    model="gpt-4"  # Optional: specify model
)

# Chat with conversation history
conversation = []
response1 = aiwand.chat("Hello!", conversation_history=conversation)
conversation.append({"role": "user", "content": "Hello!"})
conversation.append({"role": "assistant", "content": response1})

response2 = aiwand.chat("What did I just say?", conversation_history=conversation)

# Generate text with custom parameters
text = aiwand.generate_text(
    prompt="Write a technical explanation",
    max_tokens=300,
    temperature=0.3  # Lower = more focused, Higher = more creative
)

# Helper utilities for testing and development
test_id = aiwand.generate_random_number(6)  # 6-digit number
session_id = aiwand.generate_uuid()  # UUID4
user_code = aiwand.generate_random_number(4)  # 4-digit code
transaction_uuid = aiwand.generate_uuid(uppercase=True)  # Uppercase UUID
```

### Configuration Management

```python
import aiwand

# Show current configuration
aiwand.show_current_config()

# Interactive setup (optional)
aiwand.setup_user_preferences()
```

### Error Handling

```python
import aiwand

try:
    summary = aiwand.summarize("Some text")
except aiwand.AIError as e:
    print(f"AI service error: {e}")
except ValueError as e:
    print(f"Input error: {e}")
```

## 🔧 CLI Usage (Optional)

```bash
# Direct prompts (easiest way!)
aiwand "Ten fun names for a pet pelican"
aiwand "Explain quantum computing in simple terms" 

# Specific commands
aiwand summarize "Your text here" --style bullet-points
aiwand chat "What is machine learning?"
aiwand generate "Write a story about AI"

# Helper utilities
aiwand helper random --length 8        # Generate 8-digit random number
aiwand helper uuid --uppercase         # Generate uppercase UUID

# Setup preferences
aiwand setup
aiwand config
```

## 📚 Documentation

- **[API Reference](docs/api-reference.md)** - Complete function documentation  
- **[CLI Reference](docs/cli.md)** - Command line usage
- **[Installation Guide](docs/installation.md)** - Detailed setup instructions
- **[Virtual Environment Guide](docs/venv-guide.md)** - Best practices for Python environments

## 🛠️ Contributing

We welcome contributions from both AI assistants and human developers! Please see our comprehensive contributing guide:

- **[Contributing Guide](CONTRIBUTING.md)** - Standards, workflows, and best practices
- **[Development Guide](docs/development.md)** - Technical details and advanced topics

Whether you're an AI assistant helping users or a human developer, these guides ensure consistency and quality across all contributions.

## 🤝 Connect

- **GitHub**: [github.com/onlyoneaman/aiwand](https://github.com/onlyoneaman/aiwand)
- **PyPI**: [pypi.org/project/aiwand](https://pypi.org/project/aiwand/)
- **X (Twitter)**: [@onlyoneaman](https://x.com/onlyoneaman)

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Made with ❤️ by [Aman Kumar](https://x.com/onlyoneaman)** 