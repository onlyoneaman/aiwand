from openai import OpenAI
from typing import Dict, Any
from .extras import print_debug_messages, remove_empty_values
from ..models import FullAiResponse, UsageMetadata


def openai_config_params(params: Dict[str, Any]) -> Dict[str, Any]:
    config = {
        "model": params.get("model"),
        "input": params.get("messages"),
        "temperature": params.get("temperature"),
        "top_p": params.get("top_p"),
        "max_output_tokens": params.get("max_completion_tokens"),
        "tools": params.get("tools"),
        "tool_choice": params.get("tool_choice"),
    }
    response_format = params.get("response_format")
    if response_format:
        config["text_format"] = response_format
    return remove_empty_values(config)


def chatcompletion_usage_details(response: Any) -> UsageMetadata:
    """
    Get usage details from a OpenAI API response.
    """
    return UsageMetadata(
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        total_tokens=response.usage.total_tokens,
        raw_metadata=response.usage
    )


def responses_usage_details(response: Any) -> UsageMetadata:
    """
    Get usage details from a OpenAI API response.
    """
    return UsageMetadata(
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
        total_tokens=response.usage.total_tokens,
        raw_metadata=response.usage
    )


def get_openai_response(client: OpenAI, params: Dict[str, Any], debug: bool = False, raw_response: bool = False) -> str:
    if debug:
        print_debug_messages(messages=params.get("messages"), params=params)
    response_format = params.get("response_format")
    config = openai_config_params(params)
    if response_format:
        full_response = client.responses.parse(**config)
        return_value = full_response.output_parsed
    else:
        full_response = client.responses.create(**config)
        return_value = full_response.output_text.strip()
    if raw_response:
        return_value = FullAiResponse(
            output=return_value,
            usage_metadata=responses_usage_details(full_response),
            raw_response=full_response
        )
    return return_value
