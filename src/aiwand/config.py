"""
Core AI functionality for AIWand.

This module provides the main AI request functionality, client management,
and provider resolution utilities.
"""

import os
import json
from typing import Dict, Any, Optional, Tuple, List, Union
from openai import OpenAI

from .models import (
    AIProvider,
    ModelType,
    GeminiModel,
    ProviderRegistry,
)
from .preferences import get_preferred_provider_and_model

# Default system prompt
DEFAULT_SYSTEM_PROMPT = "You are AIWand, a helpful AI assistant that provides clear, accurate, and concise responses. You excel at text processing, analysis, and generation tasks."

# Client cache to avoid recreating clients
_client_cache: Dict[AIProvider, OpenAI] = {}


class AIError(Exception):
    """Custom exception for AI-related errors."""
    pass


def get_current_provider() -> Optional[AIProvider]:
    """Get the currently active provider."""
    provider, _ = get_preferred_provider_and_model()
    return provider


def _get_cached_client(provider: AIProvider) -> OpenAI:
    """Get or create a cached client for the provider."""
    if provider not in _client_cache:
        # Get provider configuration from registry
        env_var = ProviderRegistry.get_env_var(provider)
        base_url = ProviderRegistry.get_base_url(provider)
        
        if not env_var:
            raise AIError(f"Unsupported provider: {provider}")
        
        api_key = os.getenv(env_var)
        if not api_key:
            raise AIError(f"{provider.value.title()} API key not found. Please set {env_var} environment variable.")
        
        # Create client with provider-specific configuration
        if base_url:
            _client_cache[provider] = OpenAI(api_key=api_key, base_url=base_url)
        else:
            _client_cache[provider] = OpenAI(api_key=api_key)
    
    return _client_cache[provider]


def _resolve_provider_model_client(
    model: Optional[ModelType] = None, 
    provider: Optional[Union[AIProvider, str]] = None
) -> Tuple[AIProvider, str, OpenAI]:
    """
    Resolve provider, model name, and client based on input model, provider, or preferences.
    
    Args:
        model: Optional model to use for inference
        provider: Optional provider to use explicitly (AIProvider enum or string)
        
    Returns:
        Tuple of (provider, model_name, client)
        
    Raises:
        AIError: When no provider is available
    """
    # Handle explicit provider specification
    if provider is not None:
        # Convert string to AIProvider enum if needed
        if isinstance(provider, str):
            try:
                provider_enum = AIProvider(provider.lower())
            except ValueError:
                raise AIError(f"Unknown provider: {provider}. Supported providers: {[p.value for p in AIProvider]}")
        else:
            provider_enum = provider
        
        # Use explicit provider with provided model or get default model for provider
        if model is not None:
            return provider_enum, str(model), _get_cached_client(provider_enum)
        else:
            default_model = ProviderRegistry.get_default_model(provider_enum)
            if not default_model:
                raise AIError(f"No default model available for provider: {provider_enum}")
            return provider_enum, str(default_model), _get_cached_client(provider_enum)
    
    # No explicit provider, try to infer from model
    if model is not None:
        # Try to infer provider from model (now includes pattern matching)
        inferred_provider = ProviderRegistry.infer_provider_from_model(model)
        if inferred_provider is not None:
            return inferred_provider, str(model), _get_cached_client(inferred_provider)
        else:
            # Model provided but can't infer provider, use preferences with provided model
            fallback_provider, _ = get_preferred_provider_and_model()
            if not fallback_provider:
                raise AIError("No AI provider available. Please set up your API keys.")
            return fallback_provider, str(model), _get_cached_client(fallback_provider)
    else:
        # No model or provider provided, use current preferences
        pref_provider, preferred_model = get_preferred_provider_and_model()
        if not pref_provider or not preferred_model:
            raise AIError("No AI provider available. Please set up your API keys and run 'aiwand setup'.")
        return pref_provider, str(preferred_model), _get_cached_client(pref_provider)


def make_ai_request(
    messages: Optional[List[Dict[str, str]]] = None,
    max_tokens: Optional[int] = None,
    temperature: float = 0.7,
    top_p: float = 1.0,
    model: Optional[ModelType] = GeminiModel.GEMINI_2_0_FLASH_LITE.value,
    provider: Optional[Union[AIProvider, str]] = None,
    response_format: Optional[Dict[str, Any]] = None,
    system_prompt: Optional[str] = None,
    user_prompt: Optional[str] = None,
    additional_system_instructions: Optional[str] = None
) -> str:
    """
    Unified wrapper for AI API calls that handles provider differences.
    
    Args:
        messages: Optional list of message dictionaries with 'role' and 'content'.
                 If None or empty, a default user message will be added.
        max_tokens: Maximum tokens to generate
        temperature: Response creativity (0.0 to 1.0)
        top_p: Nucleus sampling parameter
        model: Specific model to use (auto-selected if not provided)
        provider: Optional provider to use explicitly (AIProvider enum or string like 'openai', 'gemini').
                 Overrides model-based inference when specified.
        response_format: Response format specification
        system_prompt: Optional system prompt to add at the beginning (uses default if None).
                      Can be used alone without messages for simple generation.
        user_prompt: Optional user message to add at the end of the messages list.
                     Can be used in parallel with or without existing messages.
        additional_system_instructions: Optional additional instructions to append to the system prompt.
                                       If provided, will be added to the end of the system message with proper spacing.
    Returns:
        str: The AI response content
        
    Raises:
        AIError: When the API call fails
    """
    try:
        # Resolve provider, model, and client
        current_provider, model_name, client = _resolve_provider_model_client(model, provider)
        
        # Handle case where messages is None or empty
        if messages is None:
            messages = []
        
        # Prepare messages with system prompt
        final_messages = messages.copy()
        
        # Check if messages already contain a system message
        has_system_message = any(msg.get("role") == "system" for msg in final_messages)
        
        # Add system prompt only if:
        # 1. No existing system message in messages
        # 2. Either system_prompt was explicitly provided (including empty string) or we should use default
        if not has_system_message:
            if system_prompt is not None:
                # Use provided system_prompt (even if empty string)
                final_messages.insert(0, {"role": "system", "content": system_prompt})
            else:
                # Use default system prompt only when system_prompt is None
                final_messages.insert(0, {"role": "system", "content": DEFAULT_SYSTEM_PROMPT})

        # Append additional system instructions if provided
        if additional_system_instructions is not None:
            # Find the system message and append additional instructions
            for msg in final_messages:
                if msg.get("role") == "system":
                    current_content = msg["content"]
                    # Add proper spacing if current content exists and doesn't end with whitespace
                    if current_content:
                        msg["content"] = f"{current_content}\n\n{additional_system_instructions}"
                    break

        if user_prompt is not None:
            final_messages.append({"role": "user", "content": user_prompt})
        
        # If we only have a system message (no user messages), add a default user message
        # This allows using system_prompt alone as a kind of generation prompt
        has_user_message = any(msg.get("role") in ["user", "assistant"] for msg in final_messages)
        if not has_user_message:
            final_messages.append({"role": "user", "content": "Please respond based on your instructions."})
        
        # Prepare common parameters
        params = {
            "model": model_name,
            "messages": final_messages,
            "temperature": temperature,
            "top_p": top_p
        }
        
        if max_tokens:
            params["max_tokens"] = max_tokens
        
        if response_format:
            params["response_format"] = response_format

        # Choose API call method based on provider and features
        if current_provider == AIProvider.GEMINI and response_format:
            # For Gemini with structured output, use beta endpoint
            response = client.beta.chat.completions.parse(**params)
        else:
            # Standard chat completions for all other cases
            response = client.chat.completions.create(**params)
        
        content = response.choices[0].message.content.strip()
        if response_format:
            if isinstance(content, dict):
                parsed = content
            else:
                parsed = json.loads(content)
            return response_format(**parsed)
        return content
    
    except AIError as e:
        raise AIError(str(e))
    except Exception as e:
        raise AIError(f"AI request failed: {str(e)}")


def get_ai_client() -> OpenAI:
    """
    Get configured AI client with smart provider selection.
    
    Returns:
        OpenAI: Configured client for the selected provider
        
    Raises:
        AIError: When no API provider is available
    """
    provider, _ = get_preferred_provider_and_model()
    
    if not provider:
        available = ProviderRegistry.get_available_providers()
        if not any(available.values()):
            raise AIError(
                "No API keys found. Please set OPENAI_API_KEY or GEMINI_API_KEY environment variable, "
                "or run 'aiwand setup' to configure your preferences."
            )
    
    return _get_cached_client(provider)


def get_model_name() -> str:
    """
    Get the model name for the current provider.
    
    Returns:
        str: Model name to use
        
    Raises:
        AIError: When no provider is available
    """
    provider, model = get_preferred_provider_and_model()
    
    if not provider or not model:
        raise AIError(
            "No AI provider available. Please set up your API keys and run 'aiwand setup' "
            "to configure your preferences."
        )
    
    return str(model) 