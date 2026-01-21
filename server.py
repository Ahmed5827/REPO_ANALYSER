from flask import Flask, request, jsonify
from services.github_service import GitHubService
from services.ai_service import AIService
from utils.file_manager import save_results
from flask_cors import CORS
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}, expose_headers=["X-GitHub-Token", "X-Gemini-API-Key"], allow_headers=["Content-Type", "X-GitHub-Token", "X-Gemini-API-Key"])


@app.route('/analyze', methods=['POST'])
def analyze_repository():
    # 1. Get Tokens from Headers

    # Use .get() and check for both lowercase/uppercase just in case
    github_token = request.headers.get('X-GitHub-Token')
    gemini_api_key = request.headers.get('X-Gemini-API-Key')
    # 2. Get Repository URL from JSON Body
    data = request.get_json()
    if not data or 'repo_url' not in data:
        return jsonify({"error": "Missing 'repo_url' in request body"}), 400

    repo_url = data['repo_url']

    # 3. Validation
    if not github_token or not gemini_api_key:
        return jsonify({"error": "Missing GITHUB_TOKEN or GEMINI_API_KEY in headers"}), 401

    try:
        # 4. Initialize Services with dynamic tokens
        github_service = GitHubService(token=github_token)
        ai_service = AIService(api_key=gemini_api_key)

        # 5. Parse and Collect
        owner, repo_name = github_service.parse_github_url(repo_url)
        code_files = github_service.collect_code_files(owner, repo_name)

        if not code_files:
            return jsonify({"error": "No code files found in the repository"}), 404

        # 6. Generate Content
        readme_content = ai_service.generate_readme(repo_name, code_files)
        test_content = ai_service.generate_tests(code_files)

        # 7. Save Results (Optional, keep if you want local copies)
        save_results(repo_name, readme_content, test_content, code_files)

        # 8. Return JSON Response
        return jsonify({
            "status": "success",
            "repository": repo_name,
            "owner": owner,
            "files_analyzed": [f['path'] for f in code_files],
            "generated_content": {
                "readme": readme_content,
                "tests": test_content
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)