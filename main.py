import sys
import re
import os
import shutil
from transliterate import translit
from pathlib import Path


path = Path(sys.argv[1])


def normalize(name: str) -> str:
    trans_name = translit(name, reversed=True)
    clean_name = re.sub(r'[^a-zA-Z0-9]+', '_', trans_name)
    return clean_name


file_types = {
    'JPEG': 'images',
    'PNG': 'images',
    'JPG': 'images',
    'SVG': 'images',
    'AVI': 'video',
    'MP4': 'video',
    'MOV': 'video',
    'MKV': 'video',
    'DOC': 'documents',
    'DOCX': 'documents',
    'TXT': 'documents',
    'PDF': 'documents',
    'XLSX': 'documents',
    'PPTX': 'documents',
    'MP3': 'audio',
    'OGG': 'audio',
    'WAV': 'audio',
    'AMR': 'audio',
    'ZIP': 'archives',
    'GZ': 'archives',
    'TAR': 'archives'
}


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def get_subfolders_paths(folder_path) -> list:
    subfolder_path = [f.path for f in os.scandir(folder_path) if f.is_dir()]

    return subfolder_path


def get_file_paths(folder_path) -> list:
    file_path = [f.path for f in os.scandir(folder_path) if not f.is_dir()]

    return file_path


def get_file_names(folder_path) -> list:
    file_path = [f.path for f in os.scandir(folder_path) if not f.is_dir()]
    file_names = [os.path.split(f)[-1] for f in file_path]

    return file_names


def extract_and_move_archive(archive_path, destination_folder):

    archive_name = os.path.splitext(os.path.basename(archive_path))[0]
    subfolder_path = os.path.join(destination_folder, archive_name)
    create_folder_if_not_exists(subfolder_path)

    try:
        shutil.unpack_archive(archive_path, subfolder_path)
        return True
    except Exception as e:
        print(f"Error extracting {archive_path}: {e}")
        return False


def sort_file(folder_path):
    file_paths = get_file_paths(folder_path)
    for file_path in file_paths:
        extension = file_path.split('.')[-1]
        file_name = os.path.split(file_path)[-1]

        for ext, folder in file_types.items():
            if extension.upper() == ext:
                print(f'Moving {file_name} in {folder} folder\n')
                new_path = os.path.join(path, folder, file_name)
                create_folder_if_not_exists(os.path.join(path, folder))

                if folder == 'archives':
                    if extract_and_move_archive(file_path, os.path.join(path, folder)):
                        os.remove(file_path)
                else:
                    os.rename(file_path, new_path)


if __name__ == "__main__":
    sort_file(path)
