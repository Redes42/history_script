import os
import tempfile
import shutil

from .history_types import BuildID
from .validation import build_validation, branch_validation
from .consts import *
from .configs import *
from .get_data import get_build_info
from .files import get_hexfile, get_path
from .zip import extract_zip_to


@branch_validation
@build_validation
def export_build(build_id: BuildID):
    # Выбор папки для экспорта
    export_path = get_path(dialog_title='Укажите папку для экспорта сборки')

    # Распаковка сборки в папку экспорта
    zip_filename = f'{config['path']}{HISTORY}{get_build_info(build_id).filename}'
    extract_zip_to(zip_filename, export_path)
    print(f'{TAB}Сборка №{build_id.build} из ветки №{build_id.branch} экспортирована в "{export_path}"')


@branch_validation
@build_validation
def export_build_hex(build_id: BuildID):
    # Получение информации о сборке
    build_info = get_build_info(build_id)

    # Распаковка сборки во временную папку
    zip_filename =  f'{config['path']}{HISTORY}{build_info.filename}'
    tmp_dir = tempfile.gettempdir() + '\\' + HISTORY_TMP
    extract_zip_to(zip_filename, tmp_dir)

    # Выбор папки для экспорта
    export_path = get_path(dialog_title='Укажите папку для экспорта сборки')
    hexfile = get_hexfile(tmp_dir)
    shutil.copyfile(hexfile, f'{export_path}/{config['project_name']} [{build_info.firmware_ver}]')

    # Удаление временных файлов
    shutil.rmtree(tmp_dir)
    print(f'{TAB}Сборка №{build_id.build} из ветки №{build_id.branch} экспортирована (в виде HEX-файла) в "{export_path}"')


@branch_validation
@build_validation
def export_build_zip(build_id: BuildID):
    # Выбор папки для экспорта
    export_path = get_path(dialog_title='Укажите папку для экспорта сборки')

    # Копирование сборки в папку экспорта
    zip_filename = f'{config['path']}{HISTORY}{get_build_info(build_id).filename}'
    shutil.copyfile(zip_filename, f'{export_path}/{os.path.basename(zip_filename)}')
    print(f'{TAB}Сборка №{build_id.build} из ветки №{build_id.branch} экспортирована (в виде ZIP-архива) в "{export_path}"')