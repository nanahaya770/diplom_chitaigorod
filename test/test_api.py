import requests
import pytest


BEARER_TOKEN = (
    'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3'
    'NTM5Njc0ODQsImlhdCI6MTc1Mzc5OTQ4NCwiaXNzIjoiL2FwaS92MS9h'
    'dXRoL2Fub255bW91cyIsInN1YiI6ImZmNGQ0ZjI2ZGM4MjQwMDA2NTNj'
    'YmZiMWE0MWE1ZDRkNDUyMGZmZWZhMWI0MTk1YWE2MGNlYzE0OWIzMDEy'
    'MzAiLCJ0eXBlIjoxMH0.Lv63O0Ij8j7bQNucoNN2WzeiP382R7p_FmyYcl8WPtg'
)
HEADERS = {
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
      'AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
      'Authorization': BEARER_TOKEN
    }

BOOK_ID_IN_CART = 214865377

BASE_URL = "https://web-agr.chitai-gorod.ru/web"

BOOK1_ID_IN_CATALOG = 2968841

BOOK2_ID_IN_CATALOG = 2713476

BOOK_NAME = "танах"


@pytest.fixture
def clear_cart():
    URL = f'{BASE_URL}/api/v1/cart'
    requests.request("DELETE", URL, headers=HEADERS)
    yield
    requests.request("DELETE", URL, headers=HEADERS)


@pytest.fixture
def delete_book_from_cart():
    # действия до вызова тестовой функции
    URL = f'{BASE_URL}/api/v1/cart/product/{BOOK_ID_IN_CART}'

    yield

    # действия после вызова тестовой функции
    requests.request("DELETE", URL, headers=HEADERS)


@pytest.fixture
def add_book_to_cart():
    URL = f'{BASE_URL}/api/v1/cart/product'
    body = {
        "id": BOOK1_ID_IN_CATALOG, "adData":
        {"product_shelf": "", "item_list_name": "search"}
    }
    requests.post(URL, headers=HEADERS, json=body)

    yield


def test_add_book(delete_book_from_cart):
    URL = f'{BASE_URL}/api/v1/cart/product'
    body = {
        "id": BOOK1_ID_IN_CATALOG, "adData":
        {"product_shelf": "", "item_list_name": "search"}
    }
    response = requests.post(URL, headers=HEADERS, json=body)
    assert response.status_code == 200


def test_get_cart() -> None:
    URL = f'{BASE_URL}/api/v1/cart'
    # получение карзины
    response = requests.request("GET", URL, headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["products"] == []


def test_get_by_keyword() -> None:
    URL = (
      f'{BASE_URL}'
      '/api/v2/search/product?customerCityId=213&products'
      f'[page]=1&products[per-page]=60&phrase={BOOK_NAME}&abTestGroup=1'
    )
    body = {
        "id": 2968841, "adData":
        {"product_shelf": "", "item_list_name": "search"}
    }
    response = requests.get(URL, headers=HEADERS, json=body)
    assert response.status_code == 200


def test_delete_book_from_cart(add_book_to_cart) -> None:
    URL = f'{BASE_URL}/api/v1/cart/product/{BOOK_ID_IN_CART}'
    response = requests.request("DELETE", URL, headers=HEADERS)
    assert response.status_code == 204


def test_total_cost(clear_cart):
    # добавление двух книг
    URL = f'{BASE_URL}/api/v1/cart/product'
    body = {
        "id": BOOK1_ID_IN_CATALOG, "adData":
        {"product_shelf": "", "item_list_name": "search"}
    }

    requests.post(URL, headers=HEADERS, json=body)
    body = {
        "id": BOOK2_ID_IN_CATALOG, "adData":
        {"product_shelf": "", "item_list_name": "search"}
    }
    requests.post(URL, headers=HEADERS, json=body)

    # получение карзины
    URL = f'{BASE_URL}/api/v1/cart'
    response = requests.request("GET", URL, headers=HEADERS)

    total_cost = response.json()["costWithSale"]
    cost1 = response.json()["products"][0]["cost"]
    cost2 = response.json()["products"][1]["cost"]

    assert cost1 + cost2 == total_cost
