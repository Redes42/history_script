import tempfile
import shutil
import os
import zipfile

from .db import exec_sql, commit
from .history_types import BuildID, BuildInfo
from .validation import build_validation, branch_validation
from .consts import *
from .configs import *
from .zip import set_ext_comment_to_zip, get_ext_comment_from_zip, extract_zip_to, make_zip
from .files import get_ext_comment, get_md5, delete_build_file, get_hexfile, get_firmware_ver, make_build_filename
from .get_data import get_build_info

@branch_validation
def update_branch_comment(branch: int):
    new_comment = input('Введите новый краткий комментарий для существующей ветки: ')
    exec_sql(f'UPDATE branches SET comment = ? WHERE branch = {branch}', (new_comment,))
    commit()
    print(f'{TAB}Новый комментарий для ветки {branch} установлен')

@branch_validation
@build_validation
def update_build_comment(build_id: BuildID):
    new_comment = input('Введите новый краткий комментарий для существующей сборки: ')
    exec_sql(f'UPDATE history SET comment = ? WHERE branch = {build_id.branch} AND build = {build_id.build}', (new_comment,))
    commit()
    print(f'{TAB}Новый комментарий для сборки {build_id.build} из ветки {build_id.branch} установлен')

@branch_validation
@build_validation
def update_extcomment(build_id: BuildID):
    build_info = get_build_info(build_id)
    new_ext_comment = get_ext_comment(build_info.ext_comment)
    zip_filename = f'{config['path']}{HISTORY}{build_info.filename}'
    set_ext_comment_to_zip(zip_filename, new_ext_comment)
    build_info.hash = get_md5(zip_filename)
    exec_sql(f'UPDATE history SET ext_comment = ?, hash = ? WHERE branch = {build_id.branch} AND build = {build_id.build}',
             (new_ext_comment, build_info.hash))
    commit()
    print(f'{TAB}Новый расширенный комментарий для сборки {build_id.build} из ветки {build_id.branch} установлен')

@branch_validation
@build_validation
def update_build(build_id: BuildID, compression_level=zipfile.ZIP_DEFLATED):
    # Получение информации о сборке
    build_info = get_build_info(build_id)
    delete_build_file(f'{config['path']}{HISTORY}{build_info.filename}')
    build_info.firmware_ver = get_firmware_ver(config['hexfile'])
    build_info.filename = make_build_filename(build_info)

    # Создание zip-архива сборки
    make_zip(build_info, compression_level=compression_level)
    print(f'{TAB}Файл {build_info.filename} создан')
    build_info.hash = get_md5(f'{config['path']}{HISTORY}{build_info.filename}')

    # Запись информации о сборке в базу
    exec_sql(f'UPDATE history SET filename = ?, hash = ? WHERE branch = {build_id.branch} AND build = {build_id.build}',
             (build_info.filename, build_info.hash))
    commit()
    print(f'{TAB}Обновлена сборка №{build_info.build} в ветке №{build_id.branch}')

@branch_validation
@build_validation
def update_build_from_file(build_id: BuildID, filename: str):
    # Распаковка во временную папку:
    tmp_dir = tempfile.gettempdir() + '\\' + HISTORY_TMP
    extract_zip_to(filename, tmp_dir)

    # Получение существующей информации о сборке
    build_info = get_build_info(build_id)

    # Новый краткий комментарий
    tmp = input('Введите новый краткий комментарий для сборки (оставьте поле пустым для сохранения имеющегося): ').strip()
    if tmp != '':
        build_info.comment = tmp
    
    # Получение данных из импортируемого архива 
    build_info.ext_comment = get_ext_comment_from_zip(filename)
    hexfile = get_hexfile(tmp_dir)
    build_info.firmware_ver = get_firmware_ver(hexfile)
    build_info.filename = make_build_filename(build_info)
    build_info.hash = get_md5(filename)

    # Удаление старого файла сборки и копирование нового
    old_filename = build_info.filename
    delete_build_file(f'{config['path']}{HISTORY}{build_info.filename}')
    shutil.copyfile(filename, f'{config['path']}{HISTORY}{build_info.filename}')
    print(f'{TAB}Файл {old_filename} заменён (импортирован из {os.path.basename(filename)})')
    print(f'{TAB}Новое имя файла: {build_info.filename}')
    
    # Запись обновлённой информации в хранилище
    exec_sql(f'UPDATE history SET comment = ?, ext_comment = ?, hash = ?, firmware_ver = ?, filename = ? WHERE branch = {build_id.branch} AND build = {build_id.build}',
             (build_info.comment, build_info.ext_comment, build_info.hash, build_info.firmware_ver, build_info.filename))
    commit()  
    
    # Удаление файлов из временной папки
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print(f'{TAB}Сборка №{build_id.build} из ветки {build_id.branch} обновлена.')
