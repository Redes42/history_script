import os
import pathlib
import tempfile
import stat
import subprocess
from tkinter import filedialog
from datetime import datetime as dt
from hashlib import md5

from .consts import *
from .configs import *
from .progress_bar import update_progress_bar
from .history_types import BuildInfo


def is_in_ignore_list(base: str, file_or_dir: str) -> bool:
    for ignore_item in config['ignore_list']:
        if ignore_item in os.path.join(base, file_or_dir):
            return True
    return False


def get_files_and_dirs(path: str):
    objects = []
    for base, dirs, files in os.walk(path):
        for file in files:
            if not is_in_ignore_list(base, file):
                objects.append(os.path.join(base, file))
        for dir in dirs:
            if not is_in_ignore_list(base, dir):
                objects.append(os.path.join(base, dir))
    return objects


def get_file_sizes(files: tuple[str] | list[str]):
    file_sizes = [os.path.getsize(file) for file in files]
    return file_sizes


def get_md5(filename: str):
    hash_md5 = md5()
    processed_size = 0
    chunk_size = 4096
    zip_size = os.path.getsize(filename)
    print(f'{TAB}Идёт вычисление контрольной суммы...')      
    with open(filename, "rb") as file:
        for chunk in iter(lambda: file.read(chunk_size), b""):
            hash_md5.update(chunk)
            processed_size += chunk_size
            percent = (processed_size*100) // zip_size
            update_progress_bar(percent)
        print()
    return hash_md5.hexdigest()


def delete_build_file(filename: str):
    if os.path.exists(filename):
        os.remove(filename)
        print(f'{TAB}Удалён файл "{os.path.basename(filename)}"')


def get_hexfile(override_path: str = None):
    objects_path = f'{config['path']}{OBJECTS}'

    # Переопределение пути по умолчанию
    if override_path is not None:
        objects_path = override_path + '\\'

        # Для сборок, которые упакованы папкой - добавить имя папки к пути
        if os.path.exists(f'{objects_path}{OBJECTS}'):
            objects_path += OBJECTS
        else:
            proj_dir = os.listdir(objects_path)[0] + '\\'
            objects_path += f'{proj_dir}{OBJECTS}'
    hexfiles = []
    hexfile = '?'
    
    # Поиск hex-файлов
    if os.path.exists(objects_path):
        dir_contents = os.listdir(objects_path)
        for file in dir_contents:
            if '.hex' in file:
                hexfiles.append(file)
    if len(hexfiles) == 1:
        hexfile = objects_path + hexfiles[0]
    else:
        while not os.path.exists(hexfile):
            hexfile = filedialog.askopenfilename(initialdir=objects_path, title='Выберите hex-файл', filetypes=(("HEX-файлы", ".hex"),))
    return hexfile


def get_ext_comment(old_ext_comment: str = None):
    ext_comment = ''
    tmp_filename = tempfile.gettempdir() + '\\Введите_расширенный_комментарий_для_сборки,_сохраните_файл_и_закройте_редактор.txt'
    with open(tmp_filename, 'w', encoding='UTF-8') as tmp_file:
        if old_ext_comment is not None:
            tmp_file.write(old_ext_comment)
    doc = subprocess.Popen(["start", "/WAIT", tmp_filename], shell=True)
    doc.wait()
    with open(tmp_filename, 'r', encoding='UTF-8') as ext_comment_file:
        ext_comment = ext_comment_file.read()
    os.remove(tmp_filename)
    return ext_comment


def get_path(dialog_title='Выберите папку проекта', dir='.'):
    path = '?'
    while not os.path.exists(path):
        path = filedialog.askdirectory(initialdir=dir, mustexist=True, title=dialog_title)
    return path


def get_firmware_ver(hexpath: str):
    fw_dt = dt.fromtimestamp(pathlib.Path(hexpath).stat().st_mtime)
    firmware_ver = hex(fw_dt.year).upper()[2:] + hex(fw_dt.month).upper()[2:] + hex(fw_dt.day).upper()[2:] + hex(fw_dt.hour*60 + fw_dt.minute).upper()[2:]
    return firmware_ver


def get_project_file(path: str):
    project_files = []
    project_file = '?'
    
    # Для сборок, которые упакованы папкой - добавить имя папки к пути
    if not os.path.exists(f'{path}{OBJECTS}'):
        proj_dir = os.listdir(path)[0] + '\\'
        path += proj_dir

    # Поиск файлов проекта
    if os.path.exists(path):
        dir_contents = os.listdir(path)
        for file in dir_contents:
            if '.uvprojx' in file:
                project_files.append(file)
    if len(project_files) == 1:
        project_file = path + project_files[0]
    else:
        while not os.path.exists(project_file):
            project_file = filedialog.askopenfilename(initialdir=path, title='Выберите файл проекта', filetypes=(("Файлы проектов Keil uVision (.uvprojx)", ".uvprojx"),))
    return project_file


def get_zip_file():
    zip_filename = filedialog.askopenfilename(initialdir=config['path'], title='Выберите zip-файл', filetypes=(("ZIP-файлы", ".zip"),))
    return zip_filename


def clear_working_dir():
    for base, dirs, files in os.walk(config['path'], topdown=False):
        for name in files:
            if not is_in_ignore_list(base, name):
                os.chmod(os.path.join(base, name), stat.S_IWRITE)
                os.remove(os.path.join(base, name))
        for name in dirs:
            if not is_in_ignore_list(base, name):      
                os.chmod(os.path.join(base, name), stat.S_IWRITE)            
                os.rmdir(os.path.join(base, name))


def make_build_filename(build_info: BuildInfo):
    result = f'{str(build_info.branch).zfill(2)}.{str(build_info.build).zfill(2)} - {config['project_name']} [{build_info.firmware_ver}] - {build_info.comment}.zip'
    return result