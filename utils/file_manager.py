from pathlib import Path

def save_results(repo_name, readme_content, test_content, code_files):
    output_dir = Path(f"output_{repo_name}")
    output_dir.mkdir(exist_ok=True)

    # Save README
    with open(output_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"README saved to {output_dir}/README.md")

    ext = ".txt"


    test_filename = f"test_generated{ext}"
    
    # Save Tests
    with open(output_dir / test_filename, "w", encoding="utf-8") as f:
        f.write(test_content)
    print(f"Test file saved to {output_dir}/{test_filename}")