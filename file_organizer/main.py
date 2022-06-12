# Small script to organize your file into folders that match the file extention, you can customize your list of folder via list_of_directories variable.
# You can either run this script from designated folder without sys parameter or specify your folder via system parameter.

import os
import sys
from pathlib import Path

wd_specified = True

if len(sys.argv) == 1:
    wd_specified = False

list_of_directories = {
    'archive': ['.zip', '.rar', '.tar', '.gz', '.iso', '.7z'],
    'picture': ['.jpg', '.jpeg', '.png', '.gif', '.tiff'],
    'pdf': ['.pdf'],
    'design': ['.svg', '.ai'],
    'doc': ['.doc', '.docx', '.csv', '.xls', '.xlsx', '.ppt', '.pptx'],
    'audio': ['.mp3', '.wav', '.wma', 'acc'],
    'video': ['.mpeg', '.mp4'],
    'exe': ['.exe', '.msi', '.apk', '.deb']
}

file_format_dictionary = {
      final_file_format: directory
      for directory, file_format_stored in list_of_directories.items()
      for final_file_format in file_format_stored
}

if wd_specified:
    working_directory = Path(sys.argv[1])
else:
    working_directory = Path('.')

dir_entries = os.scandir(working_directory)

for entry in dir_entries:
    if entry.is_dir():
        continue
    
    file_path = Path(entry)

    if (not wd_specified) & (file_path.name == sys.argv[0]):
        continue

    file_format = file_path.suffix.lower()
    if file_format in file_format_dictionary:
        target_directory = working_directory / file_format_dictionary[file_format]
    else:
        target_directory = working_directory / 'others'

    os.makedirs(target_directory, exist_ok=True)
    os.rename(file_path, target_directory/file_path.name)
       

