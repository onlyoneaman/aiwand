"""
AIWand - A simple AI toolkit for text processing using OpenAI and Gemini
"""

__version__ = "0.4.9"
__author__ = "Aman Kumar"

from .core import summarize, chat, generate_text
from .extract import extract
from .config import (
    make_ai_request,
    get_ai_client,
    get_current_provider,
    get_model_name
)
from .constants import (
    DEFAULT_SYSTEM_PROMPT
)
from .setup import (
    setup_user_preferences, 
    show_current_config, 
)
from .models import (
    AIError,
    AIProvider,
    OpenAIModel,
    GeminiModel,
    ModelType,
    ProviderType,
    ProviderRegistry,
)
from .helper import (
    generate_random_number, 
    generate_uuid,
    # File and URL helpers (still used internally)
    read_file_content,
    fetch_url_content,
    get_file_extension,
    is_text_file,
)
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
    "extract",
    "make_ai_request",
    
    # Configuration and setup
    "setup_user_preferences",
    "show_current_config",
    "get_ai_client",
    "get_current_provider", 
    "get_model_name",
    
    # AI Models and Providers
    "AIProvider",
    "OpenAIModel", 
    "GeminiModel",
    "ModelType",
    "ProviderType",
    "ProviderRegistry",
    
    # Helper functions
    "generate_random_number",
    "generate_uuid",
    "read_file_content",
    "fetch_url_content",
    "get_file_extension",
    "is_text_file",
    
    # Classification
    "ClassifierResponse",
    "classify_text",
    "create_classifier", 
    "create_binary_classifier",
    "create_quality_classifier",
    
    # Configuration
    "AIError",
    "DEFAULT_SYSTEM_PROMPT",
] 