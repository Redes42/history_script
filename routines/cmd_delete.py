from .db import exec_sql, commit
from .history_types import BuildID
from .validation import build_validation, branch_validation
from .consts import *
from .configs import *
from .files import delete_build_file
from .cmd_add import add_branch
from .get_data import get_branch_count, get_children_branches, get_build_info

@branch_validation
def delete_branch(branch: int):
    # Отказ, если ветка не пустая
    children_count = get_children_branches(branch)
    if len(children_count) > 0:
        print(f'{TAB}Выбранная ветка содержит ответвления (потомков). Воспользуйтесь командой {REBASE} для их переноса в другие части дерева и освобождения текущей ветки.')
        print(f'{TAB}Также, можно воспользоваться командой {DELETE} для удаления дочерних веток.')
        return
    
    # Удаление файлов входящих сборок
    files = exec_sql(f'SELECT filename FROM history WHERE branch = {branch};')
    for file in files:
        delete_build_file(f'{config['path']}{HISTORY}{file[0]}')

    # Удаление ветки из базы
    exec_sql(f'DELETE FROM branches WHERE branch = {branch};')
    commit()

    # Создание ветки, если их не осталось
    branch_count = get_branch_count()
    print(f'{TAB}Удалена ветка №{branch} и все входящие сборки')
    if branch_count == 0:
        exec_sql('UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME = "branches";')
        print(f'{TAB}Удалена последняя ветка, автоматическое создание новой (должна быть хотя бы одна)...')
        add_branch()

@branch_validation
@build_validation
def delete_build(build_id: BuildID):
    filename = config['path'] + HISTORY + get_build_info(build_id).filename
    exec_sql(f'DELETE FROM history WHERE branch = {build_id.branch} AND build = {build_id.build};')
    commit()
    print(f'{TAB}Удалена сборка №{build_id.build} из ветки {build_id.branch}')
    delete_build_file(filename)

def delete_all():
    files = exec_sql('SELECT filename FROM history;')
    for file in files:
        delete_build_file(config['path'] + HISTORY + file[0])
    exec_sql(f'DROP TABLE IF EXISTS parents;')
    exec_sql(f'DROP TABLE IF EXISTS history;')
    exec_sql(f'DROP TABLE IF EXISTS branches;')
    commit()
    print(f'{TAB}Хранилище полностью очищено. Для повторного создания хранилища воспользуйтесь командой {CREATE}.')