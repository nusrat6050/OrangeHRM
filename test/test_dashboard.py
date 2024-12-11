import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Pytest fixture to handle WebDriver setup and teardown
@pytest.fixture
def driver():
    # Setup WebDriver using Service
    service = Service('../driver/chromedriver-win64/chromedriver.exe')  # Adjust path as needed
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)  # Implicit wait for better stability
    yield driver  # Yielding the driver to the test
    driver.quit()  # Teardown: Close the browser after test completion


def test_login(driver):
    print("Starting the OrangeHRM login test.")

    # Step 1: Navigate to the OrangeHRM demo page
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    driver.maximize_window()
    print("Opened OrangeHRM login page.")

    # Step 2: Verify the page title
    assert "OrangeHRM" in driver.title, "Incorrect page title!"
    print("Page title verified.")

    try:
        # Step 3: Locate username and password fields
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_field = driver.find_element(By.NAME, "password")
        print("Located username and password fields.")
    except TimeoutException:
        raise AssertionError("Test failed: Username and password fields not found.")

    # Step 4: Enter login credentials
    username_field.send_keys("Admin")
    password_field.send_keys("admin123")
    print("Entered login credentials.")

    # Step 5: Click the login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    print("Clicked login button.")

    try:
        # Step 6: Wait for the dashboard to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Dashboard']"))
        )
        print("Login successful. Dashboard loaded.")
    except TimeoutException:
        raise AssertionError("Test failed: Unable to load dashboard after login.")

    # Step 7: Navigate to "Admin" module
    admin_module = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Admin']"))
    )
    admin_module.click()
    print("Navigated to Admin module.")

    # Step 8: Verify navigation to the Admin module
    assert "admin/viewSystemUsers" in driver.current_url, "Failed to navigate to Admin module!"
    print("Admin module verified.")

    # Step 9: Navigate to "PIM" module
    pim_module = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='PIM']"))
    )
    pim_module.click()
    print("Navigated to PIM module.")

    # Step 10: Verify navigation to the PIM module
    assert "pim/viewEmployeeList" in driver.current_url, "Failed to navigate to PIM module!"
    print("PIM module verified.")

    # Step 11: Navigate to "Leave" module
    leave_module = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Leave']"))
    )
    leave_module.click()
    print("Navigated to Leave module.")

    # Step 12: Verify navigation to the Leave module
    assert "leave/viewLeaveList" in driver.current_url, "Failed to navigate to Leave module!"
    print("Leave module verified.")
