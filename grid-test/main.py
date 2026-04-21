from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

GRID_URL = "http://localhost:4444"
def get_browser_options(browser_name):
    if browser_name == "chrome":
        options = ChromeOptions()
        return options
    elif browser_name == "firefox":
        options = FireFoxOptions()
        return options
    else:
        raise ValueError(f'такого браузера {browser_name} не на вашей ОС')

def test_case1 (browser_name):
    print(f'\n{"="*50}')
    print(f'1. запускаем {browser_name.upper()}')
    options = get_browser_options(browser_name)
    driver = webdriver.Remote(command_executor=GRID_URL, options=options)
    try:
        driver.get('https://www.python.org')
        if 'Python' not in driver.title:
            raise AssertionError(f'тайтл (заголовок) не соответсвует {browser_name} прозошла ошибка')
        
        wait = WebDriverWait(driver, 10)
        search_input = wait.until(EC.presence_of_element_located((By.NAME, 'q')))
        search_input.send_keys('python 3.12')
        search_input.submit()
        
        time.sleep(2)
        
        if "Search" not in driver.title and "Python" not in driver.title:
            raise AssertionError(f'Не удалось выполнить поиск для {browser_name}')
        print(f'все успешно работает для {browser_name}')
    except Exception as e:
        print(f'в этом браузере {browser_name} прозошла ошибка')
    finally:
        driver.quit()

def test_case2_navigation_and_links(browser_name):
    print(f'\n{"="*50}')
    print(f'2. запускаем {browser_name.upper()}')
    options = get_browser_options(browser_name)
    driver = webdriver.Remote(command_executor=GRID_URL, options=options)
    try:
        driver.get('https://www.wikipedia.org')
        driver.maximize_window()
        
        wait = WebDriverWait(driver, 10)
        
        assert "Wikipedia" in driver.title, "Неверный заголовок страницы"
        
        # Находим поле поиска и вводим запрос
        search_input = wait.until(EC.presence_of_element_located((By.NAME, 'search')))
        search_input.send_keys('Selenium WebDriver')
        search_input.submit()
        
        time.sleep(3)
        
        assert "Selenium" in driver.title, "Не удалось найти статью"
        
        # Находим все ссылки в содержании статьи
        try:
            content_links = driver.find_elements(By.CSS_SELECTOR, '#toc a')
            if content_links:
                print(f'✓ Найдено {len(content_links)} ссылок в содержании')
                # Проверяем первую ссылку
                first_link_text = content_links[0].text
                print(f'  Первая ссылка: {first_link_text}')
        except:
            print('  Содержание не найдено')
        
        # Возвращаемся на главную
        driver.back()
        time.sleep(1)
        assert "Wikipedia" in driver.title, "Не удалось вернуться на главную"
        print(f'все успешно работает для {browser_name}')
    except Exception as e:
        print(f'Ошибка в {browser_name}: {str(e)}')
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    
    browsers = ["chrome", "firefox"]
    for browser in browsers:
        test_case1(browser)
        test_case2_navigation_and_links(browser)
    print("все тесты должны быть выполнены")
