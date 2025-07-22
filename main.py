import json
import csv
from kinopoisk_api.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_api.request.films.film_search_request import FilmSearchRequest

def parse_kinopoisk_film(film_name: str) -> dict | None:
    """
    Парсит подробную информацию о фильме с Кинопоиска по его названию.

    Args:
        film_name (str): Название фильма для поиска.

    Returns:
        dict | None: Словарь с информацией о фильме, или None, если фильм не найден
                     или произошла ошибка при получении данных.
    """
    try:
        client = KinopoiskApiClient()
        # Создаем запрос на поиск фильма
        request = FilmSearchRequest(film_name)
        films = client.films(request)

        if not films:
            print(f"Фильм '{film_name}' не найден на Кинопоиске.")
            return None

        # Берем первый найденный фильм (предполагаем, что это наиболее релевантный результат)
        film = films[0]

        # Получаем более подробную информацию о фильме по его ID
        film_details = client.films.get_film_details(film.kp_id)

        if not film_details:
            print(f"Не удалось получить подробную информацию о фильме '{film_name}' (ID: {film.kp_id}).")
            return None

        # Извлекаем нужную информацию из объекта film_details
        movie_data = {
            "kp_id": film_details.kp_id,
            "title_ru": film_details.name_ru,
            "title_en": film_details.name_en,
            "year": film_details.year,
            "rating_kp": film_details.rating_kp,
            "rating_imdb": film_details.rating_imdb,
            "genres": [genre.name for genre in film_details.genres],
            "countries": [country.name for country in film_details.countries],
            "description": film_details.description,
            "poster_url": film_details.poster_url,
            "link": f"https://www.kinopoisk.ru/film/{film_details.kp_id}/"
        }

        return movie_data

    except Exception as e:
        print(f"Произошла ошибка при парсинге фильма '{film_name}': {e}")
        return None

def save_results(data, output_format="json", filename="kinopoisk_films"):
    """
    Сохраняет результаты парсинга в указанный формат файла.

    Args:
        data (list): Список словарей с данными для сохранения.
        output_format (str): Формат сохранения ('json', 'csv').
        filename (str): Базовое имя файла для сохранения (без расширения).
    """
    if not data:
        print("Нет данных для сохранения.")
        return

    try:
        if output_format.lower() == "json":
            full_filename = f"{filename}.json"
            with open(full_filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Данные успешно сохранены в файл: {full_filename}")

        elif output_format.lower() == "csv":
            full_filename = f"{filename}.csv"
            # Получаем заголовки из ключей первого словаря (предполагаем, что все словари имеют одинаковую структуру)
            fieldnames = data[0].keys()
            with open(full_filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            print(f"Данные успешно сохранены в файл: {full_filename}")
        else:
            print(f"Неподдерживаемый формат вывода: {output_format}. Поддерживаются 'json' и 'csv'.")
    except Exception as e:
        print(f"Ошибка при сохранении данных в файл {output_format}: {e}")

if __name__ == "__main__":
    print("--- Парсер информации о фильмах с Кинопоиска ---")

    while True:
        film_name_input = input("Введите название фильма (или 'выход' для завершения): ").strip()
        if film_name_input.lower() == 'выход':
            break

        if not film_name_input:
            print("Название фильма не может быть пустым. Попробуйте снова.")
            continue

        # Парсим информацию о фильме
        film_info = parse_kinopoisk_film(film_name_input)

        if film_info:
            # Сохраняем результат (в виде списка, даже если один фильм)
            save_results([film_info], output_format="json")
            # Для сохранения в CSV, раскомментируйте следующую строку:
            # save_results([film_info], output_format="csv")
        else:
            print("Не удалось получить информацию о фильме.")
        print("-" * 30)

    print("Работа парсера завершена.")