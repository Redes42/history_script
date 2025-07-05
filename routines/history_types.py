from dataclasses import dataclass

from .consts import *

@dataclass
class BranchInfo:
    branch: int
    comment: str


@dataclass
class BuildInfo:
    branch: int = 1
    build: int = 1
    comment: str = ''
    ext_comment:str = ''
    hash: str = ''
    firmware_ver: str = ''
    filename: str = ''


@dataclass
class BuildID:
    branch: int | None = None
    build: int | None = None  
    
    def __str__(self):
        if self.build is None:
            return f'Ветка №{self.branch} (пусто)'.ljust(22)
        return f'Ветка №{self.branch}. Сборка №{self.build}'.ljust(22)

    
@dataclass
class PrintCell:
    branch: int | None = None
    cell_type: int = WHITESPACE
    text_line_1: str = ' '*CELL_WIDTH
    text_line_2: str = ' '*CELL_WIDTH