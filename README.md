# AIWand 🪄

> **One API to rule them all** - Unified OpenAI and Gemini interface with automatic provider switching and structured data extraction from anywhere.

[![PyPI version](https://img.shields.io/pypi/v/aiwand.svg)](https://pypi.org/project/aiwand/)
[![Python versions](https://img.shields.io/pypi/pyversions/aiwand.svg)](https://pypi.org/project/aiwand/)
[![License](https://img.shields.io/pypi/l/aiwand.svg)](https://github.com/onlyoneaman/aiwand/blob/main/LICENSE)
[![Coverage Status](https://img.shields.io/badge/coverage-100%25-success)](https://github.com/onlyoneaman/aiwand/actions?query=workflow%3ACI)
[![Downloads](https://pepy.tech/badge/aiwand)](https://pepy.tech/project/aiwand)
[![Downloads](https://pepy.tech/badge/aiwand/month)](https://pepy.tech/project/aiwand/month)
[![Downloads](https://pepy.tech/badge/aiwand/week)](https://pepy.tech/project/aiwand/week)

## 🚀 **Stop Wrestling with AI APIs**

**Before:** Provider chaos, manual parsing, complex setup
```python
# Different APIs, manual JSON parsing, provider-specific code
import openai, google.generativeai as genai
response = openai.chat.completions.create(...)
result = json.loads(response.choices[0].message.content)  # 😫
```

**After:** One API, automatic everything
```python
import aiwand
from pydantic import BaseModel

# 🎯 Universal AI calls - any model, any provider
response = aiwand.call_ai(
    model="gpt-4o",              # or "gemini-2.0-flash" 
    messages=[{"role": "user", "content": "Explain quantum computing"}]
)

# ✨ Structured output magic - no JSON wrestling
class BlogPost(BaseModel):
    title: str
    content: str
    tags: list[str]

blog = aiwand.call_ai(
    model="gemini-2.0-flash",
    messages=[{"role": "user", "content": "Write a blog about AI"}],
    response_format=BlogPost    # Returns BlogPost object directly!
)
print(blog.title)  # Just works ✨

# 🧠 Smart extraction from anywhere
contact = aiwand.extract(content="John Doe, john@example.com, (555) 123-4567")
webpage_data = aiwand.extract(links=["https://company.com/about"])
document_data = aiwand.extract(document_links=["resume.pdf", "report.docx"])
image_data = aiwand.extract(images=["chart.png", "diagram.jpg"])

# Mix all sources together
mixed_data = aiwand.extract(
    content="Meeting notes: call John tomorrow",
    links=["https://company.com/team"],
    document_links=["business_card.pdf"],
    images=["photo.jpg"]
)
```

## 🔧 Installation & Setup

```bash
pip install aiwand

# Set your API key (either works, or both for fallback)
export OPENAI_API_KEY="your-key"     
export GEMINI_API_KEY="your-key"     
```

## 💡 Core Features

### **`call_ai`** - Universal AI Interface
Drop-in replacement for OpenAI and Gemini with automatic provider detection:

```python
# Same code, any provider
responses = []
for model in ["gpt-4o", "gemini-2.0-flash", "o3-mini"]:
    response = aiwand.call_ai(
        model=model,  # Auto-detects provider
        messages=[{"role": "user", "content": f"What makes {model} special?"}]
    )
    responses.append(response)
```

### **`extract`** - Smart Data Extraction  
Extract structured data from text, web links, documents, and images:

```python
from pydantic import BaseModel

class CompanyInfo(BaseModel):
    name: str
    founded: int
    employees: int
    technologies: list[str]

# Extract from all source types
company = aiwand.extract(
    content="Research notes about tech companies...", 
    links=["https://company.com/about"],           # Web pages
    document_links=["annual_report.pdf"],          # Documents  
    images=["company_chart.png", "logo.jpg"],      # Images
    response_format=CompanyInfo  # Get typed object back
)

print(f"{company.name} founded in {company.founded}")  # Direct access
```

## ⚡ Quick Examples

```python
import aiwand

# Instant AI calls
summary = aiwand.summarize("Long article...", style="bullet-points")
response = aiwand.chat("What is machine learning?")
story = aiwand.generate_text("Write a haiku about coding")

# Smart classification  
grader = aiwand.create_binary_classifier(criteria="technical accuracy")
result = grader(question="What is 2+2?", answer="4", expected="4")
print(f"Accuracy: {result.score}/5")
```

## 🎨 CLI Magic

```bash
# Quick chat
aiwand "Explain quantum computing simply"

# Extract from anything
aiwand extract "Dr. Sarah Johnson, sarah@lab.com" --json
aiwand extract --links https://example.com --document-links resume.pdf --images chart.png

# Built-in functions
aiwand summarize "Long text..." --style concise
aiwand chat "Hello there!"
```

## ✨ Why Choose AIWand?

| 🔄 **Provider Agnostic** | Same code, OpenAI or Gemini |
|---|---|
| 🏗️ **Structured Output** | Pydantic objects, no JSON parsing |
| 🧠 **Smart Detection** | Automatic provider selection |
| 📄 **Universal Extraction** | Text, web links, documents, images |
| ⚡ **Zero Setup** | Just add API keys |
| 🎯 **Drop-in Ready** | Minimal code changes |

## 📚 Documentation

- **[API Reference](docs/api-reference.md)** - Complete function docs
- **[CLI Guide](docs/cli.md)** - Command line usage  
- **[Installation](docs/installation.md)** - Setup details
- **[Development](docs/development.md)** - Contributing guide

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

⭐ **Star this repo if AIWand makes your AI development easier!**

**Made with ❤️ by [Aman Kumar](https://x.com/onlyoneaman)** 