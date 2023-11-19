import pytest
from utils import main
from pathlib import Path

abspath_operations = Path.joinpath(Path(__file__).parent.parent, "data", "operations.json")


def test_get_all_operations():
    assert main.get_all_operations(abspath_operations)
    with pytest.raises(SystemExit):
        assert main.get_all_operations("")
    assert isinstance(main.get_all_operations(abspath_operations), list)


def test_find_last_operations():
    assert main.find_last_operations([]) == []
    list_operations = [
        {'from': 'A', 'state': 'EXECUTED', 'date': '2021-01-01'},
        {'from': 'B', 'state': 'FAILED', 'date': '2021-01-02'},
        {'from': 'C', 'state': 'EXECUTED', 'date': '2021-01-03'},
        {'from': 'D', 'state': 'EXECUTED', 'date': '2021-01-04'},
        {'from': 'E', 'state': 'EXECUTED', 'date': '2021-01-05'},
        {'from': 'F', 'state': 'EXECUTED', 'date': '2021-01-06'}]
    assert main.find_last_operations(list_operations) == [
        {'from': 'F', 'state': 'EXECUTED', 'date': '2021-01-06'},
        {'from': 'E', 'state': 'EXECUTED', 'date': '2021-01-05'},
        {'from': 'D', 'state': 'EXECUTED', 'date': '2021-01-04'},
        {'from': 'C', 'state': 'EXECUTED', 'date': '2021-01-03'},
        {'from': 'A', 'state': 'EXECUTED', 'date': '2021-01-01'}]


def test_masking_numbers():
    sorted_operations = [{"from": "Счет 1234567890123456", "to": "Visa 1234567890123456"},
                         {"from": "Visa 1234567890123456", "to": "Счет 1234567890123456"}]

    assert isinstance(main.masking_numbers(sorted_operations), list)
    hidden_operations = main.masking_numbers(sorted_operations)
    assert hidden_operations[0]["num_from"] == "**3456"
    assert hidden_operations[1]["num_from"] == "1234 67** **** 3456"
    assert hidden_operations[0]["num_to"] == "1234 67** **** 3456"
    assert hidden_operations[1]["num_to"] == "**3456"


def test_print_last_operations(capsys):
    operations_list = [{'id': 114832369, 'state': 'EXECUTED', 'date': '2019-12-07T06:17:14.634890',
                        'operationAmount': {'amount': '48150.39', 'currency': {'name': 'USD', 'code': 'USD'}},
                        'description': 'Перевод организации', 'from': 'Visa Classic 2842878893689012',
                        'to': 'Счет 35158586384610753655', 'type_from': 'Visa Classic ',
                        'num_from': '2842 78** **** 9012',
                        'type_to': 'Счет ', 'num_to': '**3655'},
                       {'id': 154927927, 'state': 'EXECUTED', 'date': '2019-11-19T09:22:25.899614',
                        'operationAmount': {'amount': '30153.72', 'currency': {'name': 'руб.', 'code': 'RUB'}},
                        'description': 'Перевод организации', 'from': 'Maestro 7810846596785568',
                        'to': 'Счет 43241152692663622869',
                        'type_from': 'Maestro ', 'num_from': '7810 46** **** 5568', 'type_to': 'Счет ',
                        'num_to': '**2869'},
                       {'id': 482520625, 'state': 'EXECUTED', 'date': '2019-11-13T17:38:04.800051',
                        'operationAmount': {'amount': '62814.53', 'currency': {'name': 'руб.', 'code': 'RUB'}},
                        'description': 'Перевод со счета на счет', 'from': 'Счет 38611439522855669794',
                        'to': 'Счет 46765464282437878125',
                        'type_from': 'Счет ', 'num_from': '**9794', 'type_to': 'Счет ', 'num_to': '**8125'},
                       {'id': 509645757, 'state': 'EXECUTED', 'date': '2019-10-30T01:49:52.939296',
                        'operationAmount': {'amount': '23036.03', 'currency': {'name': 'руб.', 'code': 'RUB'}},
                        'description': 'Перевод с карты на счет', 'from': 'Visa Gold 7756673469642839',
                        'to': 'Счет 48943806953649539453',
                        'type_from': 'Visa Gold ', 'num_from': '7756 73** **** 2839', 'type_to': 'Счет ',
                        'num_to': '**9453'},
                       {'id': 888407131, 'state': 'EXECUTED', 'date': '2019-09-29T14:25:28.588059',
                        'operationAmount': {'amount': '45849.53', 'currency': {'name': 'USD', 'code': 'USD'}},
                        'description': 'Перевод со счета на счет', 'from': 'Счет 35421428450077339637',
                        'to': 'Счет 46723050671868944961',
                        'type_from': 'Счет ', 'num_from': '**9637', 'type_to': 'Счет ', 'num_to': '**4961'}]
    output = """07.12.2019 Перевод организации
Visa Classic 2842 78** **** 9012 -> Счет **3655
48150.39 USD

19.11.2019 Перевод организации
Maestro 7810 46** **** 5568 -> Счет **2869
30153.72 руб.

13.11.2019 Перевод со счета на счет
Счет **9794 -> Счет **8125
62814.53 руб.

30.10.2019 Перевод с карты на счет
Visa Gold 7756 73** **** 2839 -> Счет **9453
23036.03 руб.

29.09.2019 Перевод со счета на счет
Счет **9637 -> Счет **4961
45849.53 USD

"""

    main.print_last_operations(operations_list)
    assert capsys.readouterr().out == output
