import sys, shutil, threading, time
from pathlib import Path
from unidecode import unidecode
from concurrent.futures import ThreadPoolExecutor as ThreadPool

CATEGORIES = {
    "Images": [".jpeg", ".png", ".jpg", ".svg", ".apng", ".avif", ".gif", ".jfif", ".pjpeg", ".pjp", ".svg", ".webp"],
    "Video": [".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv", ".vob", ".ogg"],
    "Documents": [".docx", ".txt", ".pdf", ".doc", ".xlsx", ".pptx"],
    "Audio": [".mp3", ".aiff", ".ogg", ".wav", ".amr"],
    "Archives": [".zip", ".tar", ".gz"]
}

def move_file(file: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        target_dir.mkdir(parents=True)
    file.replace(target_dir.joinpath(f"{unidecode(file.stem)}{file.suffix}"))

def sort_folder(path: Path) -> None:
    for item in path.glob("**/*"):
        if item.is_file():
            category = get_categories(item)
            move_file(item, path, category)
            
def delete_empty_folders(path: Path) -> None:
    for item in reversed(list(path.glob("**/*"))):
        if item.is_dir() and not any(item.iterdir()):
            item.rmdir()

def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"

def unpack_and_sort_archive(item: Path, sort: bool) -> None:
    file_ext = item.suffix.lower()
    for category, exts in CATEGORIES.items():
        if file_ext in exts and category == "Archives":
            archive_folder_name = item.stem
            unpack_path = item.parent / archive_folder_name
            unpack_path.mkdir(exist_ok=True)
            shutil.unpack_archive(str(item), extract_dir=str(unpack_path))
            sort_folder(unpack_path)
            delete_empty_folders(unpack_path)
            
def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        print("/// No path to folder")
        return
    
    if not path.exists():
        print(f"/// Folder {path} not found.")
        return

    confirmation = input(f"/// Are you sure you want to sort the files in folder {path}? (Y - Yes, N - No) >>> ")
    if confirmation.lower() != "y":
        print("/// Sorting aborted.")
        return

    start_time = time.time()
    sort_folder(path)
    delete_empty_folders(path)
    
    wait_sort = True

    while wait_sort:
        sort = input("/// Sort unpacked archives? (Y - Yes, N - No) >>> ")
        if sort.lower() == "y":
            with ThreadPool() as executor:
                archive_files = [item for item in path.glob("**/*") if item.is_file() and item.suffix.lower() in CATEGORIES["Archives"]]
                for item in archive_files:
                    executor.submit(unpack_and_sort_archive, item, True)
                wait_sort = False
        elif sort.lower() == "n":
            with ThreadPool() as executor:
                archive_files = [item for item in path.glob("**/*") if item.is_file() and item.suffix.lower() in CATEGORIES["Archives"]]
                for item in archive_files:
                    executor.submit(unpack_and_sort_archive, item, False)
                wait_sort = False

    end_time = time.time()
    elapsed_time = end_time - start_time

    completion_message = f"/// Sorting and unpacking completed in {elapsed_time:.2f} seconds."
    print(completion_message)
    
if __name__ == "__main__":
    main()