from dotenv import load_dotenv
import os


# test_api.py
load_dotenv()

bearer_token = os.getenv('BEARER_TOKEN')

HEADERS = {
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
      'AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
      'Authorization': bearer_token
    }

BOOK1_ID_IN_CATALOG = 2968841
BOOK2_ID_IN_CATALOG = 2713476
BOOK_NAME = "танах"

BASE_URL = "https://web-agr.chitai-gorod.ru/web"

BODY_AD_DATA = {"product_shelf": "", "item_list_name": "search"}


# test_ui.py
UNKNOWN_BOOK = "рмюлмгюша"
