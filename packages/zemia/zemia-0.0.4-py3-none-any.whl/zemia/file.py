'''
Used to edit files and folders.
'''

import shutil
import os

def test_folder(location: str, location_is_file: bool = True) -> None:
    '''
    Looks for a folder and creates it if it does not already exist.
    '''
    folder = location
    if location_is_file:
        if location.rfind("/") > -1:
            folder = location[0:location.rfind("/")]

    folder_hierarchy = folder.split("/")
    # Check top level folder
    folder = folder_hierarchy[0]
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Check subfolders
    for i in range(len(folder_hierarchy)):
        folder = "/".join(folder_hierarchy[0:i+1])
        if not os.path.exists(folder):
            os.makedirs(folder)

def delete_contents(location: str, del_files: bool = True, del_folders: bool = True) -> None:
    '''
    Location must be a folder.\n
    Deletes all files and folders inside the specified folder, unless the optional parameters specify otherwise.
    '''
    for root, dirs, files in os.walk(location):
        if del_files:
            for f in files:
                os.unlink(os.path.join(root, f))
        if del_folders:
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

def delete(location: str) -> None:
    '''
    Deletes a file or folder.
    '''
    if os.path.isfile(location):
        os.remove(location)
    elif os.path.isdir(location):
        shutil.rmtree(location)
    else:
        print(f"Warning: {location} file/folder not found")

def copy(source: str, destination: str) -> None:
    '''
    Copies a file from source to destination.
    '''
    test_folder(destination)
    shutil.copy(source, destination)

def batch_copy(source_folder: str, dest_folder: str, files: str|list) -> None:
    '''
    Copies a list of files from source_folder to dest_folder.
    '''
    if isinstance(files, str):
        files = [files]
    for f in files:
        copy(f"{source_folder}/{f}", f"{dest_folder}/{f}")

def move(source: str, destination: str) -> None:
    '''
    Moves a file from source to destination.
    '''
    test_folder(destination)
    shutil.move(source, destination)

def read(location: str, codec, split = True) -> list[str]: # utf-8-sig
    '''
    Opens a file and reads the contents into a list of strings (or a single string in a len 1 list, if split is False).
    The file is then closed.\n
    codec can be used to change the encoding with which the file is read. Leave as "" for default.
    '''
    with open(location, "r", encoding = codec) as f:
        data = f.read()
    if split:
        data = data.split("\n")
    else:
        data = [data]
    return data

def write(location: str, data: str, codec) -> None: # cp1252 (<- ANSI for Windows)
    '''
    Creates a file, or overwrites it if it already exists, and writes the data to it.\n
    codec can be used to change the encoding with which the file is read. Leave as "" for default.
    '''
    test_folder(location)
    try:
        with open(location, "x", encoding = codec) as f:
            f.write(data)
    except FileExistsError as e:
        print(e)
        with open(location, "w", encoding = codec) as f:
            f.write(data)

def append(location: str, data: str, codec) -> None:
    '''
    Appends to an existing file, or creates a new file if it does not already exist, and writes the data to it.\n
    '''
    with open(location, "a", encoding = codec) as f:
        f.write(data)

def list_files(location: str) -> list[str]:
    '''
    Returns a list of all files in the specified folder.
    '''
    # Code found at https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    return [f for f in os.listdir(location) if os.path.isfile(os.path.join(location, f))]
