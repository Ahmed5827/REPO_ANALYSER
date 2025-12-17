from pathlib import Path

def save_results(repo_name, readme_content, test_content, code_files):
    output_dir = Path(f"output_{repo_name}")
    output_dir.mkdir(exist_ok=True)

    # Save README
    with open(output_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"README saved to {output_dir}/README.md")

    # Determine test file extension
    ext = ".txt"
    if code_files:
        first_file = code_files[0]['name']
        if first_file.endswith('.py'):
            ext = ".py"
        elif first_file.endswith(('.js', '.ts')):
            ext = ".test.js"

    test_filename = f"test_generated{ext}"
    
    # Save Tests
    with open(output_dir / test_filename, "w", encoding="utf-8") as f:
        f.write(test_content)
    print(f"Test file saved to {output_dir}/{test_filename}")