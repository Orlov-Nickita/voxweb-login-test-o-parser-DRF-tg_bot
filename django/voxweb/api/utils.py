import time
import math
import uuid
from typing import Optional
import requests
import undetected_chromedriver as uc
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.response import Response
from selenium.webdriver import ActionChains
from voxweb.loader import PRODUCT_CARD_CLASS_DIV, IMAGE_CLASS_IMG, HREF_CLASS_A, TITLE_CLASS_DIV, \
    TITLE_CLASS_DIV_SPAN, PRICE_CLASS_DIV, NEW_PRICE_CLASS_DIV_SPAN, OLD_PRICE_CLASS_DIV_SPAN, SALE_CLASS_DIV, \
    SALE_PRICE_CLASS_DIV_SPAN, COUNT_CLASS_DIV, COUNT_CLASS_DIV_SPAN, RATING_CLASS_DIV, RATING_CLASS_DIV_SPAN, \
    BASE_URL
from re import compile as _c
from re import sub as _s
import json
import os.path
from bs4 import BeautifulSoup, ResultSet
from voxweb.settings import MEDIA_ROOT


def get_source_html(url: str, html_file_path: str) -> Optional[Response]:
    """
    Скачивает HTML с указанного адреса
    param url: URL адрес
    param html_file_path: Путь до файла, где произойдет сохранение
    """
    options = uc.ChromeOptions()
    options.add_argument('--incognito')  # --incognito: Запускает браузер в режиме инкогнито, чтобы не сохранять историю и данные сеанса.
    options.add_argument("--no-sandbox")  # --no-sandbox: Отключает использование песочницы, что может быть полезно при запуске контейнера в среде Docker.
    options.add_argument("--disable-gpu")  # --disable-gpu: Отключает использование графического процессора, что может быть полезно при запуске контейнера в среде Docker.
    options.add_argument('--ignore-certificate-errors')  # --ignore-certificate-errors: Игнорирует ошибки сертификатов SSL.
    options.add_argument('--allow-running-insecure-content')  # --allow-running-insecure-content: Разрешает запуск небезопасного контента.
    options.add_argument('--disable-setuid-sandbox')  # --disable-setuid-sandbox: Отключает использование setuid-песочницы.
    options.add_argument('--headless=new')  # --headless=new: Запускает браузер в режиме без графического интерфейса.
    options.add_argument("--disable-extensions")  # --disable-extensions: Отключает установленные расширения браузера.
    options.add_argument('--disable-application-cache')  # --disable-application-cache: Отключает кэширование приложений.
    options.add_argument("--disable-dev-shm-usage")  # --disable-dev-shm-usage: Отключает использование /dev/shm для временного хранения данных браузера.
    driver = uc.Chrome(options=options, use_subprocess=True)

    try:
        driver.get(url)
        driver.maximize_window()
        driver.execute_script("document.body.style.zoom = '70%'")

        actions = ActionChains(driver)
        actions.scroll_by_amount(delta_x=0, delta_y=6000).perform()

        time.sleep(3)

        with open(html_file_path, "w", encoding='utf-8') as file:
            file.write(driver.page_source)

    except Exception as Ex:
        er = json.dumps({'error': Ex})
        return Response(er, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    finally:
        driver.close()
        driver.quit()


def soup_disassemble(soup_with_classes: ResultSet) -> list:
    """
    Разбирает скачанный HTML на необходимые теги
    param soup_with_classes: Результат парсинга всей страницы
    """
    DATA = []

    for item in soup_with_classes:
        image = item.find('img', class_=_c(f'{IMAGE_CLASS_IMG}.*')).get('srcset')

        href = item.find('a', class_=_c(f'{HREF_CLASS_A}.*')).get('href')

        title = item.find('div', class_=_c(f'{TITLE_CLASS_DIV}.*')) \
            .find('span', class_=_c(f'{TITLE_CLASS_DIV_SPAN}.*')).text.strip()

        new_price = item.find('div', class_=_c(f'{PRICE_CLASS_DIV}.*')) \
            .find('span', class_=_c(f'{NEW_PRICE_CLASS_DIV_SPAN}.*')).text.strip()

        old_price = item.find('div', class_=_c(f'{PRICE_CLASS_DIV}.*')) \
            .find('span', class_=_c(f'{OLD_PRICE_CLASS_DIV_SPAN}.*')).text.strip()

        sale = item.find('div', class_=_c(f'{SALE_CLASS_DIV}.*')) \
            .find('span', class_=_c(f'{SALE_PRICE_CLASS_DIV_SPAN}.*')).text.strip()

        try:
            count_in_stock = item.find('div', class_=_c(f'{COUNT_CLASS_DIV}.*')) \
                .find('span', class_=_c(f'{COUNT_CLASS_DIV_SPAN}.*')).text.strip()

        except AttributeError:
            count_in_stock = 'Много'

        rating = item.find('div', class_=_c(f'{RATING_CLASS_DIV}.*')) \
            .find('span', class_=_c(f'{RATING_CLASS_DIV_SPAN}.*')).text.strip()

        product = {
            'href': f'{BASE_URL}{href}',
            'image': image.split()[0],
            'title': title,
            'new_price': int(_s("[^0-9]", "", new_price)),
            'old_price': int(_s("[^0-9]", "", old_price)),
            'sale': int(_s("[^0-9]", "", sale)),
            'count_in_stock': count_in_stock,
            'rating': float(rating),
        }

        DATA.append(product)

    return DATA


def write_into_json(into_path: str, file_to_remove: str, data_to_dump: list) -> None:
    """
    Записывает данные в json файл
    param into_path: Путь до файла
    param file_to_remove: Файл, который будет удален после записи
    param data_to_dump: Информация для записи
    """
    with open(into_path, 'w', encoding='utf-8') as json_f:
        json.dump(data_to_dump, json_f, ensure_ascii=False, indent=4)
        os.remove(file_to_remove)


def get_items_from_page(url: str, html_file: str, json_file_name: str, product_count: int = 0,
                        page_scrape: int = 1) -> None:
    """
    Парсинг страницы после скачивания страницы с HTML кодом
    param url: Страница, откуда будет выполняться скачивание
    param html_file: Наименование файла
    param json_file_name: Наименование файла json
    param product_count: Количество товаров, которое нужно добавить в БД
    param page_scrape: Страница непосредственного парсинга (товаров может быть много и в данном случае будет
    пагинация, этот параметр учитывает номер страницы)
    """
    n = "{html_file}-{page}".format(html_file=html_file, page=page_scrape)
    html_file_path = os.path.join(MEDIA_ROOT, f'{n}.html')

    get_source_html(url=url, html_file_path=html_file_path)

    with open(html_file_path, 'r', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, "html.parser")
    items_divs = soup.find_all("div", class_=_c(f"{PRODUCT_CARD_CLASS_DIV}.*"))
    data_from_page = soup_disassemble(soup_with_classes=items_divs)

    json_path = os.path.join(MEDIA_ROOT, f'{json_file_name}.json')
    if os.path.exists(json_path):
        if page_scrape == 1:
            os.truncate(path=json_path, length=0)
            write_into_json(into_path=json_path, file_to_remove=html_file_path, data_to_dump=data_from_page)

        else:
            with open(json_path, 'r', encoding='utf-8') as json_f:
                old_data = json.load(json_f)
                extended_data = old_data + data_from_page

            write_into_json(into_path=json_path, file_to_remove=html_file_path, data_to_dump=extended_data)

    else:
        write_into_json(into_path=json_path, file_to_remove=html_file_path, data_to_dump=data_from_page)

    if product_count > len(items_divs):
        pages = math.ceil(product_count / len(items_divs))
        for i_page in range(2, pages + 1):
            next_url = url + f'?page={i_page}'
            get_items_from_page(url=next_url, html_file=html_file, page_scrape=i_page, json_file_name=json_file_name)


def download_image(url: str) -> ContentFile:
    """
    Скачивает изображение по полученному адресу
    param url: Ссылка на изображение
    """
    response = requests.get(url)
    filename = f"{uuid.uuid4()}.jpg"
    return ContentFile(response.content, name=filename)


def send_message_in_bot(products_count: int) -> None:
    """
    Отправляет сообщение в тг-бот, после завершения парсинга
    param products_count: Количество добавленных товаров
    """
    base_url = 'https://api.telegram.org/bot{token}/sendMessage?chat_id={idx}&text={message}'
    token = os.getenv('BOT_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    message = 'Задача на парсинг товаров с сайта Ozon завершена\n' \
              'Сохранено: {count} товаров\n'.format(count=products_count)
    print('')
    try:
        requests.get(url=base_url.format(token=token,
                                         idx=chat_id,
                                         message=message))
    except Exception as Ex:
        print(Ex)
