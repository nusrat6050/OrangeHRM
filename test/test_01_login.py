import pytest  # Importing Pytest framework
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Pytest fixture to handle WebDriver setup and teardown
@pytest.fixture(scope="module")
def driver():
    # Setup Chrome WebDriver
    driver = webdriver.Chrome()  # Ensure the ChromeDriver matches your browser version
    yield driver  # Yield returns the driver to the test
    driver.quit()  # Close the browser after the test completes

# Test case: Login test
@pytest.mark.login
def test_login(driver):
    # 1. Navigate to the login page
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    driver.maximize_window()
    print("Navigated to OrangeHRM login page.")
    time.sleep(3)  # Wait for the page to load (only for demo purposes)

    # 2. Input username and password
    try:
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        username_field.send_keys("Admin")  # Correct username
        password_field.send_keys("admin123")  # Correct password
        print("Entered username and password.")
    except Exception as e:
        pytest.fail(f"Field not found: {str(e)}")  # Fail the test if fields are not found

    # 3. Click the login button
    try:
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        print("Clicked the login button.")
    except Exception as e:
        pytest.fail(f"Login button not found: {str(e)}")  # Fail the test if button is not found

    # 4. Verify if login was successful
    time.sleep(5)  # Wait for the page to load
    if "dashboard" in driver.current_url.lower():
        print("Login successful. Dashboard loaded.")
        assert True  # Test passes
    else:
        pytest.fail("Login failed. Dashboard not loaded.")  # Test fails if dashboard doesn't load