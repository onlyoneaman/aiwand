"""
AIWand - A simple AI toolkit for text processing using OpenAI and Gemini
"""

__version__ = "0.4.1"
__author__ = "Aman Kumar"

from .core import summarize, chat, generate_text
from .config import (
    setup_user_preferences, 
    show_current_config, 
    AIError,
    AIProvider,
    OpenAIModel,
    GeminiModel,
    ModelType,
    ProviderType,
    make_ai_request,
    DEFAULT_SYSTEM_PROMPT,
    get_ai_client,
    get_current_provider,
    get_model_name
)
from .helper import generate_random_number, generate_uuid

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
    
    # Helper utilities
    "generate_random_number",
    "generate_uuid",
] 