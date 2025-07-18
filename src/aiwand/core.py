"""
Core AI functionality for AIWand
"""

from typing import Optional, List, Dict, Any
from .config import make_ai_request, AIError, ModelType, DEFAULT_SYSTEM_PROMPT


def summarize(
    text: str,
    max_length: Optional[int] = None,
    style: str = "concise",
    model: Optional[ModelType] = None
) -> str:
    """
    Summarize the given text using AI API (OpenAI or Gemini).
    
    Args:
        text (str): The text to summarize
        max_length (Optional[int]): Maximum length of the summary in words
        style (str): Style of summary ('concise', 'detailed', 'bullet-points')
        model (Optional[ModelType]): Specific model to use (auto-selected if not provided)
        
    Returns:
        str: The summarized text
        
    Raises:
        ValueError: If the text is empty
        AIError: If the API call fails
    """
    if not text.strip():
        raise ValueError("Text cannot be empty")
    
    # Prepare the system prompt for summarization
    system_prompt = "You are an expert text summarizer. You excel at extracting key information and presenting it clearly and concisely while preserving the essential meaning and context."
    
    # Prepare the user prompt based on style
    style_prompts = {
        "concise": "Provide a concise summary of the following text:",
        "detailed": "Provide a detailed summary of the following text:",
        "bullet-points": "Summarize the following text in bullet points:"
    }
    
    user_prompt = style_prompts.get(style, style_prompts["concise"])
    
    if max_length:
        user_prompt += f" Keep the summary under {max_length} words."
    
    messages = [
        {"role": "user", "content": f"{user_prompt}\n\n{text}"}
    ]
    
    return make_ai_request(
        messages=messages,
        model=model,
        system_prompt=system_prompt
    )


def chat(
    message: str,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    model: Optional[ModelType] = None,
    temperature: float = 0.7
) -> str:
    """
    Have a conversation with the AI (OpenAI or Gemini).
    
    Args:
        message (str): The user's message
        conversation_history (Optional[List[Dict[str, str]]]): Previous conversation messages
        model (Optional[ModelType]): Specific model to use (auto-selected if not provided)
        temperature (float): Response creativity (0.0 to 1.0)
        
    Returns:
        str: The AI's response
        
    Raises:
        ValueError: If the message is empty
        AIError: If the API call fails
    """
    if not message.strip():
        raise ValueError("Message cannot be empty")
    
    # Prepare system prompt for conversational AI
    system_prompt = "You are a helpful, knowledgeable, and engaging conversational AI assistant. You provide thoughtful responses, ask clarifying questions when needed, and maintain context throughout the conversation. You are friendly, professional, and adapt your tone to match the user's needs."
    
    messages = conversation_history or []
    messages.append({"role": "user", "content": message})
    
    return make_ai_request(
        messages=messages,
        temperature=temperature,
        model=model,
        system_prompt=system_prompt
    )


def generate_text(
    prompt: str,
    max_tokens: int = None,
    temperature: float = 0.7,
    model: Optional[ModelType] = None
) -> str:
    """
    Generate text based on a prompt using AI (OpenAI or Gemini).
    
    Args:
        prompt (str): The prompt to generate text from
        max_tokens (int): Maximum number of tokens to generate
        temperature (float): Response creativity (0.0 to 1.0)
        model (Optional[ModelType]): Specific model to use (auto-selected if not provided)
        
    Returns:
        str: The generated text
        
    Raises:
        ValueError: If the prompt is empty
        AIError: If the API call fails
    """
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    
    # Prepare system prompt for text generation
    system_prompt = "You are a skilled creative writer and content generator. You excel at producing high-quality, engaging, and contextually appropriate text based on user prompts. You adapt your writing style, tone, and format to match the specific requirements and context provided."
    
    messages = [{"role": "user", "content": prompt}]
    
    return make_ai_request(
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        model=model,
        system_prompt=system_prompt
    ) 