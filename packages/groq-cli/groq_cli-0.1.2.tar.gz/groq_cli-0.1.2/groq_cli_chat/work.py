import os
import json
import argparse
from groq import Groq

#? dicts for role and model
role_dict = {
    '1': 'system',
    '2': 'user',
    '3': 'assistant'
}

model_dict = {
    '1': 'llama3-8b-8192',
    '2': 'llama3-70b-8192',
    '3': 'mixtral-8x7b-32768',
    '4': 'gemma-7b-it'
}

#? options for role and model
def role_options():
    print("\nChoose a role:")
    print("1. System: Can be used to provide specific instructions for how it should behave throughout the conversation.")
    print("2. User: Messages written by a user of the LLM.")
    print("3. Assistant: Messages written by the LLM in a previous completion.")

def model_options():
    print("\nChoose a model:")
    print("1. LLaMA3 8b")
    print("2. LLaMA3 70b")
    print("3. Mixtral 8x7b")
    print("4. Gemma 7b")


def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))

def check_setup():
    config_path = os.path.join(get_script_dir(), "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
        if config.get("SETUP_COMPLETE") == "True":
            return True
    return False

def setup():
    if check_setup():
        return

    api_key = input("Enter your API key: ")

    role_options()

    while True:
        role_choice = input("\nEnter your role choice (1, 2, or 3): ")
        if role_choice in ['1', '2', '3']:
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    role = role_dict[role_choice]

    model_options()

    while True:
        model_choice = input("\nEnter your model choice (1, 2, 3, or 4): ")
        if model_choice in ['1', '2', '3', '4']:
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

    model = model_dict[model_choice]

    config = {
        "GROQ_API_KEY": api_key,
        "GROQ_ROLE": role,
        "GROQ_MODEL": model,
        "SETUP_COMPLETE": "True"
    }

    with open(os.path.join(get_script_dir(), "config.json"), "w") as f:
        json.dump(config, f)

    print("Setup complete!")


def edit_role():

    role_options()

    while True:
        role_choice = input("\nEnter your role choice (1, 2, or 3): ")
        if role_choice in ['1', '2', '3']:
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    role = role_dict[role_choice]

    config_path = os.path.join(get_script_dir(), "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
        config["GROQ_ROLE"] = role
        with open(config_path, "w") as f:
            json.dump(config, f)
        print("Role updated successfully.")


def edit_api():
    new_api_key = input("Enter your new API key: ")
    
    config_path = os.path.join(get_script_dir(), "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
        config["GROQ_API_KEY"] = new_api_key
        with open(config_path, "w") as f:
            json.dump(config, f)
        print("API key updated successfully.")


def edit_model():
    model_options()

    while True:
        model_choice = input("\nEnter your model choice (1, 2, 3, or 4): ")
        if model_choice in ['1', '2', '3', '4']:
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

    model = model_dict[model_choice]

    config_path = os.path.join(get_script_dir(), "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
        config["GROQ_MODEL"] = model
        with open(config_path, "w") as f:
            json.dump(config, f)
        print("Model updated successfully.")




def search(query):
    config_path = os.path.join(get_script_dir(), "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
        api_key = config["GROQ_API_KEY"]
        role = config["GROQ_ROLE"]
        model = config["GROQ_MODEL"]

        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": role,
                    "content": query,
                }
            ],
            model=model,
        )

        print("\033[K\r", end="")
        print("\n", chat_completion.choices[0].message.content)
    else:
        print("Configuration file not found. Please run setup first.")



def main():
    parser = argparse.ArgumentParser(description='prompt for input')
    parser.add_argument('--role', action='store_true', help='Change the role')
    parser.add_argument('--api', action='store_true', help='Change the API key')
    parser.add_argument('--model', action='store_true', help='Change the model')

    args, unknown = parser.parse_known_args()

    if args.role:
        edit_role()
        return

    if args.api:
        edit_api()
        return

    if args.model:
        edit_model()
        return

    if not check_setup() and not unknown:
        setup()
        return
        
    if not unknown:
        query = input("Enter your query: ")  
    else:
        query = ' '.join(unknown)
    search(query)

if __name__ == "__main__":
    main()
