import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

@pytest.fixture
def driver():
   
    PACKAGE_NAME = "com.miui.notes" 
    ACTIVITY_NAME = "com.miui.notes.ui.NotesListActivity" 

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "Android Phone"
    options.app_package = PACKAGE_NAME
    options.app_activity = ACTIVITY_NAME
    options.no_reset = True

    options.skip_device_initialization = True  # Пропускает некоторые проверки
    options.ignore_hidden_api_policy_error = True  # Игнорирует ошибки hidden API
    options.auto_grant_permissions = True  # Автоматически выдаёт разрешения приложению

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    yield driver
    driver.quit()