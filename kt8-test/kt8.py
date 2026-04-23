import os 
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image, ImageChops
import imagehash

os.makedirs("baselines", exist_ok=True)
os.makedirs("diffs", exist_ok=True)
@pytest.fixture
def browser():
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(options=opts)
    driver.set_window_size(1920,1080)
    yield driver
    driver.quit()
def test_python_ui(browser):
    browser.get("https://www.python.org")
    wait = WebDriverWait(browser, 15)

    browser.get('https://www.python.org/doc/')
    wait = WebDriverWait(browser, 15)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    
    base = "baselines/python-doc.png"
    curr = "diffs/python-doc_current.png"
    
    if not os.path.exists(base):
        browser.get_screenshot_as_file(base)
        print('Эталон создан')

    browser.get('https://www.python.org/community/')
    wait = WebDriverWait(browser, 15)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    curr = "diffs/python-community_current.png"
    diff = "diffs/python-com_diff.png"
    browser.get_screenshot_as_file(curr)
    
    img_1 = Image.open(base).convert("RGB")
    img_2 = Image.open(curr).convert("RGB")
    h1 = imagehash.phash(img_1)
    h2 = imagehash.phash(img_2)
    if (h1 - h2) > 5:
        diff_img = ImageChops.difference(img_1, img_2)
        diff_img.save(diff)
        assert False, f'страницы отличаются {diff}'