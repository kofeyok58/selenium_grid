import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestNotes:
    
    def test_create_note_with_ids(self, driver):
        # Ждём загрузки главного экрана
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ID, "com.miui.notes:id/recycler_view"))
        )
        
        # 1. Нажимаем кнопку создания заметки
        add_btn = driver.find_element(AppiumBy.ID, "com.miui.notes:id/note_add")
        add_btn.click()
        time.sleep(2)
        
        # 2. Вводим заголовок 
        title_field = driver.find_element(AppiumBy.ID, "com.miui.notes:id/note_title")
        title_field.click()  
        title_field.send_keys("Моя тестовая заметка c помощью Appium")
        
        # 3. Вводим текст заметки
        content_field = driver.find_element(AppiumBy.ID, "com.miui.notes:id/rich_editor")
        content_field.click() 
        content_field.send_keys("лалалалалалала")
        
        # 4. Сохраняем заметку 
        time.sleep(1)
        back_btn = driver.find_element(AppiumBy.ID, "com.miui.notes:id/home")
        back_btn.click()
        
        # 5. Ждём возврата в список и проверяем, что заметка появилась
        time.sleep(3)
        note_title = driver.find_element(AppiumBy.XPATH, 
            "//android.widget.TextView[contains(@text, 'Моя тестовая заметка')]")

        assert note_title.is_displayed(), "Заметка не найдена в списке!"
        print("\n Тест пройден! Заметка успешно создана и отображается в списке.")