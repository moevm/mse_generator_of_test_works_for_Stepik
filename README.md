# Генератор контрольных работ для stepik.org
Веб приложение предназначенное для составления контрольных работ на основе существующих курсов.

## Создание модуля для получения списка курсов авторизованного пользователя

Написана функция

    $ get_admin_courses(token)

В качестве единственного аргумента она принимает строку token, полученную после авторизации пользователя. Возвращает список курсов (словарей со всеми свойствами курса).

### Использование:

    $ from getting_courses import get_admin_courses
    $ courses = get_admin_courses(token)

### Нужные ключи словаря курса:
1. Id курса: *"id"*
2. Имя курса: *"title"*
## Скачивание курса
### Загрузка курса
Используется модуль **download**, а именно функция

    $  download_course(token, course_id)

Где:
 - ***token*** - токен пользователя
 - ***course_id*** - идентификатор нужного курса

Функция создает папку с курсом в виде файловой структуры и возвращает объект **Course**
### Объект Course
Хранит в себе список всех модулей курса, с включенными в них уроками и соответственно степами, позволяет получить список всех степов, основываясь на модулях/уроках/степах, выбранных пользователем:

    $ course = download_course(token, course_id)
    $ chose_steps = course.get_chosen()
### Структура файлов
В результате выполнения скрипта **get_steps.py** создается следующая структура файлов:

![Пример структуры данных](https://github.com/moevm/mse_generator_of_test_works_for_Stepik/raw/dev/API%20research/examples/file_structure_example.png?raw=true)

## Зависимости

- requests
- Flask
- xhtml2pdf
- markdown

## Запуск

В папке проекта выполнить:

```
    pip install -r requirements.txt
    python app.py
    
```

Сервис доступен на localhost:8080

Презентация первой итерации:  
https://docs.google.com/presentation/d/1GXo8m8JXA-OC7c6_FMFOYaBImJtRXP8ZilnPeo2YIcY/edit?usp=sharing
