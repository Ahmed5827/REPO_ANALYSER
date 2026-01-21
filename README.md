# GitHub Repository Analyzer with Gemini AI 🤖

A modular Python tool that automatically analyzes GitHub repositories using Google's Gemini AI. It reads the codebase and generates a comprehensive `README.md` and a suite of unit tests tailored to the project's language.
---
![Terminal Screenshot](docs/Screenshot1.png)

![Output Screenshot](docs/Screenshot2.png)
---
## 🚀 Features

*   **Repository Parsing**: Automatically fetches and parses file structures from GitHub URLs.
*   **Smart Analysis**: Uses Google Gemini Pro/Flash models to understand code logic.
*   **Documentation Generator**: Creates professional `README.md` files describing the project.
*   **Test Generation**: detailed unit tests based on the source code.
*   **Modular Architecture**: Clean separation of services (GitHub, AI, File Management).

## 🛠️ Project Structure

```text
repo_analyzer/
├── main.py               # Entry point
├── config.py             # Environment configuration
├── services/
│   ├── github_service.py # GitHub API interactions
│   └── ai_service.py     # Gemini AI generation logic
├── utils/
│   └── file_manager.py   # File saving utilities
└── .env                  # API Keys (Not committed)
```

## 🌐 Web Server (Flask API)

This project provides a Flask-based REST API that exposes repository analysis functionality as a web service. By leveraging **Google Gemini AI**, it allows external clients—such as frontend applications, CI/CD scripts, or third-party services—to programmatically analyze GitHub repositories and generate documentation and tests.

### ✨ Purpose

The web server acts as an HTTP interface for the core analysis engine, enabling:
*   **Remote Analysis:** Process repositories via standard REST calls.
*   **Seamless Integration:** Easily connect with web or mobile frontends.


---

### 🚀 Getting Started

#### Prerequisites
- Python 3.8+
- Flask
- Required dependencies (see `requirements.txt`)

#### Installation
1. Install the required packages:
   ```bash
   pip install flask
   ```
2. Run the server:
   ```bash
   python server.py
   ```
---

### 🔌 API Documentation

#### Analyze Repository
`POST /analyze`

Analyzes a specified GitHub repository and returns AI-generated documentation and unit tests.

##### 📥 Request Details

**Headers**

| Header Name | Description | Required |
| :--- | :--- | :--- |
| `X-GitHub-Token` | GitHub Personal Access Token | **Yes** |
| `X-Gemini-API-Key` | Google Gemini API Key | **Yes** |
| `Content-Type` | `application/json` | **Yes** |

**Body (JSON)**
```json
{
  "repo_url": "https://github.com/owner/repository"
}
```

---

##### 📤 Response Details

**Success (200 OK)**
```json
{
  "status": "success",
  "repository": "repo-name",
  "owner": "owner-name",
  "files_analyzed": [
    "path/to/file1.py",
    "path/to/file2.js"
  ],
  "generated_content": {
    "readme": "...generated README content...",
    "tests": "...generated unit tests..."
  }
}
```

**❌ Error Responses**

| Status Code | Description |
| :--- | :--- |
| `400` | Bad Request: Missing `repo_url` in request body |
| `401` | Unauthorized: Missing GitHub or Gemini API tokens |
| `404` | Not Found: No analyzable code files found in the repository |
| `500` | Internal Server Error: Unexpected error during analysis |

---

### 🛠 Usage Example (cURL)

```bash
curl -X POST http://localhost:5000/analyze \
     -H "Content-Type: application/json" \
     -H "X-GitHub-Token: YOUR_GITHUB_TOKEN" \
     -H "X-Gemini-API-Key: YOUR_GEMINI_KEY" \
     -d '{"repo_url": "https://github.com/example/my-project"}'
```
