"""
AIWand - A simple AI toolkit for text processing using OpenAI and Gemini
"""

__version__ = "0.4.7"
__author__ = "Aman Kumar"

from .core import summarize, chat, generate_text
from .config import (
    AIError,
    make_ai_request,
    DEFAULT_SYSTEM_PROMPT,
    get_ai_client,
    get_current_provider,
    get_model_name
)
from .setup import (
    setup_user_preferences, 
    show_current_config, 
)
from .models import (
    AIProvider,
    OpenAIModel,
    GeminiModel,
    ModelType,
    ProviderType,
    ProviderRegistry,
)
from .helper import generate_random_number, generate_uuid
from .classifier import (
    ClassifierResponse,
    classify_text,
    create_classifier,
    create_binary_classifier,
    create_quality_classifier,
)

__all__ = [
    # Core AI functions
    "summarize",
    "chat", 
    "generate_text",
    "make_ai_request",
    
    # Configuration and setup
    "setup_user_preferences",
    "show_current_config",
    "get_ai_client",
    "get_current_provider", 
    "get_model_name",
    "DEFAULT_SYSTEM_PROMPT",
    
    # Types and enums
    "AIError",
    "AIProvider",
    "OpenAIModel", 
    "GeminiModel",
    "ModelType",
    "ProviderType",
    "ProviderRegistry",
    
    # Helper utilities
    "generate_random_number",
    "generate_uuid",
    
    # Classifier functionality
    "ClassifierResponse",
    "classify_text",
    "create_classifier",
    "create_binary_classifier",
    "create_quality_classifier",
] 