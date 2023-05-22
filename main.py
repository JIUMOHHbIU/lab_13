import locale

from typing import List, Any, Callable

from check_path import is_path_exists_or_creatable
import os

field_width = 35
my_sep = '|'

# locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))


def get_number(convert_function: Callable, prompt='') -> Any:
    value = None
    while value is None:
        input_string = input(prompt)
        try:
            value = convert_function(input_string)
        except ValueError:
            print('Полученная строка не является валидным числом')

    return value


def get_separetor():
    return my_sep


def fields_repr_sep(fields: List[Any]) -> str | None:
    try:
        str = get_separetor().join(fields)
    except:
        return None
    return str


def line_parse_sep(line: str) -> List[any] | None:
    try:
        fields = line.strip().split(my_sep)
    except:
        return None
    return fields


def choose_file(path: str) -> str:
    while True:
        path = input('Введите путь: ')
        if is_path_exists_or_creatable(path) and len(path) > 4 and (path[-4:] == '.txt'):
            break
        print('Введенный путь является некорректным')

    return path


def init_db(path: str) -> str:
    if not (is_path_exists_or_creatable(path) and len(path) > 4 and (path[-4:] == '.txt')) or path == '':
        print('Некорректный путь')
        return path
    f = open(path, 'w')

    while 2 >= (columns_len := get_number(int, 'Введите количество полей: ')):
        print('Некорректное значение')

    headers = []
    columns_types = []
    for i in range(columns_len):
        while len((header := input(f'Введите {i+1}-й заголовок базы данных: '))) > field_width:
            print(f'Заголовок длиннее ширины поля({field_width})')
        while (column_type := input(f'Введите тип данных {i+1}-го столбца: ')) \
                and column_type != 'str' and column_type != 'int':
            print('Введён неподдержанный тип данных')
        headers += [header]
        columns_types += [column_type]

    if headers:
        f.write(str(columns_len) + '\n')
        f.write(fields_repr_sep(columns_types) + '\n')
        f.write(fields_repr_sep(headers) + '\n')

    print()
    while 0 > (lines_count := get_number(int, 'Введите количество записей для инициализации: ')):
        print('Некорректное значение')

    for i in range(lines_count):
        fields = []
        for j in range(columns_len):
            field = None
            while field is None:
                input_string = input(f'Введите {j + 1}-е поле {i + 1}-й строки: ')
                while columns_types[j] == 'str' and len(input_string) > field_width:
                    print(f'Поле длиннее ширины поля({field_width})')
                    input_string = input(f'Введите {j + 1}-е поле {i + 1}-й строки: ')

                if columns_types[j] == 'int':
                    try:
                        field = int(input_string)
                    except ValueError:
                        print('Полученная строка не является валидным числом')
                else:
                    field = input_string

            fields += [str(field)]
        f.write(fields_repr_sep(fields) + '\n')

    f.close()
    return path


def print_db(path: str) -> str:
    if not (is_path_exists_or_creatable(path) and len(path) > 4 and (path[-4:] == '.txt')) or path == '':
        print('Некорректный путь')
        return path

    try:
        with open(path, 'r') as f:
            inp_str_columns = f.readline()
            try:
                inp_str_columns = int(inp_str_columns)
            except ValueError:
                print('\nБитый файл базы данных\n')
                return path
            columns_len = inp_str_columns
            if columns_len < 2:
                print('\nБитый файл базы данных\n')
                return path

            inp_str_types = f.readline()
            columns_types = line_parse_sep(inp_str_types)
            if not columns_types or len(columns_types) != columns_len:
                print('\nБитый файл базы данных\n')
                return path

            is_headers = 1
            for line in f:
                parsed = line_parse_sep(line)
                if not parsed or len(parsed) != columns_len:
                    print('\nБитый файл базы данных\n')
                    return path

                if is_headers:
                    print(*[f'{item:{field_width}}' for item in parsed], sep=' | ')
                    is_headers = 0
                    continue
                for j in range(columns_len):
                    if columns_types[j] == 'int':
                        try:
                            value = int(parsed[j])
                        except ValueError:
                            print('\nБитый файл базы данных\n')
                            return path
                        print(f'{value:<{field_width}.5g}', sep='', end='')
                    elif columns_types[j] == 'str':
                        print(f'{parsed[j]:{field_width}}', sep='', end='')
                    if j != columns_len - 1:
                        print(f' {my_sep} ', sep='', end='')
                    elif j == columns_len - 1:
                        print()
    except PermissionError:
        print('Нет необходимого доступа')
    return path


def add_line(path: str) -> str:
    if not (os.path.exists(path) and len(path) > 4 and (path[-4:] == '.txt')) or path == '':
        print('Некорректный путь')
        return path
    try:
        with open(path, 'r') as f:
            inp_str_columns = f.readline()
            try:
                inp_str_columns = int(inp_str_columns)
            except ValueError:
                print('\nБитый файл базы данных\n')
                return path
            columns_len = inp_str_columns
            if columns_len < 2:
                print('\nБитый файл базы данных\n')
                return path

            inp_str_types = f.readline()
            columns_types = line_parse_sep(inp_str_types)
            if not columns_types:
                print('\nБитый файл базы данных\n')
                return path

        with open(path, 'a') as f:
            fields = []
            for j in range(columns_len):
                field = None
                while field is None:
                    input_string = input(f'Введите {j + 1}-е поле: ')
                    while columns_types[j] == 'str' and len(input_string) > field_width:
                        print(f'Поле длиннее ширины поля({field_width})')
                        input_string = input(f'Введите {j + 1}-е поле: ')

                    if columns_types[j] == 'int':
                        try:
                            field = int(input_string)
                        except ValueError:
                            print('Полученная строка не является валидным числом')
                    else:
                        field = input_string

                fields += [str(field)]
            f.write(fields_repr_sep(fields) + '\n')
    except PermissionError:
        print('Нет необходимого доступа')
    return path


def search_one_field(path: str) -> str:
    if not (os.path.exists(path) and len(path) > 4 and (path[-4:] == '.txt')) or path == '':
        print('Некорректный путь')
        return path

    try:
        with open(path, 'r') as f:
            inp_str_columns = f.readline()
            try:
                inp_str_columns = int(inp_str_columns)
            except ValueError:
                print('\nБитый файл базы данных\n')
                return path
            columns_len = inp_str_columns
            if columns_len < 2:
                print('\nБитый файл базы данных\n')
                return path

            inp_str_types = f.readline()
            columns_types = line_parse_sep(inp_str_types)
            if not columns_types or len(columns_types) != columns_len:
                print('\nБитый файл базы данных\n')
                return path

            while not(0 < (column_1 := get_number(int, 'Выберете столбец для поиска: ')) <= columns_len):
                print('Некорректный столбец')
            column_1 -= 1
            search_value_1 = None
            while search_value_1 is None:
                inp_str_value = input('Введите значение для поиска: ')
                if columns_types[column_1] == 'int':
                    try:
                        search_value_1 = int(inp_str_value)
                    except ValueError:
                        print('Значение не соответствует типу данных столбца')
                elif columns_types[column_1] == 'str':
                    search_value_1 = inp_str_value

            print('Найденные записи в базе данных:')
            is_headers = 1
            for line in f:
                parsed = line_parse_sep(line)
                if not parsed or len(parsed) != columns_len:
                    print('\nБитый файл базы данных\n')
                    return path

                if is_headers:
                    print(*[f'{item:{field_width}}' for item in parsed], sep=' | ')
                    is_headers = 0
                    continue

                found = 1
                if columns_types[column_1] == 'int':
                    try:
                        value = int(parsed[column_1])
                    except ValueError:
                        print('\nБитый файл базы данных\n')
                        return path
                elif columns_types[column_1] == 'str':
                    value = parsed[column_1]
                found *= search_value_1 == value

                if found:
                    for j in range(columns_len):
                        if columns_types[j] == 'int':
                            try:
                                value = int(parsed[j])
                            except ValueError:
                                print('\nБитый файл базы данных\n')
                                return path

                            print(f'{value:<{field_width}.5g}', sep='', end='')
                        elif columns_types[j] == 'str':
                            print(f'{parsed[j]:{field_width}}', sep='', end='')
                        if j != columns_len - 1:
                            print(f' {my_sep} ', sep='', end='')
                        elif j == columns_len - 1:
                            print()
    except PermissionError:
        print('Нет необходимого доступа')
    return path


def search_two_field(path: str) -> str:
    if not (os.path.exists(path) and len(path) > 4 and (path[-4:] == '.txt')) or path == '':
        print('Некорректный путь')
        return path

    try:
        with open(path, 'r') as f:
            inp_str_columns = f.readline()
            try:
                inp_str_columns = int(inp_str_columns)
            except ValueError:
                print('\nБитый файл базы данных\n')
                return path
            columns_len = inp_str_columns
            if columns_len < 2:
                print('\nБитый файл базы данных\n')
                return path

            inp_str_types = f.readline()
            columns_types = line_parse_sep(inp_str_types)
            if not columns_types or len(columns_types) != columns_len:
                print('\nБитый файл базы данных\n')
                return path

            while not(0 < (column_1 := get_number(int, 'Выберете столбец для поиска: ')) <= columns_len):
                print('Некорректный столбец')
            column_1 -= 1
            search_value_1 = None
            while search_value_1 is None:
                inp_str_value = input('Введите значение для поиска: ')
                if columns_types[column_1] == 'int':
                    try:
                        search_value_1 = int(inp_str_value)
                    except ValueError:
                        print('Значение не соответствует типу данных столбца')
                elif columns_types[column_1] == 'str':
                    search_value_1 = inp_str_value

            while not(0 < (column_2 := get_number(int, 'Выберете столбец для поиска: ')) <= columns_len):
                print('Некорректный столбец')
            column_2 -= 1
            search_value_2 = None
            while search_value_2 is None:
                inp_str_value = input('Введите значение для поиска: ')
                if columns_types[column_2] == 'int':
                    try:
                        search_value_2 = int(inp_str_value)
                    except ValueError:
                        print('Значение не соответствует типу данных столбца')
                elif columns_types[column_2] == 'str':
                    search_value_2 = inp_str_value

            print('Найденные записи в базе данных:')
            is_headers = 1
            for line in f:
                parsed = line_parse_sep(line)
                if not parsed or len(parsed) != columns_len:
                    print('\nБитый файл базы данных\n')
                    return path

                if is_headers:
                    print(*[f'{item:{field_width}}' for item in parsed], sep=' | ')
                    is_headers = 0
                    continue

                found = 1
                if columns_types[column_1] == 'int':
                    try:
                        value = int(parsed[column_1])
                    except ValueError:
                        print('\nБитый файл базы данных\n')
                        return path
                elif columns_types[column_1] == 'str':
                    value = parsed[column_1]
                found *= search_value_1 == value
                if columns_types[column_2] == 'int':
                    try:
                        value = int(parsed[column_2])
                    except ValueError:
                        print('\nБитый файл базы данных\n')
                        return path
                elif columns_types[column_2] == 'str':
                    value = parsed[column_2]
                found *= search_value_2 == value

                if found:
                    for j in range(columns_len):
                        if columns_types[j] == 'int':
                            try:
                                value = int(parsed[j])
                            except ValueError:
                                print('\nБитый файл базы данных\n')
                                return path

                            print(f'{value:<{field_width}.5g}', sep='', end='')
                        elif columns_types[j] == 'str':
                            print(f'{parsed[j]:{field_width}}', sep='', end='')
                        if j != columns_len - 1:
                            print(f' {my_sep} ', sep='', end='')
                        elif j == columns_len - 1:
                            print()
    except PermissionError:
        print('Нет необходимого доступа')
    return path


def loop(menu_str: str) -> None:
    actions = {
        1: choose_file,
        2: init_db,
        3: print_db,
        4: add_line,
        5: search_one_field,
        6: search_two_field,
    }

    path = ''
    while True:
        print(menu_str)
        prompt = 'Введите номер действия: '
        action = get_number(int, prompt=prompt)

        if action == 7:
            break

        if actions.get(action, -1) != -1:
            path = actions[action](path)
            print()
        else:
            print('Такого действия не существует')


def main():
    menu_str = '''Меню:
1. Выбрать файл для работы
2. Инициализировать базу данных (создать либо перезаписать файл и заполнить его записями)
3. Вывести содержимое базы данных
4. Добавить запись в конец базы данных
5. Поиск по одному полю
6. Поиск по двум полям
'''
    loop(menu_str)


if __name__ == '__main__':
    main()
