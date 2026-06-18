import os

base_dir = r'C:\Users\kevin\ProyectoRentCar'
ignore_dirs = ['.git', 'venv', '.gemini']

empty_dirs = []
empty_files = []
junk_files = []

junk_patterns = ['.pyc', '.bak', '.tmp', '.log']
known_temp_scripts = ['prepare.py', 'migrate_icons.py', 'update_icons.py', 'update_lists.py', 'check_sync.py', 'migrate2.py']

for root, dirs, files in os.walk(base_dir):
    # filter ignored directories
    dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('__pycache__')]
    
    if not os.listdir(root):
        empty_dirs.append(root)
        
    for f in files:
        full_path = os.path.join(root, f)
        rel_path = os.path.relpath(full_path, base_dir)
        
        try:
            if os.path.getsize(full_path) == 0:
                empty_files.append(rel_path)
        except OSError:
            pass
            
        if any(f.endswith(ext) for ext in junk_patterns):
            junk_files.append(rel_path)
            
        if f in known_temp_scripts and root == base_dir:
            junk_files.append(rel_path)

print("=== CARPETAS VACÍAS ===")
for d in empty_dirs: print(os.path.relpath(d, base_dir))

print("\n=== ARCHIVOS VACÍOS (0 bytes) ===")
for f in empty_files: print(f)

print("\n=== ARCHIVOS BASURA / TEMPORALES ===")
for f in junk_files: print(f)

