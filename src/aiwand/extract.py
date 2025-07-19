"""
Extract functionality for AIWand - structured data extraction from any content
"""

from typing import Optional, List, Union, Any, Dict
from pydantic import BaseModel
from .config import make_ai_request, ModelType
from .models import AIError
from .helper import read_file_content, fetch_url_content
from .utils import convert_to_string, string_to_json, is_local_file


def extract(
    content: Optional[Union[str, Any]] = None,
    links: Optional[List[str]] = None,
    model: Optional[ModelType] = None,
    temperature: float = 0.7,
    response_format: Optional[BaseModel] = None
) -> Union[str, Dict[str, Any]]:
    """
    Extract structured data from content and/or links using AI.
    
    This function processes any content (converted to string) and fetches data from
    links (URLs or file paths), then extracts structured information using AI.
    
    Args:
        content: Any content to extract from - will be converted to string.
            Can be str, dict, list, or any object with __str__ method.
        links: List of URLs or file paths to fetch and include in extraction.
            URLs (http/https) will be fetched, file paths will be read.
        model: Specific AI model to use (auto-selected if not provided)
        temperature: Response creativity (0.0 to 1.0, default 0.7)
        response_format: Pydantic model class for structured output.
        
    Returns:
        Union[str, Dict[str, Any]]: Extracted data.
        - Dict if JSON parsing succeeds
        - Formatted string otherwise
        
    Raises:
        ValueError: If neither content nor links are provided
        AIError: If the AI call fails
        FileNotFoundError: If file path doesn't exist
        
    Examples:
        # Simple text extraction
        result = extract(content="John Doe, email: john@example.com")
        
        # Extract from URLs
        result = extract(links=["https://example.com/article"])
        
        # Mix content and links with structured output
        from pydantic import BaseModel
        
        class ContactInfo(BaseModel):
            name: str
            email: str
            
        result = extract(
            content="Meeting notes: contact John at john@example.com",
            links=["https://company.com/about", "/path/to/business_card.txt"],
            response_format=ContactInfo
        )
        
        # Complex content (dict/list converted to string)
        data = {"name": "John", "email": "john@example.com"}
        result = extract(content=data)
    """
    if not content and not links:
        raise ValueError("Must provide either content or links")
    
    all_content = []
    
    if content is not None:
        content_str = convert_to_string(content)
        if content_str.strip():
            all_content.append(f"=== Main Content ===\n{content_str}")
    
    if links:
        for i, link in enumerate(links, 1):
            try:
                if not is_local_file(link):
                    link_content = fetch_url_content(link)
                    all_content.append(f"=== Link {i}: {link} ===\n{link_content}")
                else:
                    file_content = read_file_content(link)
                    all_content.append(f"=== File {i}: {link} ===\n{file_content}")
            except Exception as e:
                raise AIError(f"Failed to process link '{link}': {str(e)}")
    
    if not all_content:
        raise ValueError("No valid content found to process")
    
    combined_content = "\n\n".join(all_content)
    
    system_prompt = (
        "You are an expert data extraction specialist. You excel at identifying, "
        "analyzing, and extracting structured information from unstructured text. "
        "You provide accurate, well-organized data while preserving context and "
        "maintaining data integrity. You follow the specified format requirements precisely."
    )
    
    user_prompt = "Extract relevant structured data from the following content:\n\n"
        
    user_prompt += (
        "Organize the extracted data in a clear, logical structure. "
        "return the data as JSON format. "
        "Use appropriate categories and present the information in a way that's "
        "easy to understand and use. Include any relevant metadata or context.\n\n"
    )
    
    user_prompt += f"Content to extract from:\n{combined_content}"
    
    result = make_ai_request(
        system_prompt=system_prompt,
        model=model,
        temperature=temperature,
        response_format=response_format,
        user_prompt=user_prompt
    )
    if response_format:
        return result    
    return string_to_json(result)

