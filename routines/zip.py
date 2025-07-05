import sys
import os
import time
from zipfile import ZipFile
import zipfile

from .consts import *
from .configs import *
from .files import get_file_sizes, get_files_and_dirs
from .history_types import BuildInfo
from .progress_bar import update_progress_bar


def make_zip(build_info: BuildInfo, compression_level: int = zipfile.ZIP_DEFLATED):
    # Получение файлов и их размеров
    files = get_files_and_dirs(config['path'])
    file_sizes = get_file_sizes(files)
    total_size = sum(file_sizes)

    # Сжатие в архив
    with ZipFile(f'{config['path']}{HISTORY}{build_info.filename}', mode='w', compression=compression_level) as zf:
        zf.comment = bytes(build_info.ext_comment, encoding='cp1251')   
        print(f'{TAB}Идёт создание zip-архива...')            
        processed_size = 0
        for file, size in zip(files, file_sizes):
            arcname = os.path.relpath(file, f'{config['project_name']}')
            zf.write(file, arcname=arcname)
            processed_size += size
            percent = (processed_size*100) // total_size
            update_progress_bar(percent)
        print()

def get_ext_comment_from_zip(filename: str):
    with ZipFile(filename, mode='r') as zf:
        ext_comment = zf.comment.decode(encoding='cp1251')
    return ext_comment


def set_ext_comment_to_zip(filename: str, new_ext_comment: str):
    with ZipFile(filename, mode='a') as zf:
        zf.comment = bytes(new_ext_comment, encoding='cp1251') 


def extract_zip_to(filename: str, path: str):
    with ZipFile(filename, mode='r') as zf:
        # Распаковка
        zf.extractall(path)

        # Корректировка даты модификации
        for zipinfo in zf.infolist():
            date_time = time.mktime(zipinfo.date_time + (0, 0, -1))
            name = os.path.join(path, zipinfo.filename)
            os.utime(name, (date_time, date_time))
            #os.rename(name, name.encode('cp437').decode('cp866'))
