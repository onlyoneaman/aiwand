"""
Configuration management for AIWand.

This module handles API client setup, provider selection, and user preferences.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
from openai import OpenAI


class AIError(Exception):
    """Custom exception for AI-related errors."""
    pass


def get_config_dir() -> Path:
    """Get the AIWand configuration directory."""
    config_dir = Path.home() / ".aiwand"
    config_dir.mkdir(exist_ok=True)
    return config_dir


def get_config_file() -> Path:
    """Get the path to the configuration file."""
    return get_config_dir() / "config.json"


def load_user_preferences() -> Dict[str, Any]:
    """Load user preferences from config file."""
    config_file = get_config_file()
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # If config is corrupted, return empty dict
            pass
    return {}


def save_user_preferences(preferences: Dict[str, Any]) -> None:
    """Save user preferences to config file."""
    config_file = get_config_file()
    try:
        with open(config_file, 'w') as f:
            json.dump(preferences, f, indent=2)
    except IOError as e:
        raise AIError(f"Failed to save preferences: {e}")


def get_available_providers() -> Dict[str, bool]:
    """Check which API providers are available based on environment variables."""
    return {
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "gemini": bool(os.getenv("GEMINI_API_KEY"))
    }


def get_supported_models() -> Dict[str, list]:
    """Get supported models for each provider."""
    return {
        "openai": [
            # Latest reasoning models (best performance)
            "o3-mini",
            "o3",
            "o1",
            "o1-mini",
            # Latest GPT-4.1 series (huge context, best for coding)
            "gpt-4.1",
            "gpt-4.1-mini",
            # Latest GPT-4o series (multimodal, fast)
            "gpt-4o",
            "gpt-4o-mini",
            # Legacy but still capable
            "gpt-4-turbo",
            "gpt-4",
            "gpt-3.5-turbo"
        ],
        "gemini": [
            # Latest Gemini 2.5 series (best performance)
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
            # Gemini 2.0 series (current stable)
            "gemini-2.0-flash-exp",
            "gemini-2.0-flash",
            "gemini-2.0-pro",
            # Legacy but still capable
            "gemini-1.5-flash",
            "gemini-1.5-pro"
        ]
    }


def get_default_models() -> Dict[str, str]:
    """Get default models for each provider."""
    return {
        "openai": "gpt-4o",  # Flagship multimodal model, excellent performance
        "gemini": "gemini-2.0-flash"  # Stable, fast, and capable model
    }


def get_preferred_provider_and_model() -> Tuple[Optional[str], Optional[str]]:
    """Get user's preferred provider and model from preferences."""
    preferences = load_user_preferences()
    available_providers = get_available_providers()
    
    # Get preferred provider
    preferred_provider = preferences.get("default_provider")
    
    # If preferred provider is not available, fall back to available ones
    if not preferred_provider or not available_providers.get(preferred_provider):
        # Check environment variable
        env_provider = os.getenv("AI_DEFAULT_PROVIDER", "").lower()
        if env_provider in available_providers and available_providers[env_provider]:
            preferred_provider = env_provider
        else:
            # Use first available provider
            for provider, available in available_providers.items():
                if available:
                    preferred_provider = provider
                    break
    
    if not preferred_provider:
        return None, None
    
    # Get preferred model for the provider
    preferred_model = preferences.get("models", {}).get(preferred_provider)
    if not preferred_model:
        preferred_model = get_default_models().get(preferred_provider)
    
    return preferred_provider, preferred_model


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
        available = get_available_providers()
        if not any(available.values()):
            raise AIError(
                "No API keys found. Please set OPENAI_API_KEY or GEMINI_API_KEY environment variable, "
                "or run 'aiwand setup' to configure your preferences."
            )
    
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise AIError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        return OpenAI(api_key=api_key)
    
    elif provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise AIError("Gemini API key not found. Please set GEMINI_API_KEY environment variable.")
        return OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
    
    else:
        raise AIError(f"Unsupported provider: {provider}")


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
    
    return model


def setup_user_preferences() -> None:
    """Interactive setup for user preferences."""
    print("🪄 AIWand Setup")
    print("=" * 40)
    
    available_providers = get_available_providers()
    available_list = [p for p, available in available_providers.items() if available]
    
    if not available_list:
        print("❌ No API keys found!")
        print("\nPlease set up your API keys first:")
        print("  OPENAI_API_KEY=your_openai_key")
        print("  GEMINI_API_KEY=your_gemini_key")
        print("\nThen run 'aiwand setup' again.")
        return
    
    print(f"📋 Available providers: {', '.join(available_list)}")
    
    # Load current preferences
    current_prefs = load_user_preferences()
    current_provider = current_prefs.get("default_provider")
    current_models = current_prefs.get("models", {})
    
    print(f"\nCurrent settings:")
    if current_provider:
        print(f"  Provider: {current_provider}")
        if current_provider in current_models:
            print(f"  Model: {current_models[current_provider]}")
    else:
        print("  No preferences set")
    
    # Choose provider
    print(f"\n🔧 Choose your default provider:")
    for i, provider in enumerate(available_list, 1):
        marker = " (current)" if provider == current_provider else ""
        print(f"  {i}. {provider.title()}{marker}")
    
    while True:
        try:
            choice = input(f"\nEnter choice (1-{len(available_list)}) or press Enter to keep current: ").strip()
            if not choice and current_provider:
                chosen_provider = current_provider
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(available_list):
                chosen_provider = available_list[int(choice) - 1]
                break
            else:
                print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\n\nSetup cancelled.")
            return
    
    # Choose model for the provider
    supported_models = get_supported_models()[chosen_provider]
    current_model = current_models.get(chosen_provider, get_default_models()[chosen_provider])
    
    print(f"\n🤖 Choose your default model for {chosen_provider.title()}:")
    for i, model in enumerate(supported_models, 1):
        marker = " (current)" if model == current_model else ""
        if model == get_default_models()[chosen_provider]:
            marker += " (recommended)"
        print(f"  {i}. {model}{marker}")
    
    while True:
        try:
            choice = input(f"\nEnter choice (1-{len(supported_models)}) or press Enter to keep current: ").strip()
            if not choice:
                chosen_model = current_model
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(supported_models):
                chosen_model = supported_models[int(choice) - 1]
                break
            else:
                print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\n\nSetup cancelled.")
            return
    
    # Save preferences
    new_preferences = {
        "default_provider": chosen_provider,
        "models": {
            **current_models,
            chosen_provider: chosen_model
        }
    }
    
    try:
        save_user_preferences(new_preferences)
        print(f"\n✅ Preferences saved!")
        print(f"   Provider: {chosen_provider}")
        print(f"   Model: {chosen_model}")
        print(f"\n💡 You can change these anytime by running 'aiwand setup'")
        print(f"📁 Config saved to: {get_config_file()}")
    except AIError as e:
        print(f"\n❌ Error saving preferences: {e}")


def show_current_config() -> None:
    """Display current configuration and preferences."""
    print("🪄 AIWand Configuration")
    print("=" * 40)
    
    # Show available providers
    available = get_available_providers()
    print("📋 Available providers:")
    for provider, is_available in available.items():
        status = "✅" if is_available else "❌"
        print(f"  {status} {provider.title()}")
    
    if not any(available.values()):
        print("\n❌ No API keys configured!")
        print("Please set OPENAI_API_KEY or GEMINI_API_KEY environment variables.")
        return
    
    # Show current preferences
    preferences = load_user_preferences()
    print(f"\n⚙️  Current preferences:")
    
    if preferences:
        default_provider = preferences.get("default_provider")
        models = preferences.get("models", {})
        
        if default_provider:
            print(f"  Default provider: {default_provider}")
            if default_provider in models:
                print(f"  Default model: {models[default_provider]}")
        else:
            print("  No default provider set")
            
        if models:
            print(f"  Configured models:")
            for provider, model in models.items():
                print(f"    {provider}: {model}")
    else:
        print("  No preferences configured")
    
    # Show what will be used
    try:
        provider, model = get_preferred_provider_and_model()
        if provider and model:
            print(f"\n🎯 Currently using:")
            print(f"  Provider: {provider}")
            print(f"  Model: {model}")
        else:
            print(f"\n🎯 No provider currently available")
    except Exception as e:
        print(f"\n❌ Error getting current config: {e}")
    
    print(f"\n📁 Config file: {get_config_file()}")
    print(f"💡 Run 'aiwand setup' to change preferences") 


def get_current_provider() -> Optional[str]:
    """Get the currently active provider."""
    provider, _ = get_preferred_provider_and_model()
    return provider


def make_ai_request(
    messages: List[Dict[str, str]],
    max_tokens: Optional[int] = None,
    temperature: float = 0.7,
    top_p: float = 1.0,
    model: Optional[str] = None,
    response_format: Optional[Dict[str, Any]] = None
) -> str:
    """
    Unified wrapper for AI API calls that handles provider differences.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
        max_tokens: Maximum tokens to generate
        temperature: Response creativity (0.0 to 1.0)
        top_p: Nucleus sampling parameter
        model: Specific model to use (auto-selected if not provided)
        response_format: Response format specification
        
    Returns:
        str: The AI response content
        
    Raises:
        AIError: When the API call fails
    """
    try:
        client = get_ai_client()
        current_provider = get_current_provider()
        
        # Use provided model or get from user preferences
        if model is None:
            model = get_model_name()
        
        # Prepare common parameters
        params = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p
        }
        
        if max_tokens:
            params["max_tokens"] = max_tokens
        
        if response_format:
            params["response_format"] = response_format
        
        # Choose API call method based on provider and features
        if current_provider == "gemini" and response_format:
            # For Gemini with structured output, use beta endpoint
            response = client.beta.chat.completions.parse(**params)
        else:
            # Standard chat completions for all other cases
            response = client.chat.completions.create(**params)
        
        return response.choices[0].message.content.strip()
    
    except AIError as e:
        raise AIError(str(e))
    except Exception as e:
        raise AIError(f"AI request failed: {str(e)}") 