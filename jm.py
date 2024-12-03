import os
import shutil
import zipfile
import requests
from termcolor import colored

# 获取当前工作目录
current_directory = os.getcwd()

zip_folder = f'{current_directory}\\zip\\'                # 压缩包文件夹
target_folder = f'{current_directory}\\target\\'            # 目标文件夹
extract_to_dir = f'{current_directory}\\extract_to_dir\\'   # 解压文件夹

if not os.path.exists(zip_folder):
    os.makedirs(zip_folder)
if not os.path.exists(target_folder):
    os.makedirs(target_folder)
if not os.path.exists(extract_to_dir):
    os.makedirs(extract_to_dir)

with open('Error_Zip.txt', 'w') as file:
    file.writelines("")
with open('Error_JM.txt', 'w') as file:
    file.writelines("")

def get_all_files(directory, is_file):
    items = os.listdir(directory)
    res = []
    if is_file == True:
        res = [item for item in items if os.path.isfile(os.path.join(directory, item))]
    else:
        res = [item for item in items if os.path.isdir(os.path.join(directory, item))]
    return res

def func(jm_ids):

    for jm in jm_ids:
        url = f"https://18comic-dwo.vip/album/{jm}"
        r = requests.get(url)
        if r.status_code != 200:
            print(colored(f"unfound html: {url}", 'red'))
            continue
        author = "btn btn-sm phone-author-tag  btn-primary"
        start_index = r.text.find(author)
        if (start_index == -1):
            with open('Error_JM.txt', 'a') as file:
                file.writelines(f"{jm}\n")
            print(colored(f"unfound {jm}", 'red'))
            continue

        name = ""
        check = False
        for i in range(start_index, len(r.text)):
            c = r.text[i]
            if c == '<': break
            if (check): name += c
            if c == '>': check = True

        file_path = f"{extract_to_dir}{jm}"
        folder_path = f"{target_folder}{name}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        old_folder = f"{folder_path}\\{jm}"
        if os.path.exists(old_folder):
            if os.path.isdir(old_folder):
                shutil.rmtree(old_folder)
            else:
                raise ValueError(colored(f"Unsupported file type at {old_folder}", 'red'))
    
        # 移动文件
        try:
            shutil.move(file_path, folder_path)
            print(colored(f"File moved from {file_path} to {folder_path}", 'green'))
        except Exception as e:
            print(colored(f"An error occurred: {e}", 'red'))

def safe_extract(zip_file, path):
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(path)
        print(colored(f"Successfully extracted {zip_file} to {path}", 'green'))
        return
    except zipfile.BadZipFile:
        print(colored(f"Error: {zip_file} is not a valid ZIP file.", 'red'))
    except zipfile.LargeZipFile:
        print(colored(f"Error: {zip_file} is too large (ZIP64 extension required).", 'red'))
    except PermissionError:
        print(colored(f"Error: Permission denied when trying to extract {zip_file}.", 'red'))
    except FileNotFoundError:
        print(colored(f"Error: The file {zip_file} was not found.", 'red'))
    except Exception as e:
        print(colored(f"An unexpected error occurred: {e}", 'red'))
    with open('Error_Zip.txt', 'a') as file:
        file.writelines(f"{zip_file}\n")

for filename in get_all_files(zip_folder, True):
    name, ext = os.path.splitext(filename)
    safe_extract(f"{zip_folder}{filename}", f"{extract_to_dir}{name}")

all_file = get_all_files(extract_to_dir, False)
func(all_file)
