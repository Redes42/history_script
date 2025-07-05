from .db import exec_sql
from .history_types import BuildInfo, BuildID, BranchInfo
from .validation import build_validation, branch_validation


def get_first_branch() -> int:
    return exec_sql('SELECT branch FROM branches WHERE branch NOT IN (SELECT branch FROM parents);').fetchone()[0]


def get_last_branch() -> int:
    return exec_sql('SELECT MAX(branch) FROM branches').fetchone()[0]


def get_all_branches() -> list[int]:
    branches = exec_sql('SELECT branch FROM branches').fetchall()
    branches = [branch[0] for branch in branches]
    return branches


def get_branch_count() -> int:
    branch_count = exec_sql('SELECT COUNT(*) FROM branches').fetchone()[0]
    return branch_count


@branch_validation
def get_branch_comment(branch: int) -> str:
    return exec_sql(f'SELECT comment FROM branches WHERE branch = {branch}').fetchone()[0]


@branch_validation
def get_branch_info(branch: int) -> BranchInfo:
    return BranchInfo(*exec_sql(f'SELECT * FROM branches WHERE branch = {branch}').fetchone())


@branch_validation
def get_first_build(branch: int) -> int:
    result = exec_sql(f'SELECT MIN(build) FROM history WHERE branch = {branch}').fetchone()[0]
    return result


@branch_validation
def get_last_build(branch: int) -> int:
    result = exec_sql(f'SELECT MAX(build) FROM history WHERE branch = {branch}').fetchone()[0]
    result = 1 if result is None else result
    return result


@branch_validation
def get_new_build(branch: int) -> int:
    result = exec_sql(f'SELECT MAX(build) FROM history WHERE branch = {branch}').fetchone()[0]
    result = 1 if result is None else result + 1
    return result


@branch_validation
def get_build_nums(branch: int) -> list[int]:
    result = [item.build for item in get_branch_history(branch)]
    return result


@branch_validation
@build_validation
def get_build_info(build_id: BuildID) -> BuildInfo:
    build_info = exec_sql(f'''SELECT *
                               FROM history
                               WHERE branch = {build_id.branch} AND build = {build_id.build};''').fetchone()
    build_info = BuildInfo(*build_info)
    return build_info


@branch_validation
def get_children_branches(branch: int) -> list[int]:
    branches = exec_sql(f'SELECT branch FROM parents WHERE parent_branch = {branch};').fetchall()
    children = [branch[0] for branch in branches]
    return children


@branch_validation
def get_children_branches_total_count(branch: int) -> int:
    counter = 0
    branch_children = exec_sql(f'SELECT branch FROM parents WHERE parent_branch = {branch}').fetchall()
    if branch_children is None:
        return 0
    else:
        counter += len(branch_children)
        for child in branch_children:
            counter += get_children_branches_total_count(child[0])
        return counter


@branch_validation
def get_parents(branch: int) -> list[BuildID]:
    result = exec_sql(f'SELECT parent_branch, parent_build FROM parents WHERE branch = {branch}').fetchall()
    result = [BuildID(*item) for item in result]
    return result


@branch_validation
def get_branch_history(branch: int) -> list[BuildInfo]:
    branch_history = exec_sql(f'SELECT * FROM history WHERE branch = {branch}').fetchall()
    branch_history = [BuildInfo(*item) for item in branch_history]
    return branch_history




