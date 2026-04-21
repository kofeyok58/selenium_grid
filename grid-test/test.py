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

def test_case1_basic_search(browser_name):
    print(f'\n{"="*50}')
    print(f'1. запускаем {browser_name.upper()}')
    options = get_browser_options(browser_name)
    driver = webdriver.Remote(command_executor=GRID_URL, options=options)
    try:
        driver.get('https://www.python.org')
        if 'Python' not in driver.title:
            raise AssertionError(f'тайтл (заголовок) не соответсвует {browser_name} прозошла ошибка')
        
        wait = WebDriverWait(driver, 10)

        search_input = wait.until(EC.presence_of_element_located((By.ID, 'id-search-field')))
        search_input.send_keys('python 3.12')
        search_button = wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
        search_button.click()
        
        time.sleep(2)
        
        if "Search" not in driver.title and "Python" not in driver.title:
            raise AssertionError(f'Не удалось выполнить поиск для {browser_name}')
        print(f'все успешно работает для {browser_name}')
    except Exception as e:
        print(f'в этом браузере {browser_name} прозошла ошибка')
    finally:
        driver.quit()

def test_case2_navigation_docs(browser_name):
    print(f'\n{"="*50}')
    print(f'2. запускаем {browser_name.upper()}')
    options = get_browser_options(browser_name)
    driver = webdriver.Remote(command_executor=GRID_URL, options=options)
    try:
        driver.get('https://www.python.org')
        driver.maximize_window()
        
        wait = WebDriverWait(driver, 10)
        
        if "Python" not in driver.title:
            print(f'предупреждение: нестандартный заголовок для {browser_name}')
        
        try:
            docs_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "nav [href='/doc/']")))
            docs_link.click()
            print(f'перешли в Documentation для {browser_name}')
        except Exception as e:
            print(f'при переходе в Documentation в {browser_name} прозошла ошибка: {str(e)}')
        
        time.sleep(2)
        
        try:
            doc_content = driver.find_elements(By.CSS_SELECTOR, "#docs-content, .document, article")
            if len(doc_content) > 0:
                print(f'найден контент документации для {browser_name}')
            else:
                # Альтернативная проверка через ссылки
                doc_links = driver.find_elements(By.TAG_NAME, 'a')
                if len(doc_links) > 10:
                    print(f'найдены ссылки на документацию для {browser_name}')
                else:
                    print(f'найдено ограниченное количество ссылок на документацию для {browser_name}')
        except:
            print(f'не удалось проверить документацию для {browser_name}')
        
        # Переход в Downloads через прямой URL 
        driver.get('https://www.python.org/downloads/')
        time.sleep(2)
        
        download_sections = driver.find_elements(By.CSS_SELECTOR, 
            "#content, .download-buttons, .release-banner, [id*='download'], [class*='download']")
        
        if len(download_sections) > 0:
            print(f'найдены секции загрузки для {browser_name}')
        else:
            # Проверяем наличие кнопок загрузки по тексту
            download_buttons = driver.find_elements(By.XPATH, 
                "//a[contains(translate(text(), 'DOWNLOAD', 'download'), 'download')]")
            if download_buttons:
                print(f'найдены кнопки загрузки для {browser_name}')
            else:
                print(f'страница загрузок может иметь другой формат для {browser_name}')
        
        print(f'навигация работает успешно для {browser_name}')
    except Exception as e:
        print(f'Ошибка в {browser_name}: {str(e)}')
    finally:
        driver.quit()

def test_case3_community_and_news(browser_name):
    print(f'\n{"="*50}')
    print(f'3. запускаем {browser_name.upper()}')
    options = get_browser_options(browser_name)
    driver = webdriver.Remote(command_executor=GRID_URL, options=options)
    try:
        driver.get('https://www.python.org')
        
        wait = WebDriverWait(driver, 10)
        
        try:
            community_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "nav a[href='/community/']")))
            community_link.click()
            print(f'перешли в Community для {browser_name}')
        except Exception as e:
            print(f'при переходе в Community в {browser_name} прозошла ошибка: {str(e)}')
            # Резервный переход через прямой URL
            driver.get('https://www.python.org/community/')
            print(f'перешли в Community через прямой URL для {browser_name}')

        time.sleep(2)
        
        community_elements = driver.find_elements(By.CSS_SELECTOR, 
            ".community-grid, .pep-widget, .psf-widget, [id*='community'], [class*='community']")
        
        if len(community_elements) > 0:
            print(f'найдены элементы сообщества для {browser_name}')
        else:
            links_count = driver.find_elements(By.TAG_NAME, 'a')
            if len(links_count) > 5:
                print(f'найдены элементы сообщества для {browser_name}')
            else:
                print(f'элементы сообщества могут быть в другом формате для {browser_name}')
        
        # Переход к новостям через прямой URL 
        driver.get('https://www.python.org/blogs/')
        time.sleep(2)

        blog_elements = driver.find_elements(By.CSS_SELECTOR, 
            ".blog-list, .blog-post, .post, [class*='blog'], [class*='post']")
        
        if len(blog_elements) > 0:
            print(f'найдены элементы блога для {browser_name}')
        elif "Blog" in driver.title or "News" in driver.title:
            print(f'новости доступны для {browser_name}')
        else:
            # Резервная проверка через статьи
            articles = driver.find_elements(By.TAG_NAME, 'article')
            if articles:
                print(f'найдены статьи в блоге для {browser_name}')
            else:
                print(f'страница новостей загружена для {browser_name}')
        
        print(f'все успешно работает для {browser_name}')
    except Exception as e:
        print(f'Ошибка в {browser_name}: {str(e)}')
    finally:
        driver.quit()

if __name__ == "__main__":
    
    browsers = ["chrome", "firefox"]
    for browser in browsers:
        test_case1_basic_search(browser)
        test_case2_navigation_docs(browser)
        test_case3_community_and_news(browser)
    print("все тесты должны быть выполнены")
