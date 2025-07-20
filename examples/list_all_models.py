import aiwand
import pprint
from dotenv import load_dotenv

def main():
    load_dotenv()
    models = aiwand.list_models()
    pprint.pp(models)
    for model in models:
        print(model.id)

if __name__ == "__main__":
    main()