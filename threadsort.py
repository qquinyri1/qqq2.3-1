import os 
import re
from transliterate import translit
from concurrent.futures import ThreadPoolExecutor
import time

def normalize(text):
    return re.sub(r'[^a-zA-Z0-9]', '_', translit(text, 'ru', reversed=True))

def create_folders(destination):
    folders = ['images', 'video', 'documents', 'audio', 'archives']
    for folder in folders:
        os.makedirs(os.path.join(destination, 'sorted', folder), exist_ok=True)

def move_file(file_path, destination, folder):
    base_name = os.path.basename(file_path)
    new_name = normalize(base_name[:base_name.rfind('.')]) + base_name[base_name.rfind('.'):]
    new_file_path = os.path.join(destination, 'sorted', folder, new_name)
    os.rename(file_path, new_file_path)

def process_folder(item_path, destination):
    if os.path.isfile(item_path):
        ext = os.path.splitext(item_path)[1]
        if ext in {'.jpeg', '.png', '.jpg', '.svg'}:
            move_file(item_path, destination, 'images')
        elif ext in {'.avi', '.mp4', '.mov', '.mkv'}:
            move_file(item_path, destination, 'video')
        elif ext in {'.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'}:
            move_file(item_path, destination, 'documents')
        elif ext in {'.mp3', '.ogg', '.wav', '.amr'}:
            move_file(item_path, destination, 'audio')
        elif ext in {'.zip', '.gz', '.tar'}:
            move_file(item_path, destination, 'archives')
    elif os.path.isdir(item_path):
        new_subpath = os.path.join(destination, 'sorted', normalize(os.path.basename(item_path)))
        os.rename(item_path, new_subpath)
        sub_items = os.listdir(new_subpath)
        if sub_items:
            for sub_item in sub_items:
                sub_item_path = os.path.join(new_subpath, sub_item)
                process_folder(sub_item_path, destination)
            if not os.listdir(new_subpath):
                os.rmdir(new_subpath)
        else:
            os.rmdir(new_subpath)

def main_sort(target_directory):
    start_time = time.time()
    create_folders(target_directory)
    
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        for item in os.listdir(target_directory):
            item_path = os.path.join(target_directory, item)
            executor.submit(process_folder, item_path, target_directory)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total time taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    target_directory = "C:\Новая папка"
    main_sort(target_directory)
