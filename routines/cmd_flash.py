import shutil
import subprocess
import tempfile

from .history_types import BuildID
from .validation import build_validation, branch_validation
from .consts import *
from .configs import *
from .get_data import get_build_info
from .files import get_project_file
from .zip import extract_zip_to


@branch_validation
@build_validation
def flash_build(build_id: BuildID, compile=False):
    # Подготовка информации и путей
    info = get_build_info(build_id)
    filename = f'{config['path']}{HISTORY}{info.filename}'
    tmp_dir = tempfile.gettempdir() + '\\history_tmp\\'

    # Извлечение сборки во временную папку
    extract_zip_to(filename, tmp_dir)

    # Запуск пересборки и прошивки
    project_file_name = get_project_file(tmp_dir)
    if compile:
        print(f'{TAB}Идёт компиляция проекта...')
        build_process = subprocess.Popen(f'C:\\Keil_v5\\UV4\\UV4.exe -b "{project_file_name}" -j0')
        build_process.wait()
    print(f'{TAB}Идёт прошивка контроллера...')
    flash_process = subprocess.Popen(f'C:\\Keil_v5\\UV4\\UV4.exe -f "{project_file_name}" -j0 -o flash.log')
    flash_process.wait()

    # Получение результата прошивки
    result = 'failed'
    with open(tmp_dir + 'flash.log', mode='r', encoding='UTF-8') as file:
        result = file.read()
    shutil.rmtree(tmp_dir, ignore_errors=True)
    if 'failed' not in result:
        print(f'{TAB}Сборка {build_id.build} из ветки {build_id.branch} успешно прошита в контроллер.')
    else:
        print(f'{TAB}Ошибка прошивки сборки {build_id.build} из ветки {build_id.branch} контроллер.')
