
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def setup_teardown():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    yield driver
    driver.quit()


def test_registration_page(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5002/")

    assert driver.title == "Form Example"
    assert driver.find_element(By.TAG_NAME, "h2").text == "Application Form"


def test_registration_fields(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5002/")

    assert driver.find_element(By.NAME, "username").is_displayed()
    assert driver.find_element(By.NAME, "pwd").is_displayed()
    assert driver.find_element(By.NAME, "sb").is_displayed()


def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5002/")

    driver.find_element(By.NAME, "username").send_keys(" ")
    driver.find_element(By.NAME, "pwd").send_keys("password123")
    driver.find_element(By.NAME, "sb").click()

    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    assert alert.text == "Username cannot be empty."
    alert.accept()


def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5002/")

    driver.find_element(By.NAME, "username").send_keys("Nisha")
    driver.find_element(By.NAME, "pwd").send_keys("123")
    driver.find_element(By.NAME, "sb").click()

    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    assert alert.text == "Password must be at least 6 characters long."
    alert.accept()


def test_valid_registration(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5002/")

    driver.find_element(By.NAME, "username").send_keys("Nisha")
    driver.find_element(By.NAME, "pwd").send_keys("password123")
    driver.find_element(By.NAME, "sb").click()

    message = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.TAG_NAME, "h2"))
    ).text

    assert message == "Hello, Nisha! Welcome to the website"
