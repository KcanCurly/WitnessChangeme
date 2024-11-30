import argparse
import os
import importlib.util
from pathlib import Path
from witnesschangeme import AuthChecker
from concurrent.futures import ThreadPoolExecutor

class TemplateManager:
    @staticmethod
    def get_template_folders():
        """Get all subfolders in the templates directory."""
        current_script = Path(__file__).resolve()
        base_path = os.path.join(current_script.parent.parent, "templates")
        return [
            folder for folder in os.listdir(base_path)
            if os.path.isdir(os.path.join(base_path, folder))
        ]

    @staticmethod
    def load_template(template_name):
        """Load the template.py file from the specified template folder."""
        template_path = os.path.join(Path(__file__).resolve().parent.parent, "templates", template_name, "template.py")
        
        if not os.path.exists(template_path):
            print(template_path)
            return None

        spec = importlib.util.spec_from_file_location("template", template_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.get_template()

    @staticmethod
    def load_all_templates():
        """Load all templates from the templates directory."""
        templates = {}
        for folder in TemplateManager.get_template_folders():
            template = TemplateManager.load_template(folder)
            if template:
                templates[folder] = template
        return templates
    
    
def main():
    parser = argparse.ArgumentParser(description="Witnesschangeme - Website Authentication Checker")
    parser.add_argument("--url", required=True, help="Target URL to test.")
    parser.add_argument("--output-dir", default="output/", help="Directory to save results.")
    args = parser.parse_args()

    # Load all templates
    templates = TemplateManager.load_all_templates()
    if not templates:
        print("No templates found in the 'templates' folder.")
        return

    print(f"Loaded {len(templates)} templates: {', '.join(templates.keys())}")


    if os.path.isfile(args.url):
        with open(args.url, 'r') as file:
            for line in file:
                for template_name, template in templates.items():
                    print(f"Running template: {template_name} for {line}")
                    auth_checker = AuthChecker(url=line, template=template, output_dir=args.output_dir)
                    auth_checker.run()
    else:
        for template_name, template in templates.items():
            print(f"Running template: {template_name}")
            auth_checker = AuthChecker(url=args.url, template=template, output_dir=args.output_dir)
            auth_checker.run()
    

if __name__ == "__main__":
    main()