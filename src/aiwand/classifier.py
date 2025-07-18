"""
AIWand Classifier - Simple text classification and grading functionality.

This module provides a simplified classifier that can be used to grade or classify
text responses based on custom criteria and choice scores.
"""

from typing import Dict, Optional, List, Any, Union
from pydantic import BaseModel, Field

from .config import make_ai_request, AIError, ModelType
from .models import AIProvider


class ClassifierResponse(BaseModel):
    """Response from the classifier with score, choice, and optional reasoning."""
    
    score: float = Field(description="The numerical score for the response")
    choice: str = Field(description="The choice/grade selected")
    reasoning: str = Field(default="", description="Reasoning behind the choice")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    def __init__(self, **data):
        super().__init__(**data)
        # Add reasoning to metadata for compatibility
        if self.reasoning and "rationale" not in self.metadata:
            self.metadata["rationale"] = self.reasoning


def classify_text(
    input_text: str,
    output_text: str,
    expected_text: str = "",
    prompt_template: str = "",
    choice_scores: Optional[Dict[str, float]] = None,
    use_reasoning: bool = True,
    model: Optional[ModelType] = None,
    provider: Optional[Union[AIProvider, str]] = None
) -> ClassifierResponse:
    """
    Classify or grade text based on custom criteria.
    
    This function provides a simple interface for text classification and grading
    that's inspired by autoevals but integrated with AIWand's provider system.
    
    Args:
        input_text: The question, prompt, or context
        output_text: The response to be evaluated
        expected_text: The expected or reference response (optional)
        prompt_template: Custom prompt template with {input}, {output}, {expected} placeholders
        choice_scores: Mapping of choices to scores (e.g., {"A": 1.0, "B": 0.5, "C": 0.0})
        use_reasoning: Whether to include step-by-step reasoning
        model: Specific model to use
        provider: Specific provider to use
        
    Returns:
        ClassifierResponse with score, choice, reasoning, and metadata
        
    Raises:
        ValueError: If required parameters are missing
        AIError: If the classification fails
        
    Examples:
        # Simple grading
        result = classify_text(
            input_text="What is 2+2?",
            output_text="4", 
            expected_text="4",
            choice_scores={"CORRECT": 1.0, "INCORRECT": 0.0}
        )
        
        # Custom prompt with reasoning
        result = classify_text(
            input_text="Write a haiku about spring",
            output_text="Cherry blossoms bloom\\nGentle breeze through ancient trees\\nSpring awakens all",
            prompt_template="Evaluate this haiku based on structure and imagery. Grade as: A (excellent), B (good), C (fair), D (poor)",
            choice_scores={"A": 1.0, "B": 0.75, "C": 0.5, "D": 0.25},
            use_reasoning=True
        )
    """
    # Validate inputs
    if not input_text.strip():
        raise ValueError("input_text cannot be empty")
    if not output_text.strip():
        raise ValueError("output_text cannot be empty")
    
    # Default choice scores if not provided
    if choice_scores is None:
        choice_scores = {"CORRECT": 1.0, "INCORRECT": 0.0}
    
    if not choice_scores:
        raise ValueError("choice_scores cannot be empty")
    
    # Default prompt template if not provided
    if not prompt_template.strip():
        if expected_text.strip():
            prompt_template = """
Evaluate the given response by comparing it to the expected answer.

Question/Input: {input}
Given Response: {output}
Expected Response: {expected}

Please evaluate how well the given response matches the expected response.
Grade the response as: {choices}
"""
        else:
            prompt_template = """
Evaluate the quality of the given response to the input.

Input: {input}
Response: {output}

Please evaluate the quality and appropriateness of the response.
Grade the response as: {choices}
"""
    
    # Format choices for the prompt
    choices_text = ", ".join([f"{choice} ({score})" for choice, score in choice_scores.items()])
    
    # Create dynamic response model
    if use_reasoning:
        class DynamicClassifierModel(BaseModel):
            reasoning: str = Field(description="Step-by-step analysis and reasoning")
            grade: str = Field(description=f"Final grade, must be one of: {', '.join(choice_scores.keys())}")
    else:
        class DynamicClassifierModel(BaseModel):
            grade: str = Field(description=f"Final grade, must be one of: {', '.join(choice_scores.keys())}")
    
    # Format the prompt
    formatted_prompt = prompt_template.format(
        input=input_text,
        output=output_text,
        expected=expected_text,
        choices=choices_text
    )
    
    # System prompt for classification
    system_prompt = f"""You are an AI classifier and grader. Evaluate responses according to the given criteria.

Available grades: {', '.join(choice_scores.keys())}

{"Provide your step-by-step reasoning in the 'reasoning' field, then your final grade in the 'grade' field." if use_reasoning else "Provide your final grade in the 'grade' field."}

Your grade must be exactly one of the specified options."""
    
    messages = [{"role": "user", "content": formatted_prompt}]
    
    try:
        # Use structured output
        result = make_ai_request(
            messages=messages,
            system_prompt=system_prompt,
            response_format=DynamicClassifierModel,
            model=model,
            provider=provider,
            temperature=0.0  # Use deterministic output for grading
        )
        
        # Validate grade
        grade = result.grade.upper()
        if grade not in choice_scores:
            # Try case-insensitive match
            grade_lower = result.grade.lower()
            matched_key = None
            for key in choice_scores.keys():
                if key.lower() == grade_lower:
                    matched_key = key
                    break
            
            if matched_key:
                grade = matched_key
            else:
                raise AIError(f"Invalid grade '{result.grade}' received. Expected one of: {', '.join(choice_scores.keys())}")
        
        score = choice_scores[grade]
        reasoning = getattr(result, 'reasoning', '') if use_reasoning else ''
        
        return ClassifierResponse(
            score=score,
            choice=grade,
            reasoning=reasoning,
            metadata={
                "model": str(model) if model else None,
                "provider": str(provider) if provider else None,
                "choices_available": list(choice_scores.keys()),
                "choice_scores": choice_scores
            }
        )
        
    except AIError:
        raise
    except Exception as e:
        raise AIError(f"Classification failed: {str(e)}")


def create_classifier(
    prompt_template: str,
    choice_scores: Dict[str, float],
    use_reasoning: bool = True,
    model: Optional[ModelType] = None,
    provider: Optional[Union[AIProvider, str]] = None
) -> callable:
    """
    Create a reusable classifier function with predefined settings.
    
    This is useful when you want to create a classifier with specific settings
    that you'll use multiple times.
    
    Args:
        prompt_template: Template for evaluation prompts
        choice_scores: Mapping of choices to scores
        use_reasoning: Whether to include reasoning
        model: Default model to use
        provider: Default provider to use
        
    Returns:
        A callable classifier function
        
    Example:
        # Create a reusable grader
        grader = create_classifier(
            prompt_template="Grade this math answer: {input} -> {output} (expected: {expected})",
            choice_scores={"CORRECT": 1.0, "PARTIAL": 0.5, "INCORRECT": 0.0},
            use_reasoning=True
        )
        
        # Use it multiple times
        result1 = grader("2+2", "4", "4")
        result2 = grader("3+3", "6", "6")
    """
    def classifier(
        input_text: str,
        output_text: str,
        expected_text: str = "",
        **kwargs
    ) -> ClassifierResponse:
        """Classify text using the predefined settings."""
        # Allow overriding settings via kwargs
        return classify_text(
            input_text=input_text,
            output_text=output_text,
            expected_text=expected_text,
            prompt_template=prompt_template,
            choice_scores=choice_scores,
            use_reasoning=use_reasoning,
            model=kwargs.get('model', model),
            provider=kwargs.get('provider', provider)
        )
    
    return classifier


# Predefined common classifiers
def create_binary_classifier(
    criteria: str = "correctness",
    model: Optional[ModelType] = None,
    provider: Optional[Union[AIProvider, str]] = None
) -> callable:
    """
    Create a simple binary (correct/incorrect) classifier.
    
    Args:
        criteria: What to evaluate (e.g., "correctness", "relevance", "quality")
        model: Model to use
        provider: Provider to use
        
    Returns:
        Binary classifier function
    """
    prompt_template = f"""
Evaluate the {criteria} of the response.

Input: {{input}}
Response: {{output}}
Expected: {{expected}}

Is the response correct and appropriate? Grade as CORRECT or INCORRECT.
"""
    
    return create_classifier(
        prompt_template=prompt_template,
        choice_scores={"CORRECT": 1.0, "INCORRECT": 0.0},
        use_reasoning=True,
        model=model,
        provider=provider
    )


def create_quality_classifier(
    model: Optional[ModelType] = None,
    provider: Optional[Union[AIProvider, str]] = None
) -> callable:
    """
    Create a quality classifier with grades A through F.
    
    Args:
        model: Model to use
        provider: Provider to use
        
    Returns:
        Quality classifier function
    """
    prompt_template = """
Evaluate the overall quality of the response.

Input: {input}
Response: {output}
Expected: {expected}

Consider factors like accuracy, completeness, clarity, and appropriateness.
Grade as: A (excellent), B (good), C (average), D (below average), F (poor)
"""
    
    return create_classifier(
        prompt_template=prompt_template,
        choice_scores={"A": 1.0, "B": 0.8, "C": 0.6, "D": 0.4, "F": 0.0},
        use_reasoning=True,
        model=model,
        provider=provider
    ) 