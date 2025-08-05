import requests
import pytest
from conftest import (
    HEADERS,
    BOOK_ID_IN_CART,
    BASE_URL,
    BOOK1_ID_IN_CATALOG,
    BOOK2_ID_IN_CATALOG,
    BOOK_NAME,
    BODY_AD_DATA
)


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
        "id": BOOK1_ID_IN_CATALOG,
        "adData": BODY_AD_DATA
    }
    requests.post(URL, headers=HEADERS, json=body)

    yield


def test_add_book(delete_book_from_cart):
    URL = f'{BASE_URL}/api/v1/cart/product'
    body = {
        "id": BOOK1_ID_IN_CATALOG,
        "adData": BODY_AD_DATA
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
        "id": BOOK1_ID_IN_CATALOG,
        "adData": BODY_AD_DATA
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
        "id": BOOK1_ID_IN_CATALOG,
        "adData": BODY_AD_DATA
    }
    requests.post(URL, headers=HEADERS, json=body)

    body = {
        "id": BOOK2_ID_IN_CATALOG,
        "adData": BODY_AD_DATA
    }
    requests.post(URL, headers=HEADERS, json=body)

    # получение корзины
    URL = f'{BASE_URL}/api/v1/cart'
    response = requests.request("GET", URL, headers=HEADERS)

    total_cost = response.json()["costWithSale"]
    cost1 = response.json()["products"][0]["cost"]
    cost2 = response.json()["products"][1]["cost"]

    assert cost1 + cost2 == total_cost
