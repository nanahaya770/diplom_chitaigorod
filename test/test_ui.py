from typing import Generator
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import allure
from conftest import UNKNOWN_BOOK


@pytest.fixture(scope='module')
def driver() -> Generator[WebDriver, None]:
    """
    Фикстура открывает браузер
    """
    service = ChromeService(ChromeDriverManager().install())
    driver: WebDriver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()


@allure.story("Проверка поиска книги по названию")
def test_search_box(driver: Generator[WebDriver, None]) -> None:
    """
    Функция проверяет работу поисковой строки,
    вводит название несуществующей книги и проверяет что
    поиск не принес результата

    """
    driver.get("https://www.chitai-gorod.ru")

    search_box = driver.find_element(By.NAME, "search")
    search_box.clear()
    search_box.send_keys(UNKNOWN_BOOK)
    driver.find_element(
        By.XPATH,
        '//*[@id="__nuxt"]/div/header/div/div[1]/div/div/div[1]/form/button'
    ).click()

    element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'search-title'))
    )
    assert element.text == (
        f'Поиск по запросу «{UNKNOWN_BOOK}» не принёс результатов'
    )


@allure.story("Проверка отображения количества товаров у иконки корзины")
def test_add_book_to_cart(driver: WebDriver) -> None:
    """
    Функция проверяет появление цыфры 1 у значка пустой корзины,
    после нажатия на кнопку 'Купить'
    """
    driver.get(
        "https://www.chitai-gorod.ru/product/bukvar-uchebnoe-posobie-94503"
        )
    driver.find_element(
        By.XPATH, '//*[@id="__nuxt"]/div/div[3]/div[1]/div/main/aside/div[2]'
        '/header/div/div[2]/button[1]').click()

    count = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((
            By.XPATH,
            '//*[@id="__nuxt"]/div/header/div/div[2]/button[3]/span[1]/div'
        ))
    )

    assert count.text == "1"


@allure.story("Проверка корректности подсчета количества товаров в корзине")
def test_book_in_cart(driver: WebDriver) -> None:
    """
    Функция проверяет правильность подчета
    итогового количества товаров в корзине
    """
    driver.get("https://www.chitai-gorod.ru/cart")
    count = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            '#__nuxt > div > div.app-wrapper__content > div:nth-child(1) > '
            'div > div > div.cart-page__cart-content > '
            'div.cart-page__cart-content--right > div > div:nth-child(2) > '
            'section.cart-sidebar__info > '
            'div:nth-child(1) > div.info-item__title'
        ))
    )

    assert count.text == "1 товар"


@allure.story("Проверка кнопки 'очистить корзину'")
def test_empty_cart(driver: WebDriver) -> None:
    """
    Функция проверяет кнопку очистки корзины
    """

    driver.find_element(By.CLASS_NAME, 'cart-page__delete-many').click()

    empty_cart = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((
            By.CLASS_NAME, 'cart-multiple-delete__title'
        ))
    )

    assert empty_cart.text == "Корзина очищена"


@allure.story("Проверка кнопки 'востановить корзину'")
def test_recover_cart(driver: WebDriver) -> None:
    """
    Функция проверяет кнопку востановления корзины
    """

    button_recover = (
        '#__nuxt > div > div.app-wrapper__content > div > '
        'div > div > section > div > button.chg-app-button'
        '.chg-app-button--primary.chg-app-button--s.'
        'chg-app-button--brand-blue.cart-multiple-delete__button.'
        'cart-multiple-delete__button'
        )

    driver.find_element(By.CSS_SELECTOR, button_recover).click()

    waiter = WebDriverWait(driver, 10)
    count_selector = (
        '#__nuxt > div > div.app-wrapper__content > div:nth-child(1) > '
        'div > div > div.cart-page__cart-content > '
        'div.cart-page__cart-content--right > div > div:nth-child(2) > '
        'section.cart-sidebar__info > '
        'div:nth-child(1) > div.info-item__title'
    )
    waiter.until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, count_selector),  "1 товар")
    )
    count = driver.find_element(By.CSS_SELECTOR, count_selector)

    assert count.text == "1 товар"
