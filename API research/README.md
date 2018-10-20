# API Research
Исследование на тему получения курса со степика для дальнейшей работы с ним
 - **get_steps.py** - выгрузка курса и представление его в виде файловой структуры
 - **examples** - директория с примерами того как выглядят отдельные элементы курса при его выгрузке 
## Выгрузка курса
Используется скрипт **get_steps.py** следующим образом:

    $ python3 get_steps.py <client_id> <client_secret> <course_id>
Где:

 - ***client_d***, ***client_secret*** - соответствующие ключи пользователя
 - ***course_id*** - идентификатор нужного курса
### Структура файлов
В результате выполнения скрипта **get_steps.py** создается следующая структура файлов:

![Пример структуры данных](https://raw.githubusercontent.com/moevm/mse_generator_of_test_works_for_Stepik/issue-12/API%20research/examples/file_structure_example.png)

