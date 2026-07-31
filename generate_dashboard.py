import os
import json

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def scan_quizzes():
    quizzes = []
    
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            # Skip non-HTML files, index.html, and hidden dot-folders like .github
            if file.endswith(".html") and file != "index.html" and not root.startswith(os.path.join(ROOT_DIR, ".")):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, ROOT_DIR).replace("\\", "/")
                
                parts = rel_path.split("/")
                subject = parts[1] if len(parts) > 1 else "General"
                tag = parts[2] if len(parts) > 3 else subject
                
                clean_title = (
                    os.path.splitext(file)[0]
                    .replace("-", " ")
                    .replace("_", " ")
                    .title()
                )
                
                quizzes.append({
                    "title": clean_title,
                    "path": rel_path,
                    "subject": subject.replace("-", " ").replace("_", " ").title(),
                    "tag": tag.replace("-", " ").replace("_", " ").title()
                })
                
    return quizzes

def update_index_html(quiz_list):
    index_path = os.path.join(ROOT_DIR, "index.html")
    
    if not os.path.exists(index_path):
        print("❌ Error: index.html not found!")
        return
        
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    json_data = json.dumps(quiz_list, indent=2)
    start_marker = "// AUTO-GENERATED-START"
    end_marker = "// AUTO-GENERATED-END"
    
    if start_marker in content and end_marker in content:
        before = content.split(start_marker)[0]
        after = content.split(end_marker)[1]
        new_content = f"{before}{start_marker}\n    const autoScannedQuizzes = {json_data};\n    {end_marker}{after}"
        
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅ Successfully indexed {len(quiz_list)} static quiz files.")
    else:
        print("❌ Error: AUTO-GENERATED markers missing in index.html!")

if __name__ == "__main__":
    quizzes = scan_quizzes()
    update_index_html(quizzes)
