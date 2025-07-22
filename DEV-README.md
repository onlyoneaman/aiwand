# AIWand Developer Reference 🪄

Quick reference guide for all AIWand functionalities.

## 🚀 Core AI Functions

### `aiwand.call_ai()`
**Unified AI request function - works with OpenAI & Gemini**

```python
aiwand.call_ai(
    messages: Optional[List[Dict[str, str]]] = None,
    max_output_tokens: Optional[int] = None,
    temperature: float = 0.7,
    top_p: float = 1.0,
    model: Optional[ModelType] = None,
    provider: Optional[Union[AIProvider, str]] = None,
    response_format: Optional[Dict[str, Any]] = None,
    system_prompt: Optional[str] = None,
    user_prompt: Optional[str] = None,
    additional_system_instructions: Optional[str] = None,
    images: Optional[List[Union[str, Path, bytes]]] = None
) -> str
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `messages` | `List[Dict[str, str]]` | `None` | Chat messages with 'role' and 'content' |
| `max_output_tokens` | `int` | `None` | Maximum tokens to generate |
| `temperature` | `float` | `0.7` | Creativity level (0.0-1.0) |
| `top_p` | `float` | `1.0` | Nucleus sampling parameter |
| `model` | `ModelType` | `None` | Specific model (auto-detected provider) |
| `provider` | `AIProvider/str` | `None` | Force specific provider ("openai"/"gemini") |
| `response_format` | `Dict/Pydantic` | `None` | Structured output format |
| `system_prompt` | `str` | `None` | System prompt (uses default if None) |
| `user_prompt` | `str` | `None` | User message to append to messages list |
| `additional_system_instructions` | `str` | `None` | Additional system instructions to append to the system prompt |
| `images` | `List[Union[str, Path, bytes]]` | `None` | List of images to add to the messages list |

**Returns:** `str` or parsed Pydantic object (if `response_format` provided)

**Examples:**
```python
# Basic usage
response = aiwand.call_ai(
    messages=[{"role": "user", "content": "Hello!"}],
    model="gpt-4o"
)

# With structured output
class BlogPost(BaseModel):
    title: str
    content: str

post = aiwand.call_ai(
    messages=[{"role": "user", "content": "Write a blog post"}],
    model="gemini-2.0-flash",
    response_format=BlogPost
)  # Returns BlogPost object

# Explicit provider
response = aiwand.call_ai(
    model="custom-model",
    provider="gemini",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Using user_prompt to extend conversation
conversation = [
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language..."}
]
response = aiwand.call_ai(
    messages=conversation,
    user_prompt="How do I install it?",  # Appends as new user message
    system_prompt="You are a helpful programming tutor."
)
```

---

## 📝 High-Level Functions

### `aiwand.summarize()`
```python
aiwand.summarize(
    text: str,
    max_length: Optional[int] = None,
    style: str = "concise",
    model: Optional[str] = None
) -> str
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | Required | Text to summarize |
| `max_length` | `int` | `None` | Maximum summary length |
| `style` | `str` | `"concise"` | "concise", "detailed", "bullet-points" |
| `model` | `str` | `None` | Specific model to use |

**Returns:** `str` - Summary text

### `aiwand.chat()`
```python
aiwand.chat(
    message: str,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    model: Optional[str] = None,
    temperature: float = 0.7
) -> str
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `message` | `str` | Required | User message |
| `conversation_history` | `List[Dict]` | `None` | Previous conversation |
| `model` | `str` | `None` | Specific model to use |
| `temperature` | `float` | `0.7` | Response creativity |

**Returns:** `str` - AI response

### `aiwand.generate_text()`
```python
aiwand.generate_text(
    prompt: str,
    max_output_tokens: int = None,
    temperature: float = 0.7,
    model: Optional[str] = None
) -> str
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | `str` | Required | Generation prompt |
| `max_output_tokens` | `int` | `None` | Maximum tokens |
| `temperature` | `float` | `0.7` | Creativity level |
| `model` | `str` | `None` | Specific model to use |

**Returns:** `str` - Generated text

---

## ⚙️ Configuration Functions

### `aiwand.setup_user_preferences()`
```python
aiwand.setup_user_preferences() -> None
```
Interactive setup wizard for provider/model preferences.

### `aiwand.show_current_config()`
```python
aiwand.show_current_config() -> None
```
Display current configuration and available providers.

### `aiwand.get_ai_client()`
```python
aiwand.get_ai_client() -> OpenAI
```
**Returns:** `OpenAI` - Configured client for current provider

### `aiwand.get_current_provider()`
```python
aiwand.get_current_provider() -> Optional[AIProvider]
```
**Returns:** `AIProvider` - Currently active provider or None

### `aiwand.get_model_name()`
```python
aiwand.get_model_name() -> str
```
**Returns:** `str` - Current model name

---

## 🔧 Utility Functions

### `aiwand.generate_random_number()`
```python
aiwand.generate_random_number(length: int = 8) -> str
```
**Returns:** `str` - Random number string

### `aiwand.generate_uuid()`
```python
aiwand.generate_uuid() -> str
```
**Returns:** `str` - UUID4 string

---

## 🎯 Classifier Functions

### `aiwand.classify_text()`
**Simple text classification and grading with custom criteria**

```python
aiwand.classify_text(
    question: str,
    answer: str,
    expected: str = "",
    prompt_template: str = "",
    choice_scores: Optional[Dict[str, float]] = None,
    use_reasoning: bool = True,
    model: Optional[ModelType] = None,
    provider: Optional[Union[AIProvider, str]] = None
) -> ClassifierResponse
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `question` | `str` | Required | The question, prompt, or context |
| `answer` | `str` | Required | The response to be evaluated |
| `expected` | `str` | `""` | Expected/reference response (optional) |
| `prompt_template` | `str` | `""` | Custom prompt with {question}, {answer}, {expected} |
| `choice_scores` | `Dict[str, float]` | `{"CORRECT": 1.0, "INCORRECT": 0.0}` | Choice-to-score mapping |
| `use_reasoning` | `bool` | `True` | Include step-by-step reasoning |
| `model` | `ModelType` | `None` | Specific model to use |
| `provider` | `AIProvider/str` | `None` | Specific provider to use |

**Returns:** `ClassifierResponse` with score, choice, reasoning, and metadata

### `aiwand.create_classifier()`
**Create reusable classifier with predefined settings**

```python
aiwand.create_classifier(
    prompt_template: str,
    choice_scores: Dict[str, float],
    use_reasoning: bool = True,
    model: Optional[ModelType] = None,
    provider: Optional[Union[AIProvider, str]] = None
) -> callable
```

**Returns:** Classifier function that can be called with (input_text, output_text, expected_text)

### `aiwand.create_binary_classifier()`
**Create simple correct/incorrect classifier**

```python
aiwand.create_binary_classifier(
    criteria: str = "correctness",
    model: Optional[ModelType] = None,
    provider: Optional[Union[AIProvider, str]] = None
) -> callable
```

### `aiwand.create_quality_classifier()`
**Create A-F quality grading classifier**

```python
aiwand.create_quality_classifier(
    model: Optional[ModelType] = None,
    provider: Optional[Union[AIProvider, str]] = None
) -> callable
```

### `ClassifierResponse`
```python
class ClassifierResponse(BaseModel):
    score: float          # Numerical score
    choice: str           # Selected choice/grade
    reasoning: str        # Step-by-step reasoning
    metadata: Dict        # Additional information
```

**Examples:**
```python
# Simple binary classification
result = aiwand.classify_text(
    question="What is 2+2?",
    answer="4",
    expected="4",
    choice_scores={"CORRECT": 1.0, "INCORRECT": 0.0}
)

# Custom grading scale
result = aiwand.classify_text(
    question="Write a haiku",
    answer="Roses are red...",
    choice_scores={"A": 1.0, "B": 0.8, "C": 0.6, "D": 0.4, "F": 0.0}
)

# Reusable classifier
math_grader = aiwand.create_classifier(
    prompt_template="Grade this math answer: {question} -> {answer}",
    choice_scores={"CORRECT": 1.0, "PARTIAL": 0.5, "WRONG": 0.0}
)
result = math_grader(question="2+2", answer="4", expected="4")

# Predefined classifiers
checker = aiwand.create_binary_classifier(criteria="relevance")
quality = aiwand.create_quality_classifier()
```

---

## 🎯 Provider & Model Enums

### `AIProvider`
```python
from aiwand import AIProvider

AIProvider.OPENAI    # "openai"
AIProvider.GEMINI    # "gemini"
```

### `OpenAIModel`
```python
from aiwand import OpenAIModel

# Latest models
OpenAIModel.O3_MINI          # "o3-mini"
OpenAIModel.O3               # "o3"
OpenAIModel.GPT_4O           # "gpt-4o"
OpenAIModel.GPT_4O_MINI      # "gpt-4o-mini"

# Legacy models
OpenAIModel.GPT_4            # "gpt-4"
OpenAIModel.GPT_3_5_TURBO    # "gpt-3.5-turbo"
```

### `GeminiModel`
```python
from aiwand import GeminiModel

# Latest models
GeminiModel.GEMINI_2_0_FLASH     # "gemini-2.0-flash"
GeminiModel.GEMINI_2_0_PRO       # "gemini-2.0-pro"
GeminiModel.GEMINI_1_5_PRO       # "gemini-1.5-pro"
```

---

## 📊 Provider Registry

### `ProviderRegistry`
```python
from aiwand import ProviderRegistry

# Get all providers
ProviderRegistry.get_all_providers() -> List[AIProvider]

# Get models for provider
ProviderRegistry.get_models_for_provider(provider) -> List[BaseModel]

# Infer provider from model
ProviderRegistry.infer_provider_from_model(model) -> Optional[AIProvider]

# Check provider availability
ProviderRegistry.is_provider_available(provider) -> bool
```

---

## ❌ Error Handling

### `AIError`
```python
from aiwand import AIError

try:
    response = aiwand.call_ai(...)
except AIError as e:
    print(f"AI error: {e}")
```

---

## 🚀 Quick Start Examples

```python
import aiwand
from pydantic import BaseModel

# Simple chat
response = aiwand.call_ai(
    messages=[{"role": "user", "content": "Hello!"}],
    model="gpt-4o"
)

# Structured output
class Recipe(BaseModel):
    name: str
    ingredients: list[str]
    steps: list[str]

recipe = aiwand.call_ai(
    messages=[{"role": "user", "content": "Give me a pasta recipe"}],
    model="gemini-2.0-flash",
    response_format=Recipe
)

# Provider control
response = aiwand.call_ai(
    model="custom-model",
    provider="gemini",
    messages=[{"role": "user", "content": "Hello!"}]
)

# High-level functions
summary = aiwand.summarize("Long text...", style="bullet-points")
chat_response = aiwand.chat("What is AI?")
story = aiwand.generate_text("Write a short story about robots")
```

---

## 🔑 Environment Variables

```bash
OPENAI_API_KEY=your_openai_key       # Optional
GEMINI_API_KEY=your_gemini_key       # Optional
AI_DEFAULT_PROVIDER=openai           # Optional: openai|gemini
```

---

## 📦 Installation

```bash
pip install aiwand
```

**Current Version:** 0.4.5 