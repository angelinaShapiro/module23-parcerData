import requests
from bs4 import BeautifulSoup
import json
import csv
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BookScraper:
    """
    Класс для парсинга веб-сайта http://books.toscrape.com/ и извлечения информации о книгах.
    """

    def __init__(self, base_url="http://books.toscrape.com"):
        """
        Инициализация класса.

        Args:
            base_url (str): Базовый URL веб-сайта.
        """
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_page(self, url):
        """
        Получает содержимое веб-страницы.

        Args:
            url (str): URL страницы.

        Returns:
            bs4.BeautifulSoup: Объект BeautifulSoup, представляющий HTML-код страницы.
            None: Если произошла ошибка при получении страницы.
        """
        try:
            logging.info(f"Получение страницы: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)  # Добавлен timeout
            response.raise_for_status()  # Проверка на ошибки HTTP
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при получении страницы {url}: {e}")
            return None

    def extract_book_data(self, book_element):
        """
        Извлекает данные о книге из HTML-элемента.

        Args:
            book_element (bs4.element.Tag): HTML-элемент, содержащий информацию о книге.

        Returns:
            dict: Словарь с данными о книге (название, цена, рейтинг, наличие).
            None: Если не удалось извлечь данные.
        """
        try:
            title = book_element.h3.a['title']
            price = book_element.find('p', class_='price_color').text[1:]  # Убираем символ '£'
            stock_element = book_element.find('p', class_='instock availability')
            stock = stock_element.text.strip() if stock_element else "Нет информации о наличии"
            rating_element = book_element.find('p', class_='star-rating')
            rating = rating_element['class'][1] if rating_element else 'No rating'

            book_data = {
                'title': title,
                'price': price,
                'rating': rating,
                'stock': stock
            }
            return book_data
        except Exception as e:
            logging.error(f"Ошибка при извлечении данных о книге: {e}")
            return None

    def get_all_books_from_page(self, page_url):
        """
        Извлекает данные о всех книгах на данной странице.

        Args:
            page_url (str): URL страницы.

        Returns:
            list: Список словарей с данными о книгах на странице.
        """
        soup = self.get_page(page_url)
        if soup:
            book_elements = soup.find_all('article', class_='product_pod')
            books_data = []
            for book_element in book_elements:
                book_data = self.extract_book_data(book_element)
                if book_data:
                    books_data.append(book_data)
            return books_data
        else:
            return []

    def scrape_all_books(self):
        """
        Собирает данные обо всех книгах со всех страниц веб-сайта.

        Returns:
            list: Список словарей с данными обо всех книгах.
        """
        all_books = []
        page_num = 1
        while True:
            url = f"{self.base_url}/catalogue/page-{page_num}.html"
            books_on_page = self.get_all_books_from_page(url)
            if books_on_page:
                all_books.extend(books_on_page)
                logging.info(f"Страница {page_num}: Найдено {len(books_on_page)} книг")
                page_num += 1
            else:
                logging.info("Нет больше страниц с книгами.")
                break  # Прекращаем цикл, если на странице нет книг
        return all_books

    def save_to_json(self, data, filename="books.json"):
        """
        Сохраняет данные о книгах в формате JSON.

        Args:
            data (list): Список словарей с данными о книгах.
            filename (str): Имя файла для сохранения.
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logging.info(f"Данные сохранены в файл {filename}")
        except Exception as e:
            logging.error(f"Ошибка при сохранении в JSON: {e}")

    def save_to_csv(self, data, filename="books.csv"):
        """
        Сохраняет данные о книгах в формате CSV.

        Args:
            data (list): Список словарей с данными о книгах.
            filename (str): Имя файла для сохранения.
        """
        if not data:
            logging.warning("Нет данных для сохранения в CSV файл.")
            return

        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Записываем заголовок
                writer.writerow(data[0].keys())
                # Записываем данные
                for book in data:
                    writer.writerow(book.values())
            logging.info(f"Данные сохранены в файл {filename}")
        except Exception as e:
            logging.error(f"Ошибка при сохранении в CSV: {e}")

# Пример использования
if __name__ == '__main__':
    scraper = BookScraper()
    all_books = scraper.scrape_all_books()

    if all_books:
        logging.info(f"Найдено {len(all_books)} книг.")
        scraper.save_to_json(all_books)
        scraper.save_to_csv(all_books)
    else:
        logging.info("Книги не найдены.")
