import os
import tempfile
import shutil
import zipfile
from dataclasses import astuple

from .db import exec_sql, commit
from .history_types import BuildID, BuildInfo
from .validation import branch_validation, parent_validation
from .consts import *
from .configs import *
from .get_data import get_new_build, get_last_branch
from .files import get_firmware_ver, get_md5, get_ext_comment, get_hexfile, make_build_filename
from .zip import make_zip, get_ext_comment_from_zip, extract_zip_to


@parent_validation
def add_branch(parent: BuildID=None, ovrd_comment=None) -> int:
    # Назначение переопределённого комментария
    if ovrd_comment is None:
        comment = input('Введите комментарий для новой ветки: ')
    else:
        comment = ovrd_comment
    
    # Добавление ветки
    exec_sql('INSERT INTO branches VALUES(NULL, ?);', (comment,))
    commit()
    branch = get_last_branch()
    print(f'{TAB}Создана ветка №{branch}')

    # Добавление информации о родителе
    if parent is not None:
        exec_sql('INSERT INTO parents VALUES (?, ?, ?);', (branch, parent.branch, parent.build))
        commit()
    return branch

@branch_validation
def add_build(branch: int, compression_level: int=zipfile.ZIP_DEFLATED, ovrd_comment: str = None, ovrd_extcomment: str = None):
    # Получение информации о сборке
    new_build = BuildInfo()
    new_build.branch = branch
    new_build.build = get_new_build(branch)
    new_build.comment = input('Введите краткий комментарий для новой сборки: ') if ovrd_comment is None else ovrd_comment
    new_build.ext_comment = get_ext_comment() if ovrd_extcomment is None else ovrd_extcomment
    new_build.firmware_ver = get_firmware_ver(config['hexfile'])
    new_build.filename = make_build_filename(new_build)

    # Создание zip-архива сборки
    make_zip(new_build, compression_level=compression_level)
    print(f'{TAB}Файл {new_build.filename} создан')
    new_build.hash = get_md5(f'{config['path']}{HISTORY}{new_build.filename}')

    # Запись информации о сборке в базу
    exec_sql('INSERT INTO history VALUES(?, ?, ?, ?, ?, ?, ?)', astuple(new_build))
    commit()
    print(f'{TAB}В ветку №{branch} добавлена сборка №{new_build.build}')

@branch_validation
def add_build_from_file(branch: int, filename: str):
    # Подготовка информации о сборке
    new_build = BuildInfo()
    new_build.branch = branch
    new_build.build = get_new_build(branch)
    new_build.comment = input('Введите краткий комментарий для новой сборки: ')
    
    # Распаковка во временную папку
    tmp_dir = tempfile.gettempdir() + '\\' + HISTORY_TMP
    extract_zip_to(filename, tmp_dir)

    # Получение информации о сборке из архива  и удаление временных файлов
    new_build.ext_comment = get_ext_comment_from_zip(filename)
    hexfile = get_hexfile(tmp_dir)
    new_build.firmware_ver = get_firmware_ver(hexfile)
    new_build.filename = make_build_filename(new_build)
    new_build.hash = get_md5(filename)
    shutil.rmtree(tmp_dir, ignore_errors=True)

    # Копирование файла сборки в хранилище
    shutil.copyfile(filename, f'{config['path']}{HISTORY}{new_build.filename}')
    print(f'{TAB}Файл {new_build.filename} создан (импортирован из {os.path.basename(filename)})')

    # Запись информации о сборке в базу
    exec_sql('INSERT INTO history VALUES(?, ?, ?, ?, ?, ?, ?)', astuple(new_build))
    commit()
    print(f'{TAB}В ветку №{branch} добавлена сборка №{new_build.build}')

