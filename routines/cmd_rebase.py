from dataclasses import astuple

from .db import exec_sql, commit
from .history_types import BuildID
from .validation import parent_validation, branch_validation
from .consts import *
from .configs import *


@parent_validation
@branch_validation
def rebase_branch(branch: int, parent: BuildID):
    exec_sql(f'UPDATE parents SET parent_branch = ?, parent_build = ? WHERE branch = {branch}', astuple(parent))
    commit()
    print(f'{TAB}Для ветки №{branch} установлен новый родитель: Ветка №{parent.branch}, сборка {parent.build}')