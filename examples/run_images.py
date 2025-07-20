import aiwand
from dotenv import load_dotenv

def main():
    load_dotenv()
    links = [
        "https://bella.amankumar.ai/examples/receipt_1.jpeg"
    ]
    data = aiwand.call_ai(
        system_prompt="You are a helpful assistant that can extract text from images.",
        user_prompt="Extract the whole text from the image.",
        images=links,
        debug=True
    )
    print(data)

    data2 = aiwand.extract(
        links=links
    )

    return data

if __name__ == "main":
    main()