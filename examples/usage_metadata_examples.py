import aiwand
from dotenv import load_dotenv

load_dotenv()

def main():
    response = aiwand.call_ai(
        user_prompt="What is the capital of France?",
        raw_response=True,
        model='gpt-4o-mini',
        debug=True
    )
    print(response)
    
if __name__ == "__main__":
    main()