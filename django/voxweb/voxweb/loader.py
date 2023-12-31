import environ

env = environ.Env()
environ.Env.read_env()

SET_SECRET_KEY = env('SECRET_KEY')
SET_DEBUG = env('DEBUG')
SET_ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

DB_ENGINE = env('DB_ENGINE')
DB_NAME = env('DB_NAME')
DB_USER = env('DB_USER')
DB_PASSWORD = env('DB_PASSWORD')
DB_HOST = env('DB_HOST')
DB_PORT = env('DB_PORT')
DB_SQL_MODE = env('DB_SQL_MODE')

BASE_URL = 'https://www.ozon.ru'

URL = f'{BASE_URL}/seller/1/products/'

PRODUCT_CARD_CLASS_DIV = 'ji8 i9j'
IMAGE_CLASS_IMG = 'c9-a'
HREF_CLASS_A = 'y9h tile-hover-target'
TITLE_CLASS_DIV = 'x3d xd4 dx5 y2h yh3'
TITLE_CLASS_DIV_SPAN = 'tsBody500Medium'
PRICE_CLASS_DIV = SALE_CLASS_DIV = 'y2h h3y c3-a'
NEW_PRICE_CLASS_DIV_SPAN = 'c3-a1 tsHeadline500Medium c3-b9'
OLD_PRICE_CLASS_DIV_SPAN = 'c3-a1 tsBodyControl400Small c3-b0'
SALE_PRICE_CLASS_DIV_SPAN = 'tsBodyControl400Small c3-a2 c3-a7 c3-b1'
COUNT_CLASS_DIV = 'e6-a e6-a5'
COUNT_CLASS_DIV_SPAN = 'e6-a4'
RATING_CLASS_DIV = 'd3u ud3 u3d tsBodyMBold'
RATING_CLASS_DIV_SPAN = 'ud4'
