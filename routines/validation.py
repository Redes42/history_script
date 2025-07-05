from .history_types import BuildID
from .db import exec_sql
from .consts import *


def branch_validation(func):
    def wrapper(*args, **kwargs):
        branch = args[0]
        if isinstance(branch, BuildID):
            branch = branch.branch
        branch_exists = False
        if branch is not None:
            branch_exists = (exec_sql(f'SELECT COUNT(*) FROM branches WHERE branch = {branch};').fetchone()[0] == 1)
        if branch_exists:
           return func(*args, **kwargs)
        else:
            print(f'{TAB}Некорректно задана ветка. Используйте команду list --branches для просмотра перечня веток.')
    return wrapper


def build_exists(build_id: BuildID):
    if build_id is not None:
        build_exists = (exec_sql(f'SELECT COUNT(*) FROM history WHERE branch = {build_id.branch} and build = {build_id.build};').fetchone()[0] == 1)
        if build_exists:
            return True
    return False


def build_validation(func):
    def wrapper(*args, **kwargs):    
        build_id: BuildID = args[0]
        if build_exists(build_id):
            return func(*args, **kwargs)
        else:
            print(f'{TAB}Сборка отсутствует. Используйте команду list -branch=номер_ветки для просмотра перечня сборок в ветке.')
    return wrapper   


def parent_validation(func):
    def wrapper(*args, **kwargs):    
        build_id = kwargs.get('parent', None)
        if build_id is not None:
            if build_exists(build_id):
                return func(*args, **kwargs)
            else:
                print(f'{TAB}Родительская сборка отсутствует. Используйте команду list -branch=номер_ветки для просмотра перечня сборок в ветке.')
        else:
            func(*args, **kwargs)
    return wrapper   
