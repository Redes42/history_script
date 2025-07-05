from .db import exec_sql, commit
from .history_types import BuildID, BranchInfo, BuildInfo
from .validation import build_validation, branch_validation
from .consts import *
from .configs import *
from .cmd_add import add_branch

def create():
    table_count = exec_sql('SELECT COUNT(*) FROM SQLITE_MASTER WHERE tbl_name = "history";').fetchone()[0]
    if table_count == 0:
        exec_sql('''CREATE TABLE IF NOT EXISTS branches(branch INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        comment TEXT NOT NULL);''')
        exec_sql('''CREATE TABLE IF NOT EXISTS history(branch INTEGER,
                                                            build INTEGER,
                                                            comment TEXT NOT NULL, 
                                                            ext_comment TEXT NOT NULL, 
                                                            hash TEXT, 
                                                            firmware_ver TEXT, 
                                                            filename TEXT,
                                                            PRIMARY KEY(branch, build), 
                                                            FOREIGN KEY(branch) REFERENCES branches(branch) ON DELETE CASCADE);''')
        exec_sql('''CREATE TABLE IF NOT EXISTS parents(branch INTEGER,                                                                    
                                                            parent_branch INTEGER,
                                                            parent_build INTEGER,
                                                            PRIMARY KEY(branch, parent_branch, parent_build),
                                                            FOREIGN KEY(branch) REFERENCES branches(branch) ON DELETE CASCADE,
                                                            FOREIGN KEY(parent_branch, parent_build) REFERENCES history(branch, build) ON DELETE CASCADE);''')
        print(f'{TAB}Хранилище создано')
    else:
        print(f'{TAB}Хранилище уже существует')
    branches_count = exec_sql('SELECT COUNT(*) FROM branches').fetchone()[0]
    if branches_count == 0:
        print(f'{TAB}Создание ветки по умолчанию (исходной)...')
        add_branch(None)