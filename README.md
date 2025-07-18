# AIWand 🪄

> **The simplest way to unify OpenAI and Gemini APIs** - Drop-in replacement for your existing AI code with automatic provider switching and structured output handling.

[![PyPI version](https://img.shields.io/pypi/v/aiwand.svg)](https://pypi.org/project/aiwand/)
[![Python versions](https://img.shields.io/pypi/pyversions/aiwand.svg)](https://pypi.org/project/aiwand/)
[![License](https://img.shields.io/pypi/l/aiwand.svg)](https://github.com/onlyoneaman/aiwand/blob/main/LICENSE)

## 🎯 **Simple Migration - One Line Change**

**Before** - Direct API calls with provider-specific code:
```python
# OpenAI specific code
content = openai_client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    temperature=0.8,
    top_p=0.9,
    response_format={"type": "json_object"}
)
result = json.loads(content.choices[0].message.content)  # Manual parsing

# OR Gemini specific code
content = gemini_client.chat.completions.create(
    model="gemini-2.0-flash",
    messages=messages,
    temperature=0.8,
    top_p=0.9,
    response_format=SomeSchema
)
result = content.parsed  # Different response handling
```

**After** - Unified AIWand code that works with both:
```python
import aiwand

# Same code works with OpenAI, Gemini, and their structured outputs!
content = aiwand.make_ai_request(
    model="gpt-4o",          # or "gemini-2.0-flash" 
    messages=messages,
    temperature=0.8,
    top_p=0.9,
    response_format=CarouselContent  # Pydantic model - automatic parsing!
)
# 'content' is already your parsed Pydantic object - no post-processing needed! ✨
```

## ✨ **Why AIWand?**

- 🔄 **Drop-in Replacement** - Minimal code changes, maximum benefits
- 🧠 **Smart Provider Detection** - Automatically uses OpenAI or Gemini based on model name
- 🏗️ **Structured Output Magic** - Handles Pydantic models automatically for both providers
- ⚡ **No Post-Processing** - Get parsed objects directly, skip manual JSON handling
- 🎯 **Unified API** - Same code works across different AI providers
- 🔑 **Zero Configuration** - Works with just environment variables
- 📱 **High-Level Functions** - Built-in summarization, chat, and text generation

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

### Core AI Functionality

The `make_ai_request()` function is the heart of AIWand - a unified interface for all AI providers:

```python
import aiwand
from pydantic import BaseModel

# Basic text generation
response = aiwand.make_ai_request(
    messages=[{"role": "user", "content": "Explain quantum computing"}],
    model="gpt-4o"  # Automatically uses OpenAI
)

# Switch providers seamlessly
response = aiwand.make_ai_request(
    messages=[{"role": "user", "content": "Explain quantum computing"}],
    model="gemini-2.0-flash"  # Automatically uses Gemini
)

# Structured output with Pydantic models
class BlogPost(BaseModel):
    title: str
    content: str
    tags: list[str]

blog_post = aiwand.make_ai_request(
    messages=[{"role": "user", "content": "Write a blog post about AI"}],
    model="gpt-4o",
    response_format=BlogPost  # Returns parsed BlogPost object!
)
print(blog_post.title)  # Direct access to structured data

# Custom/preview models with explicit provider
response = aiwand.make_ai_request(
    model="gemini-2.5-flash-preview-05-20",  # New model not in our registry
    provider="gemini",  # Explicit provider specification
    messages=[{"role": "user", "content": "Hello from the future!"}]
)

# Advanced parameters
response = aiwand.make_ai_request(
    messages=[
        {"role": "system", "content": "You are a helpful coding assistant"},
        {"role": "user", "content": "Write a Python function to sort a list"}
    ],
    model="gpt-4o",
    temperature=0.3,  # More focused
    max_tokens=500,
    top_p=0.9
)
```

### High-Level Convenience Functions

For common tasks, use these simplified functions:

```python
import aiwand

# Text summarization
summary = aiwand.summarize("Your long text here...")

# AI chat with conversation history
response = aiwand.chat("What is machine learning?")

# Text generation from prompts
story = aiwand.generate_text("Write a poem about coding")

# Customized summarization
summary = aiwand.summarize(
    text="Your long text...",
    style="bullet-points",  # "concise", "detailed", "bullet-points"
    max_length=50,
    model="gpt-4o"  # Optional: specify model
)

# Chat with conversation history
conversation = []
response1 = aiwand.chat("Hello!", conversation_history=conversation)
conversation.append({"role": "user", "content": "Hello!"})
conversation.append({"role": "assistant", "content": response1})

response2 = aiwand.chat("What did I just say?", conversation_history=conversation)

# Text generation with custom parameters
text = aiwand.generate_text(
    prompt="Write a technical explanation",
    max_tokens=300,
    temperature=0.3  # Lower = more focused, Higher = more creative
)

# Helper utilities for testing and development
random_num = aiwand.generate_random_number(8)  # 8-digit number
unique_id = aiwand.generate_uuid()  # UUID4
```

## 🎯 **Smart Provider Features**

### Automatic Model Detection
```python
# AIWand automatically detects the right provider:
response = aiwand.make_ai_request(model="gpt-4o", ...)        # → OpenAI
response = aiwand.make_ai_request(model="gemini-2.0-flash", ...)  # → Gemini
response = aiwand.make_ai_request(model="o3-mini", ...)       # → OpenAI

# Pattern-based detection for unknown models:
response = aiwand.make_ai_request(model="gemini-experimental-123", ...)  # → Gemini
```

### Explicit Provider Control
```python
# Force a specific provider for custom models:
response = aiwand.make_ai_request(
    model="my-custom-model",
    provider="gemini",  # or AIProvider.GEMINI
    messages=[...]
)

# Works with both string and enum:
from aiwand import AIProvider
response = aiwand.make_ai_request(
    model="any-model",
    provider=AIProvider.OPENAI,
    messages=[...]
)
```

### Structured Output Support
```python
from pydantic import BaseModel

class ProductReview(BaseModel):
    rating: int
    pros: list[str]
    cons: list[str]
    recommendation: bool

# Works identically with both providers:
review = aiwand.make_ai_request(
    model="gpt-4o",  # or "gemini-2.0-flash"
    messages=[{"role": "user", "content": "Review this product: ..."}],
    response_format=ProductReview
)
# No manual JSON parsing needed - returns ProductReview object directly!
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