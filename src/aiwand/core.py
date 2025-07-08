"""
Core AI functionality for AIWand
"""

from typing import Optional, List, Dict, Any
from .config import make_ai_request, AIError


def summarize(
    text: str,
    max_length: Optional[int] = None,
    style: str = "concise",
    model: Optional[str] = None
) -> str:
    """
    Summarize the given text using AI API (OpenAI or Gemini).
    
    Args:
        text (str): The text to summarize
        max_length (Optional[int]): Maximum length of the summary in words
        style (str): Style of summary ('concise', 'detailed', 'bullet-points')
        model (Optional[str]): Specific model to use (auto-selected if not provided)
        
    Returns:
        str: The summarized text
        
    Raises:
        ValueError: If the text is empty
        AIError: If the API call fails
    """
    if not text.strip():
        raise ValueError("Text cannot be empty")
    
    # Prepare the prompt based on style
    style_prompts = {
        "concise": "Provide a concise summary of the following text:",
        "detailed": "Provide a detailed summary of the following text:",
        "bullet-points": "Summarize the following text in bullet points:"
    }
    
    prompt = style_prompts.get(style, style_prompts["concise"])
    
    if max_length:
        prompt += f" Keep the summary under {max_length} words."
    
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": text}
    ]
    
    return make_ai_request(
        messages=messages,
        max_tokens=2000,
        temperature=0.3,
        model=model
    )


def chat(
    message: str,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    model: Optional[str] = None,
    temperature: float = 0.7
) -> str:
    """
    Have a conversation with the AI (OpenAI or Gemini).
    
    Args:
        message (str): The user's message
        conversation_history (Optional[List[Dict[str, str]]]): Previous conversation messages
        model (Optional[str]): Specific model to use (auto-selected if not provided)
        temperature (float): Response creativity (0.0 to 1.0)
        
    Returns:
        str: The AI's response
        
    Raises:
        ValueError: If the message is empty
        AIError: If the API call fails
    """
    if not message.strip():
        raise ValueError("Message cannot be empty")
    
    messages = conversation_history or []
    messages.append({"role": "user", "content": message})
    
    return make_ai_request(
        messages=messages,
        max_tokens=1000,
        temperature=temperature,
        model=model
    )


def generate_text(
    prompt: str,
    max_tokens: int = 500,
    temperature: float = 0.7,
    model: Optional[str] = None
) -> str:
    """
    Generate text based on a prompt using AI (OpenAI or Gemini).
    
    Args:
        prompt (str): The prompt to generate text from
        max_tokens (int): Maximum number of tokens to generate
        temperature (float): Response creativity (0.0 to 1.0)
        model (Optional[str]): Specific model to use (auto-selected if not provided)
        
    Returns:
        str: The generated text
        
    Raises:
        ValueError: If the prompt is empty
        AIError: If the API call fails
    """
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    
    messages = [{"role": "user", "content": prompt}]
    
    return make_ai_request(
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        model=model
    ) 