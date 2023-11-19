from datetime import datetime
import sys
import json
from pathlib import Path


def get_all_operations(file_path):
    """
    Получаем все данные из файла operations.json
    :return: список с операциями
    """
    try:
        with open(file_path, 'r', encoding='UTF-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("File not found")
        sys.exit()


def find_last_operations(list_operations):
    """
    получаем индексы 5 последних транзакций
    :param list_operations: список операций
    :return: список 5 последних операций
    """

    executed_list_operations = [i for i in list_operations if 'from' in i and i['state'] == 'EXECUTED']
    sorted_list_operations = sorted(executed_list_operations, key=lambda x: x['date'], reverse=True)
    return sorted_list_operations[:5]


def masking_numbers(sorted_operations):
    """
    скрываем номера карт и счетов
    :param sorted_operations: список 5 последних операций
    :return: список операций с скрытыми номерами карт и счетов
    """
    for operation in sorted_operations:
        type_from = "".join([i for i in operation['from'] if i.isalpha() or i == " "])
        operation['type_from'] = type_from
        num_from = "".join([i for i in operation['from'] if i.isdigit()])
        if type_from == "Счет ":
            operation['num_from'] = '**'+num_from[-4:]
        else:
            operation['num_from'] = num_from[:4]+" "+num_from[5:7]+'** **** '+num_from[-4:]

        type_to = "".join([i for i in operation['to'] if i.isalpha() or i == " "])
        operation['type_to'] = type_to
        num_to = "".join([i for i in operation['to'] if i.isdigit()])
        if type_to == "Счет ":
            operation['num_to'] = '**' + num_to[-4:]
        else:
            operation['num_to'] = num_to[:4] + " " + num_to[5:7] + '** **** ' + num_to[-4:]
    return sorted_operations


def print_last_operations(operations_with_hidden_num):
    """создаем принт 5 последних операций"""
    for operation in operations_with_hidden_num:
        date = datetime.strptime(operation['date'], '%Y-%m-%dT%H:%M:%S.%f')
        print(f"{datetime.strftime(date, '%d.%m.%Y')} {operation['description']}\n"
              f"{operation['type_from']}{operation['num_from']} -> "
              f"{operation['type_to']}{operation['num_to']}\n"
              f"{operation['operationAmount']['amount']} {operation['operationAmount']['currency']['name']}\n")


def main():

    abspath_operations = Path.joinpath(Path(__file__).parent.parent, "data", "operations.json")
    operations_list = get_all_operations(abspath_operations)
    list_of_five_operations = find_last_operations(operations_list)
    hidden_operations = masking_numbers(list_of_five_operations)
    print_last_operations(hidden_operations)


if __name__ == '__main__':
    main()
