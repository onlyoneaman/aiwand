"""
Example: Using AIWand Classifier

This example demonstrates how to use the new AIWand classifier functionality
for text classification and grading tasks.
"""

import aiwand
from dotenv import load_dotenv

def main():
    load_dotenv()
    print("🔍 AIWand Classifier Examples\n")
    
    # Example 1: Simple binary classification
    print("=== Example 1: Binary Classification ===")
    
    result = aiwand.classify_text(
        input_text="What is 2 + 2?",
        output_text="4",
        expected_text="4",
        choice_scores={"CORRECT": 1.0, "INCORRECT": 0.0}
    )
    
    print(f"Score: {result.score}")
    print(f"Choice: {result.choice}")
    print(f"Reasoning: {result.reasoning}")
    print()
    
    # Example 2: Custom grading with multiple choices
    print("=== Example 2: Custom Grading Scale ===")
    
    result = aiwand.classify_text(
        input_text="Write a haiku about spring",
        output_text="Cherry blossoms bloom\nGentle breeze through ancient trees\nSpring awakens all",
        prompt_template="Evaluate this haiku based on structure (5-7-5 syllables) and imagery. Grade as: A (excellent), B (good), C (fair), D (poor)",
        choice_scores={"A": 1.0, "B": 0.75, "C": 0.5, "D": 0.25}
    )
    
    print(f"Score: {result.score}")
    print(f"Choice: {result.choice}")
    print(f"Reasoning: {result.reasoning}")
    print()
    
    # Example 3: Creating a reusable classifier
    print("=== Example 3: Reusable Classifier ===")
    
    # Create a math grader
    math_grader = aiwand.create_classifier(
        prompt_template="Grade this math answer. Input: {input}, Answer: {output}, Expected: {expected}",
        choice_scores={"CORRECT": 1.0, "PARTIAL": 0.5, "INCORRECT": 0.0},
        use_reasoning=True
    )
    
    # Use it multiple times
    questions = [
        ("What is 5 + 3?", "8", "8"),
        ("What is 10 / 2?", "5", "5"),
        ("What is 7 * 6?", "43", "42"),  # Wrong answer
    ]
    
    for question, answer, expected in questions:
        result = math_grader(question, answer, expected)
        print(f"Q: {question}")
        print(f"A: {answer} -> Score: {result.score} ({result.choice})")
        if result.reasoning:
            print(f"Reasoning: {result.reasoning[:100]}...")
        print()
    
    # Example 4: Predefined binary classifier
    print("=== Example 4: Predefined Binary Classifier ===")
    
    relevance_checker = aiwand.create_binary_classifier(criteria="relevance")
    
    result = relevance_checker(
        input_text="What is the capital of France?",
        output_text="Paris is the capital of France.",
        expected_text="Paris"
    )
    
    print(f"Relevance Score: {result.score}")
    print(f"Choice: {result.choice}")
    print()
    
    # Example 5: Quality classifier
    print("=== Example 5: Quality Classifier ===")
    
    quality_grader = aiwand.create_quality_classifier()
    
    result = quality_grader(
        input_text="Explain photosynthesis",
        output_text="Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to produce oxygen and energy in the form of sugar.",
        expected_text=""  # No specific expected answer
    )
    
    print(f"Quality Score: {result.score}")
    print(f"Grade: {result.choice}")
    print(f"Reasoning: {result.reasoning}")
    print()
    
    # Example 6: Comparison with your original complex setup
    print("=== Example 6: Simplified vs Complex ===")
    print("Instead of this complex setup:")
    print("""
    choice_scores = {"A": 1.0, "B": 0.0, "C": 0.5}
    grader = KayLLMClassifier(
        name="SimpleGrader",
        prompt_template=simple_classifier_prompt,
        choice_scores=choice_scores,
        use_cot=True,
        model=model_value,
    )
    response = await grader(
        input="question",
        output="predicted",
        expected="expected",
    )
    """)
    
    print("\nYou can now simply do:")
    print("result = aiwand.classify_text(input_text, output_text, expected_text, choice_scores={'A': 1.0, 'B': 0.0, 'C': 0.5})")
    
    # Show the simplified version in action
    simple_result = aiwand.classify_text(
        input_text="What color is the sky?",
        output_text="Blue",
        expected_text="Blue",
        choice_scores={"A": 1.0, "B": 0.0, "C": 0.5}
    )
    
    print(f"\nResult: Score={simple_result.score}, Choice={simple_result.choice}")


if __name__ == "__main__":
    try:
        main()
    except aiwand.AIError as e:
        print(f"AI Error: {e}")
        print("Make sure you have set up your API keys with 'aiwand setup' or environment variables.")
    except Exception as e:
        print(f"Error: {e}") 