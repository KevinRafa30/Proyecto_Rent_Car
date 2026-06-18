import os
import glob
import re

base_dir = r'C:\Users\kevin\ProyectoRentCar\templates'
list_files = glob.glob(os.path.join(base_dir, '**', '*_list.html'), recursive=True)

# 1. Update rentas/renta_list.html and inspecciones/inspeccion_list.html to remove the icon container
for file_path in list_files:
    if 'renta_list.html' in file_path or 'inspeccion_list.html' in file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove the <div class="p-2.5 bg-indigo-50..."><i class="..."></i></div>
        content = re.sub(r'<div class=\"[^\"]*bg-indigo-50[^\"]*\">.*?</div>', '', content, flags=re.DOTALL)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

# 2. Add text to edit and delete buttons in all list files
for file_path in list_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The edit button looks like:
    # <a href="..." class="text-slate-400 hover:text-indigo-600 transition" title="Editar">
    #     <i class="fa-solid fa-pencil-simple text-base"></i>
    # </a>
    # Wait, FontAwesome edit icon is fa-pen or fa-pencil or fa-pen-to-square
    # Actually, in the last commit I replaced ph-pencil-simple with fa-solid fa-pencil-simple (Wait, FA doesn't have fa-pencil-simple, maybe fa-pen).
    # Wait! Let's check what it currently says!
    pass
