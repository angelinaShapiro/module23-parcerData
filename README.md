# Парсер веб-сайта http://books.toscrape.com/

## Постановка задачи

Данный проект представляет собой парсер веб-сайта http://books.toscrape.com/, который собирает информацию о книгах, такую как название, цена, рейтинг и доступность.  Результаты парсинга можно сохранить в форматах JSON и CSV для дальнейшего анализа или использования.

## Инструкция по сборке и запуску

1.  Установите Python 3.x.
2.  Установите необходимые библиотеки:

    ```bash
    pip install requests beautifulsoup4
    ```

3.  Создайте файл `books_parser.py` и скопируйте в него код парсера.
4.  Запустите парсер:

    ```bash
    python books_parser.py
    ```

    В результате работы парсера будут созданы файлы `books.json` и `books.csv`, содержащие данные о книгах.

## Пример результатов работы парсера

**books.json:**

```json
[
    {
        "title": "A Light in the Attic",
        "price": "51.77",
        "rating": "Three",
        "stock": "In stock"
    },
    {
        "title": "Tipping the Velvet",
        "price": "53.74",
        "rating": "One",
        "stock": "In stock"
    },
    ...
]
