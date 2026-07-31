import os
import json
import re

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def scan_files():
    all_files = []
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # Ignore hidden directories like .github or .git
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        # Sort files alphabetically so 01-, 02-, 03- load in strict numerical order
        files.sort()
        
        for file in files:
            if file.endswith(".html") and file != "index.html":
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, ROOT_DIR).replace("\\", "/")
                
                parts = rel_path.split("/")
                folder_parts = parts[:-1]
                
                # Extract filename without extension
                raw_filename = os.path.splitext(file)[0]
                
                # STRIP NUMBER PREFIX (e.g., "01-Minerals Part 1" -> "Minerals Part 1")
                # Removes leading digits followed by hyphens, underscores, or spaces
                clean_filename = re.sub(r'^\d+[\s\-_]*', '', raw_filename)
                
                # Format to Clean Title Case
                clean_title = (
                    clean_filename
                    .replace("-", " ")
                    .replace("_", " ")
                    .title()
                )
                
                all_files.append({
                    "title": clean_title,
                    "path": rel_path,
                    "folders": folder_parts
                })
                
    return all_files

def update_index_html(file_list):
    index_path = os.path.join(ROOT_DIR, "index.html")
    
    if not os.path.exists(index_path):
        print("❌ Error: index.html not found!")
        return
        
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    json_data = json.dumps(file_list, indent=2)
    start_marker = "// AUTO-GENERATED-START"
    end_marker = "// AUTO-GENERATED-END"
    
    if start_marker in content and end_marker in content:
        before = content.split(start_marker)[0]
        after = content.split(end_marker)[1]
        new_content = f"{before}{start_marker}\n    const fileTree = {json_data};\n    {end_marker}{after}"
        
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅ Indexed {len(file_list)} files with clean prefix stripping.")
    else:
        print("❌ Error: AUTO-GENERATED markers missing in index.html!")

if __name__ == "__main__":
    files = scan_files()
    update_index_html(files)
