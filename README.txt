Курсовой проект по курсу «Основы backend-разработки»
Реализована функция, которая выводит на экран список из 5 последних выполненных клиентом операций в формате:

<дата перевода> <описание перевода>
<откуда> -> <куда>
<сумма перевода> <валюта>

Описание функций
get_all_operations(file_path) - получает путь к файлу списка операций и возвращет список в json формате

find_last_operations(list_operations) - сортирвует по убыванию даты. Возвращает список 5 последних состоявшихся операций

masking_numbers(sorted_operations) - скрывает номера карт и счетов

print_last_operations(operations_with_hidden_num) - функция принта операций в заданном формате