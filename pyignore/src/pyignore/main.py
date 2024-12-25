import requests
import argparse

def get_gitignore_template(language):
    api_url = f"https://api.github.com/gitignore/templates/{language}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        template_data = response.json()
        return template_data['source']
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def list_gitignore_templates():
    api_url = "https://api.github.com/gitignore/templates"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        templates = response.json()
        return templates
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def cli():
    parser = argparse.ArgumentParser(description="Fetch .gitignore template for a specified language from GitHub.")
    parser.add_argument("language", type=str, nargs="?", help="The language for which you want the .gitignore template (e.g., Python, Java, Node).")
    parser.add_argument("-l", "--list", action="store_true", help="List all available .gitignore templates.")
    
    args = parser.parse_args()
    
    if args.list:
        templates = list_gitignore_templates()
        if templates:
            print("Available .gitignore templates:\n")
            for template in templates:
                print(template)
        else:
            print("Could not retrieve the list of .gitignore templates.")
    elif args.language:
        template = get_gitignore_template(args.language)
        if template:
            print(f".gitignore template for {args.language}:\n")
            print(template)
        else:
            print(f"Could not retrieve the .gitignore template for {args.language}.")
    else:
        parser.print_help()

def main():
    cli()
    
if __name__ == "__main__":
    main()