import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.config import Config

def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default=Config.BASE_URL, # Lấy mặc định từ file config của bạn
        help="Base URL of the AUT",
    )

@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url")

@pytest.fixture()
def driver():
    options = Options()
    options.add_argument("--window-size=1440,900")
    # Bỏ qua lỗi chứng chỉ SSL cho https://localhost:5001
    options.add_argument('--ignore-certificate-errors')

    if os.getenv("HEADLESS", "0") == "1" or Config.HEADLESS:
        options.add_argument("--headless=new")

    # Sử dụng WebDriverManager để tự động quản lý driver
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)

    browser.implicitly_wait(Config.TIMEOUT) # Dùng timeout từ config
    yield browser
    browser.quit()

@pytest.fixture()
def wait(driver):
    from selenium.webdriver.support.ui import WebDriverWait
    return WebDriverWait(driver, 10)