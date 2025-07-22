from dotenv import load_dotenv
import aiwand
from openai import Client
import os

def main():
    load_dotenv()
    user_prompt = "Analyze the letter and provide a summary of the key points." 
    url = "https://www.berkshirehathaway.com/letters/2024ltr.pdf"
    # aiwand.call_ai(
    #     links=[url],
    #     user_prompt=user_prompt,
    # )
    openai_client = Client()
    messages = [
        {"role": "user", "content": user_prompt},
        {
            "role": "user", 
            "content": [
                {
                    "type": "input_file",
                    "file_url": url
                }
            ]
        },
    ]
    response = openai_client.responses.create(
        model="gpt-4.1",
        input=messages,
    )
    output = response.output[0]
    text_content = output.content[0].text
    print(text_content)

    aiwand.extract(
        content="Aman works at Kay.ai",
        model="gpt-4o",
    )



if __name__ == "main":
    main()