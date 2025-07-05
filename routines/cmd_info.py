from .history_types import BuildID
from .validation import build_validation, branch_validation
from .get_data import get_build_info, get_branch_info, get_parents
from .consts import *
from .configs import *

@branch_validation
@build_validation
def build_info(build_id: BuildID):
    build_info = get_build_info(build_id)
    print()
    print(f'{TAB}Подробная информация о сборке {build_id.build} из ветки {build_id.branch}:')
    print(f'{TAB}Имя файла:', build_info.filename)
    print(f'{TAB}Версия прошивки:', build_info.firmware_ver)
    print(f'{TAB}Комментарий', build_info.comment)
    print(f'{TAB}Подробный комментарий:')
    build_info.ext_comment = f'{TAB}{TAB}' + build_info.ext_comment
    build_info.ext_comment = build_info.ext_comment.replace('\n', f'\n{TAB}{TAB}')
    print(build_info.ext_comment)
    print()
    print(f'{TAB}Хэш:', build_info.hash)

@branch_validation
def branch_info(branch: int):
    branch_info = get_branch_info(branch)
    parents = get_parents(branch)
    print()
    print(f'{TAB}Ветка:', branch_info.branch, ' ', 'Комментарий:', branch_info.info)
    print(f'{TAB}Родители ветки:')
    if len(parents) == 0:
        print(f'{TAB}{TAB}Ветка не имеет родителей')
    else:
        for parent in parents:
            print(f'{TAB}{TAB}Ветка {parent.branch}, сборка {parent.build}')