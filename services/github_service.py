import requests
import base64
from pathlib import Path

class GitHubService:
    def __init__(self, token=None):
        self.headers = {}
        if token:
            self.headers['Authorization'] = f'token {token}'
        self.extensions = {'.py', '.js', '.java', '.cpp', '.c', '.go', '.rs', '.ts', '.jsx', '.tsx'}

    def parse_github_url(self, url):
        """Extract owner and repo name from GitHub URL"""
        parts = url.rstrip('/').split('/')
        if 'github.com' in url:
            repo_name = parts[-1].replace('.git', '')
            return parts[-2], repo_name
        raise ValueError("Invalid GitHub URL")

    def get_repo_structure(self, owner, repo, path=''):
        """Get repository file structure using GitHub API"""
        api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
        response = requests.get(api_url, headers=self.headers)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch repo: {response.status_code} - {response.text}")
        return response.json()

    def get_file_content(self, owner, repo, file_path):
        """Get content of a specific file"""
        api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}'
        response = requests.get(api_url, headers=self.headers)

        if response.status_code == 200:
            content = response.json()
            if content.get('encoding') == 'base64':
                return base64.b64decode(content['content']).decode('utf-8')
        return None

    def collect_code_files(self, owner, repo, path='', max_files=20):
        """Recursively collect code files from repository"""
        code_files = []
        try:
            contents = self.get_repo_structure(owner, repo, path)
            for item in contents:
                if len(code_files) >= max_files:
                    break

                if item['type'] == 'file':
                    file_ext = Path(item['name']).suffix
                    if file_ext in self.extensions:
                        content = self.get_file_content(owner, repo, item['path'])
                        if content:
                            code_files.append({
                                'path': item['path'],
                                'name': item['name'],
                                'content': content
                            })
                elif item['type'] == 'dir' and not item['name'].startswith('.'):
                    code_files.extend(
                        self.collect_code_files(owner, repo, item['path'], max_files - len(code_files))
                    )
        except Exception as e:
            print(f"Error collecting files from {path}: {e}")
        
        return code_files