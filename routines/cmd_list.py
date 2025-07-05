from .history_types import PrintCell
from .validation import build_validation, branch_validation
from .get_data import get_branch_history, get_first_build, get_last_build, get_all_branches, get_children_branches, get_children_branches_total_count, get_branch_comment, get_build_nums, get_parents
from .consts import *
from .configs import *


def list_branches():
    branches = get_all_branches()
    comments = {branch: get_branch_comment(branch) for branch in branches}
    comment_len = [len(comment) for comment in comments.values()]
    max_info_len = max(comment_len)
    for branch in branches:
        parents = get_parents(branch)
        if len(parents) == 0:
            parents = 'отсутствуют'
        elif len(parents) == 1:
            parents = f'{parents[0]}'
        else:
            parents = f'{','.join(parents)}'
        print(f'{TAB}Ветка: {branch}{TAB}Комментарий: ' + f'{comments[branch]}'.ljust(max_info_len) + f'{TAB}Родители: {parents}')


@branch_validation
def list_builds_in_branch(branch: int):
    builds = get_branch_history(branch)
    print(f'{TAB}Сборки в ветке {branch} ({get_branch_comment(branch)}):')
    if len(builds) > 0:
        for build_info in builds:
            print(f'{TAB}{TAB}Сборка:', build_info.build, ' Версия прошивки:',
                  build_info.firmware_ver,' Комментарий:', build_info.comment,
                  ' Имя файла:', build_info.filename)
    else:
        print(f'{TAB}{TAB}Сборки отсутствуют')
    print(f'{TAB}{TAB}{'-'*150}')

def list_all():
    print()
    print(f'{TAB}Полная история проекта:')
    branches = get_all_branches()
    for branch in branches:
        list_builds_in_branch(branch)


def list_tree():
    # Список веток
    branches = get_all_branches()

    # Словари горизонтального и вертикального уровней веток
    branch_depth = {branch: 0 for branch in branches}
    branch_level = {branch: 0 for branch in branches}

    # Заполнение словаря вертикальных уровней и определение максимального вертикального уровня
    # Заполнение словаря горизонтальных уровней для веток
    for branch in branches:
        children = get_children_branches(branch)
        prev_depth = branch_depth[branch] + 1
        for child in children:
            branch_level[child] = branch_level[branch] + 1
            branch_depth[child] += prev_depth
            prev_depth += get_children_branches_total_count(child) + 1
    max_vert_level = max(branch_level.values())

    # Подготовка таблицы печати
    table_width = max(branch_depth.values())
    table = [[PrintCell() for _ in range(table_width+1)] for _ in range(max_vert_level+1)]

    # Расстановка узловых точек
    for branch in branches:
        builds = get_build_nums(branch)
        if len(builds) == 0:
            builds = 'Сборок нет'
        elif len(builds) == 1:
            builds = f'Сборка {builds[0]}'
        else:
            builds = f'Сборки: {get_first_build(branch)}..{get_last_build(branch)}'
        builds = f'({builds})'
        table[branch_level[branch]][branch_depth[branch]] = PrintCell(branch, BRANCH_NODE, f'Ветка №{branch}'.center(CELL_WIDTH),
                                                                      builds.center(CELL_WIDTH))

    # Расстановка линий и стрелок
    for lvl in range(max_vert_level+1):
        for col in range(table_width+1):
            if table[lvl][col].cell_type == BRANCH_NODE:
                sub_branches = get_children_branches(table[lvl][col].branch)
                if len(sub_branches) > 0:
                    start = branch_depth[sub_branches[0]]
                    end = branch_depth[sub_branches[len(sub_branches)-1]]
                    for depth in range(start, end+1):
                        if depth < end:
                            table[lvl][depth].text_line_1 = '_'*CELL_WIDTH
                        else:
                            table[lvl][depth].text_line_1 = ('_'*(CELL_WIDTH//2 - 1)).ljust(CELL_WIDTH)
                for sub_branch in sub_branches:
                    depth = branch_depth[sub_branch]
                    table[lvl][depth].text_line_2 = '\\'.center(CELL_WIDTH)

    # Печать таблицы
    print()
    print(f'{TAB}Структура ветвления хранилища:')
    print()
    for row in table:
        line_1 = ''
        line_2 = ''
        for column in row:
            line_1 += column.text_line_1
            line_2 += column.text_line_2
        print(TAB, line_1)
        print(TAB, line_2)
    print()
