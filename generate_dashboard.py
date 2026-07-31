import os
import json

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def scan_files():
    all_files = []
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip hidden directories like .github or .git
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith(".html") and file != "index.html":
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, ROOT_DIR).replace("\\", "/")
                
                parts = rel_path.split("/")
                # Folder path parts excluding the file name
                folder_parts = parts[:-1] 
                
                clean_title = (
                    os.path.splitext(file)[0]
                    .replace("-", " ")
                    .replace("_", " ")
                    .title()
                )
                
                all_files.append({
                    "title": clean_title,
                    "path": rel_path,
                    "folders": folder_parts  # Array of nested folder names e.g. ["MCQ", "Maths", "Algebra"]
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
        print(f"✅ Indexed {len(file_list)} files matching exact folder hierarchy.")
    else:
        print("❌ Error: AUTO-GENERATED markers missing in index.html!")

if __name__ == "__main__":
    files = scan_files()
    update_index_html(files)
