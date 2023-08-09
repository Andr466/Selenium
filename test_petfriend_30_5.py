from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pytest

@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('Selenium/chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    pytest.driver.maximize_window()
    yield

    pytest.driver.quit()

def test_show_my_pets(testing):
    # Установка явного ожидания
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('baragoz@mail.ru')

    # Установка явного ожидания
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('baragoz')

    # Установка неявного ожидания
    pytest.driver.implicitly_wait(10)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Установка неявного ожидания
    pytest.driver.implicitly_wait(10)
    # Переход в раздел мои питомцы
    pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')

    # Установка неявного ожидания
    pytest.driver.implicitly_wait(10)
    # Поиск нужных элементов страницы
    count = pytest.driver.find_elements(By.CSS_SELECTOR, '.\\.col-sm-4.left')
    pets = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')
    pets_img = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover img')
    description = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tr td')

    # Нахождение количества питомцев по информации со страницы сайта
    number = count[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])
    number_of_pets = len(pets)

    # Функция для подсчета количества питомцев с фото
    k = 0
    for i in range(len(pets_img)):
        if pets_img[i].get_attribute('src') != '':
            k += 1

    # Генератор списка данных о питомце
    data = [description[i].text for i in range(len(description))]

    # Список с именами питомцев
    name = data[::4]

    # Проверка на то, что нет пустых полей в данных о питомце
    for i in range(len(data)):
        assert data[i] != ''

    # Проверка того, что присутствуют все питомцы
    assert number == number_of_pets

    # Проверка, что хотя бы у половины питомцев есть фото
    assert k * 2 >= len(pets)

    # Проверка, что у всех питомцев разные имена и соответсвенно нет повторяющихся питомцев
    assert len(name) == len(list(set(name)))


