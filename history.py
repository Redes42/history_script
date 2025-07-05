import sys; sys.dont_write_bytecode = True

import argparse
import os
import zipfile

from routines.history_types import BuildID
from routines.consts import *
from routines.configs import *
from routines.cmd_help import print_help
from routines.files import get_path, get_hexfile, get_zip_file
from routines.db import establish_connection, disconnect
from routines.cmd_add import add_branch, add_build, add_build_from_file
from routines.cmd_create import create
from routines.cmd_delete import delete_all, delete_branch, delete_build
from routines.cmd_info import branch_info, build_info
from routines.cmd_list import list_branches, list_builds_in_branch, list_all, list_tree
from routines.cmd_update import update_build_comment, update_extcomment, update_build_from_file, update_branch_comment, update_build
from routines.cmd_rebase import rebase_branch
from routines.cmd_get import get_build
from routines.cmd_flash import flash_build
from routines.cmd_export import export_build, export_build_hex, export_build_zip
from routines.get_data import get_last_build

# Докстринги

if __name__ == '__main__':
    finished = False
    parser = argparse.ArgumentParser(prog='History', add_help=False, exit_on_error=False)
    parser.add_argument('cmd', choices=[CREATE, ADD, DELETE, UPDATE, LIST, INFO, REBASE, FLASH, EXPORT, GET, HELP, QUIT])

    # Для команд add, delete, update, info, list
    parser.add_argument(BRANCH, type=int)
    parser.add_argument(BUILD, type=int)
    parser.add_argument(NEWBRANCH, action='store_true')
    parser.add_argument(NEWBUILD, action='store_true')

    # Для команд list
    parser.add_argument(BRANCHES, action='store_true')

    # Для команд list, delete, info
    parser.add_argument(LAST, action='store_true')
    parser.add_argument(ALL, action='store_true')
    parser.add_argument(TREE, action='store_true')

    # Для команды rebase
    parser.add_argument(PARENT_BRANCH, type=int)
    parser.add_argument(PARENT_BUILD, type=int)    

    # Для команд export
    parser.add_argument(HEX, action='store_true')
    parser.add_argument(ZIP, action='store_true')

    # Для команды update
    parser.add_argument(COMMENT, action='store_true')
    parser.add_argument(EXTCOMMENT, action='store_true')
    parser.add_argument(FROMFILE, action='store_true')

    # Для команды add -branch=x --newbuild
    parser.add_argument(BZIP2, action='store_true')
    parser.add_argument(LZMA, action='store_true')

    # Для команды get
    parser.add_argument(NOBACKUP, action='store_true')

    print('Вас приветствует система контроля сборок History.')
    print(f'Для получения справки введите команду {HELP}.')

    config['path'] = get_path()
    config['project_name'] = os.path.basename(config['path'])
    config['path'] += '\\'
    config['hexfile'] = get_hexfile()

    establish_connection(config['path'])

    while not finished:
        prompt = input('Введите команду: ').strip()
        try:
            args = parser.parse_args(prompt.split())
            build_id = BuildID(args.branch, args.build)
            if args.last:
                build_id.build = get_last_build(build_id.branch)
            parent = BuildID(args.parent_branch, args.parent_build)
            cmd = args.cmd
            
            if cmd == CREATE:
                create()

            if cmd == ADD:
                if args.newbranch and not args.newbuild:
                    if args.branch is not None and args.build is not None:
                        add_branch(parent=build_id)
                    else:
                        raise argparse.ArgumentError(None, '')
                elif args.newbuild and not args.newbranch:
                    if not args.fromfile:
                        if build_id.branch is not None:
                            if args.bzip2:
                                add_build(build_id.branch, zipfile.ZIP_BZIP2)
                            elif args.lzma:
                                add_build(build_id.branch, zipfile.ZIP_LZMA)
                            else:
                                add_build(build_id.branch)
                        else:
                            raise argparse.ArgumentError(None, '')
                    else:
                        add_build_from_file(build_id.branch, get_zip_file())
                else:
                    raise argparse.ArgumentError(None, '')

            if cmd == DELETE:
                if build_id.branch is not None and build_id.build is not None:
                    delete_build(build_id)
                elif build_id.branch is not None and build_id.build is None:
                    delete_branch(build_id.branch)      
                else:
                    if args.all:
                        delete_all()      

            if cmd == UPDATE:
                if build_id.build is None:
                    if build_id.branch is not None and args.comment:
                        update_branch_comment(build_id.branch)
                else:
                    if args.fromfile:
                        update_build_from_file(build_id, get_zip_file())
                    elif args.comment:
                        update_build_comment(build_id)
                    elif args.extcomment:
                        update_extcomment(build_id)
                    else:
                        if args.bzip2:
                            update_build(build_id, zipfile.ZIP_BZIP2)
                        elif args.lzma:
                            update_build(build_id, zipfile.ZIP_LZMA)
                        else:
                            update_build(build_id)
                    

            if cmd == LIST:
                if args.branches:
                    list_branches()
                elif build_id.branch is not None:
                    list_builds_in_branch(build_id.branch)
                elif args.all:
                    list_all()
                elif args.tree:
                    list_tree()
                else:
                    raise argparse.ArgumentError(None, '')

            if cmd == INFO:
                if build_id.branch is not None and build_id.build is not None:
                    build_info(build_id)
                elif args.branch is not None and args.build is None:
                    branch_info(build_id.branch)
                else:
                    raise argparse.ArgumentError(None, '')

            if cmd == REBASE:
                if parent.branch is not None and parent.build is not None:
                    rebase_branch(build_id.branch, parent)

            if cmd == GET:
                if build_id.branch is not None and build_id.build is not None:
                    get_build(build_id, nobackup=args.nobackup)

            if cmd == FLASH:
                if build_id.branch is not None and build_id.build is not None:
                    flash_build(build_id)

            if cmd == EXPORT:
                if build_id.branch is not None and build_id.build is not None:
                    if args.hex:
                        export_build_hex(build_id)
                    elif args.zip:
                        export_build_zip(build_id)
                    else:
                        export_build(build_id)
                elif build_id.branch is not None and build_id.build is None:
                    if args.last:
                        if args.hex:
                            export_build_hex(BuildID(build_id.branch, get_last_build(build_id.branch)))
                        elif args.zip:
                            export_build_zip(BuildID(build_id.branch, get_last_build(build_id.branch)))
                        else:
                            export_build(BuildID(build_id.branch, get_last_build(build_id.branch)))
                    else:
                        raise argparse.ArgumentError(None, '')                  
                else:
                    raise argparse.ArgumentError(None, '')


            if cmd == HELP:
                print_help()

            if cmd == QUIT:
                disconnect()
                finished = True
        except argparse.ArgumentError as arg_err:
            if 'invalid choice' in arg_err.message:
                print(f'{TAB}Неизвестная команда, повторите ввод')
            else:
                print(f'{TAB}Ошибка в аргументах, повторите ввод')
