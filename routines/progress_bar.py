import sys

from .consts import *


def update_progress_bar(percent: int):
    percent_str = str(percent).rjust(3)
    sys.stdout.write('\r')
    sys.stdout.write(f'{TAB}[{'='*percent}{'-'*(100-percent)}] {percent_str}%')
    sys.stdout.flush()