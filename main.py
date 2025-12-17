from config import Config
from services.github_service import GitHubService
from services.ai_service import AIService
from utils.file_manager import save_results

def main():
    # 1. Validation & Setup
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return

    github_service = GitHubService(token=Config.GITHUB_TOKEN)
    
    try:
        ai_service = AIService(api_key=Config.GEMINI_API_KEY)
    except ValueError as e:
        print(f"AI Service Error: {e}")
        return

    # 2. Input
    repo_url = input("Enter GitHub repository URL: ")

    try:
        # 3. Analyze
        print(f"Analyzing {repo_url}...")
        owner, repo_name = github_service.parse_github_url(repo_url)
        
        print("Collecting code files...")
        code_files = github_service.collect_code_files(owner, repo_name)
        
        if not code_files:
            print("No code files found.")
            return

        print(f"Found {len(code_files)} files. Generating content...")
        
        # 4. Generate
        readme_content = ai_service.generate_readme(repo_name, code_files)
        test_content = ai_service.generate_tests(code_files)

        # 5. Save
        save_results(repo_name, readme_content, test_content, code_files)
        print("\n✓ Process completed successfully!")

    except Exception as e:
        print(f"\n✗ Error: {e}")

if __name__ == "__main__":
    main()