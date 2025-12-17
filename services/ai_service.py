import google.generativeai as genai
import time

class AIService:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = self._initialize_model()

    def _initialize_model(self):
        model_names = ['gemini-1.5-flash-latest', 'gemini-2.5-flash', 'gemini-pro']
        for name in model_names:
            try:
                model = genai.GenerativeModel(name)
                # Quick connection test
                model.generate_content("Hello")
                print(f"Connected to model: {name}")
                return model
            except Exception:
                continue
        raise ValueError("Could not connect to any Gemini model.")

    def _generate_with_retry(self, prompt, max_retries=3):
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep((attempt + 1) * 2)
                else:
                    raise e

    def generate_readme(self, repo_name, code_files):
        code_summary = "\n\n".join([
            f"File: {f['path']}\n```\n{f['content'][:1000]}\n```"
            for f in code_files[:5]
        ])

        prompt = f"""Analyze this GitHub repository named '{repo_name}' and generate a comprehensive README.md file.
        
        Code files sample:
        {code_summary}
        
        Generate a Markdown README with: Title, Description, Features, Installation, Usage, Structure, and License."""
        
        return self._generate_with_retry(prompt)

    def generate_tests(self, code_files):
        main_files = [f for f in code_files if not f['name'].startswith('test_')][:3]
        code_summary = "\n\n".join([
            f"File: {f['path']}\n```\n{f['content'][:1500]}\n```"
            for f in main_files
        ])

        prompt = f"""Analyze these code files and generate comprehensive unit tests.
        
        Code to test:
        {code_summary}
        
        Generate a test file with imports, test cases, and assertions. 
        Detect the language and output valid code only."""
        
        return self._generate_with_retry(prompt)