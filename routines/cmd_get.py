from datetime import datetime

from .history_types import BuildID
from .validation import build_validation, branch_validation
from .consts import *
from .configs import *
from .get_data import get_all_branches, get_build_info, get_branch_comment
from .files import clear_working_dir
from .zip import extract_zip_to
from .cmd_add import add_branch, add_build


@branch_validation
@build_validation
def get_build(build_id: BuildID, nobackup=False):

    # Резервная копия
    if nobackup == False:
        
        # Поиск ветки для резервного копирования
        branches = get_all_branches()
        found_branch = None
        for branch in branches:
            if get_branch_comment(branch) == BACKUP_COMMENT:
                found_branch = branch
                break

        # Если не найдена - создать ответвление от Сборки №1 Ветки №1
        if found_branch is None:
            parent = BuildID(1, 1)
            found_branch = add_branch(parent=parent, ovrd_comment=BACKUP_COMMENT)

        # Добавление резервной копии рабочей папки в виде сборки
        add_build(found_branch, ovrd_comment='backup ' + datetime.strftime(datetime.now(), '%d.%m.%Y %H-%M-%S'),
                  ovrd_extcomment=f'Резервная копия рабочей директории \nот {datetime.strftime(datetime.now(), '%d.%m.%Y %H-%M-%S')}')
    
    # Очистка рабочей папки и развёртывание сборки
    clear_working_dir()
    info = get_build_info(build_id)
    extract_zip_to(f'{config['path']}{HISTORY}{info.filename}', config['path'])
    print(f'{TAB}Сборка {build_id.build} из ветки {build_id.branch} развёрнута в рабочей папке.')
    print(f'{TAB}В случае вложенности - вручную переместите содержимое новой папки в корень проекта.')