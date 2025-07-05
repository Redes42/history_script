from .consts import *

OFFSET = 70

def print_help():
    print("""Данная система предназначена для хранения только ключевых сборок проекта в виде zip-архивов, без частых коммитов.
Система предназначена для проектов, которые в один момент времени ведёт только один человек.
Поддерживается добавление новых и замена существующих сборок, ветвление (без слияния). Ветки нумеруются с единицы.
Каждая сборка сопровожадется однострочным и опциональным расширенным комментарием и нумеруется по порядку, с единицы.
Доступ к сборкам возможен через любой файловый менеджер: в подпапке ".History" проекта хранятся zip-архивы сборок
с именами файлов в формате: НомерВетки.НомерСборки - Имя_проекта [Версия] - Однострочный комментарий.zip, например:
02.01 - Проект1 [7E89C333] - Версия после испытаний (исправлены коэффициенты).zip

Ниже перечислены поддерживаемые команды и их параметры - обязательные и [опциональные]:""")
    print()
    print(f'{TAB}Создание хранилища:')
    print(f'{f'{TAB}{TAB}{CREATE}'.ljust(OFFSET)} - параметры не требуется, проект для хранилища выбирается при старте программы.')
    print()
    print(f'{TAB}Добавление данных:')     
    print(f'{f'{TAB}{TAB}{ADD} {BRANCH}={BRANCHNUM} {BUILD}={BUILDNUM} {NEWBRANCH}'.ljust(OFFSET)} - добавление новой ветки в хранилище (с указанием родительской сборки).')
    print(f'{f'{TAB}{TAB}{ADD} {BRANCH}={BRANCHNUM} {NEWBUILD}'.ljust(OFFSET)} - добавление новой сборки в хранилище (в указанную ветку). HEX-файл должен быть скомпилирован!')
    print(f'{f'{TAB}{TAB}{ADD} {BRANCH}={BRANCHNUM} {NEWBUILD} {FROMFILE}'.ljust(OFFSET)} - добавление новой сборки в хранилище (в указанную ветку) через импорт из zip-архива.')
    print()
    print(f'{TAB}Удаление данных:') 
    print(f'{f'{TAB}{TAB}{DELETE} {BRANCH}={BRANCHNUM}'.ljust(OFFSET)} - удаление ветки из хранилища. Ветка должна не иметь потомков. Используйте с осторожностью!')
    print(f'{f'{TAB}{TAB}{DELETE} {BRANCH}={BRANCHNUM} {BUILD}={BUILDNUM}'.ljust(OFFSET)} - удаление указанной сборки из заданной ветки.')
    print(f'{f'{TAB}{TAB}{DELETE} {BRANCH}={BRANCHNUM} {LAST}'.ljust(OFFSET)} - удаление последней сборки из заданной ветки.')
    print(f'{f'{TAB}{TAB}{DELETE} {ALL}'.ljust(OFFSET)} - полная очистка хранилища (с удалением файлов!). Используйте с осторожностью!')
    print()
    print(f'{TAB}Обновление данных:')        
    print(f'{f'{TAB}{TAB}{UPDATE} {BRANCH}={BRANCHNUM} {BUILD}={BUILDNUM} {COMMENT}'.ljust(OFFSET)} - обновить однострочный комментарий в указанной сборке указанной ветки.')
    print(f'{f'{TAB}{TAB}{UPDATE} {BRANCH}={BRANCHNUM} {BUILD}={BUILDNUM} {EXTCOMMENT}'.ljust(OFFSET)} - обновить расширенный комментарий в указанной сборке указанной ветки.')
    print(f'{f'{TAB}{TAB}{UPDATE} {BRANCH}={BRANCHNUM} {BUILD}={BUILDNUM}'.ljust(OFFSET)} - обновить указанную сборку в указанной ветке из рабочего каталога.')
    print(f'{f'{TAB}{TAB}{UPDATE} {BRANCH}={BRANCHNUM} {LAST}'.ljust(OFFSET)} - обновить последнюю сборку в указанной ветке из рабочего каталога.')
    print(f'{f'{TAB}{TAB}{UPDATE} {BRANCH}={BRANCHNUM} {BUILD}={BUILDNUM} {FROMFILE}'.ljust(OFFSET)} - обновить указанную сборку в указанной ветке из файла (откроется диалог для выбора zip-архива).')
    print(f'{f'{TAB}{TAB}{UPDATE} {BRANCH}={BRANCHNUM} {COMMENT}'.ljust(OFFSET)} - обновить однострочный комментарий в указанной ветке.')
    print()
    print(f'{TAB}Реструктуризация хранилища:')
    print(f'{f'{TAB}{TAB}{REBASE} {BRANCH}={BRANCHNUM} {PARENT_BRANCH}=РодительскаяВетка {PARENT_BUILD}=РодительскаяСборка'.ljust(OFFSET)} - переместить ветку, назначив нового родителя.')
    print()
    print(f'{TAB}Получение списка веток/сборок:')
    print(f'{f'{TAB}{TAB}{LIST} {BRANCHES}'.ljust(OFFSET)} - список существующих веток.')
    print(f'{f'{TAB}{TAB}{LIST} {ALL}'.ljust(OFFSET)} - полная история проекта.')
    print(f'{f'{TAB}{TAB}{LIST} {TREE}'.ljust(OFFSET)} - вывод графического отображения дерева проекта.')
    print(f'{f'{TAB}{TAB}{LIST} {BRANCH}={BRANCHNUM}'.ljust(OFFSET)} - список сборок в указанной ветке.')
    print()
    print(f'{TAB}Подробная информация о ветках/сборках:')
    print(f'{f'{TAB}{TAB}{INFO} {BRANCH}={BRANCHNUM}'.ljust(OFFSET)} - информация об указанной ветке')
    print(f'{f'{TAB}{TAB}{INFO} {BRANCH}={BRANCHNUM} {BUILD}={BUILDNUM}'.ljust(OFFSET)} - информация об указанной сборке в указанной ветке.')
    print(f'{f'{TAB}{TAB}{INFO} {BRANCH}={BRANCHNUM} {LAST}'.ljust(OFFSET)} - информация о последней сборке в указанной ветке.')
    print()
    print(f'{TAB}Развёртывание:')
    print(f'{f'{TAB}{TAB}{GET} {BRANCH}={BRANCHNUM} {BUILD}={BUILDNUM}'.ljust(OFFSET)} - развёртывание определённой сборки в рабочей папке (с сохранением резервной копии в хранилище).')
    print(f'{f'{TAB}{TAB}{GET} {BRANCH}={BRANCHNUM} {BUILD}={BUILDNUM} {NOBACKUP}'.ljust(OFFSET)} - развёртывание определённой сборки в рабочей папке (без сохранения резервной копии).')
    print(f'{f'{TAB}{TAB}{FLASH} {BRANCH}={BRANCHNUM} {BUILD}={BUILDNUM}'.ljust(OFFSET)} - прошивка контроллера прошивкой из указанной сборки.')
    print()
    print(f'{TAB}Экспортирование сборок/прошивок:')
    print(f'{f'{TAB}{TAB}{EXPORT} {BRANCH}={BRANCHNUM} {BUILD}={BUILDNUM}'.ljust(OFFSET)} - экспорт сборки в папку (откроется диалог выбора папки)')
    print(f'{f'{TAB}{TAB}{EXPORT} {BRANCH}={BRANCHNUM} {BUILD}={BUILDNUM} {HEX}'.ljust(OFFSET)} - экспорт прошивки (hex-файла) из сборки в папку (откроется диалог выбора папки)')
    print(f'{f'{TAB}{TAB}{EXPORT} {BRANCH}={BRANCHNUM} {BUILD}={BUILDNUM} {ZIP}'.ljust(OFFSET)} - экспорт сборки (архивом) в папку (откроется диалог выбора папки)')
    print()
    print(f'{TAB}Служебные команды:')
    print(f'{f'{TAB}{TAB}{HELP}'.ljust(OFFSET)} - печать данной справки.')
    print(f'{f'{TAB}{TAB}{QUIT}'.ljust(OFFSET)} - выход из программы.')
    print()
