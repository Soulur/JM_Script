import os
import shutil
import requests

# 源文件夹下文件 移动到 指定文件夹
source_file = '/home/jm/comic/'
target_folder = '/home/jm/target/'
suffix = ".txt"

if not os.path.exists(target_folder):
    os.makedirs(target_folder)

def get_all_files(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    filenames = [os.path.splitext(f)[0] for f in files]
    return filenames

def func(jm_ids):

	for jm in jm_ids:
		url = f"https://18comic-dwo.vip/album/{jm}"
		r = requests.get(url)
		if r.status_code != 200:
			print("craw html:", url)
			continue
		start_index = r.text.find("btn btn-sm phone-author-tag  btn-primary")
		if (start_index == -1):
			continue

		name = ""
		check = False
		for i in range(start_index, len(r.text)):
			c = r.text[i]
			if c == '<': break
			if (check): name += c
			if c == '>': check = True

		file_path = f"{source_file}{jm}"
		folder_path = f"{target_folder}{name}{suffix}"

		if not os.path.exists(folder_path):
	    		os.makedirs(folder_path)

		shutil.move(file_path, folder_path)

all_file = get_all_files(source_file)
func(all_file)
