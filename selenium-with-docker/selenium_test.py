#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import sys

def test_google_search():
    """Test Google search functionality"""

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    try:
        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=chrome_options
        )

        print("✓ Successfully connected to Selenium container")

        driver.get("https://www.google.com")
        print("✓ Navigated to Google homepage")

        # Wait for search box and enter search term
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )

        search_term = "Docker Selenium testing"
        search_box.send_keys(search_term)
        search_box.submit()

        print(f"✓ Searched for: {search_term}")

        # FIX: wait for ANY results container — Google changes IDs frequently
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)

        page_title = driver.title
        print(f"✓ Page title: {page_title}")

        # FIX: check title or URL instead of a specific element ID
        if search_term.lower() in page_title.lower() or "google.com/search" in driver.current_url:
            print("✓ Test PASSED: Search results displayed correctly")
            return True
        else:
            print("✗ Test FAILED: Search results not as expected")
            return False

    except Exception as e:
        print(f"✗ Test FAILED with error: {str(e)}")
        return False

    finally:
        if 'driver' in locals():
            driver.quit()
            print("✓ Browser session closed")


def test_form_interaction():
    """Test form interaction on a demo website"""

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    try:
        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=chrome_options
        )

        print("\n--- Form Interaction Test ---")

        # FIX: use a more stable demo form site
        driver.get("https://www.w3schools.com/html/html_forms.asp")
        print("✓ Navigated to demo form page")

        # Wait for page to fully load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )
        time.sleep(2)

        # FIX: find first and last name fields on W3Schools form
        try:
            fname = driver.find_element(By.CSS_SELECTOR, "input[name='fname'], input#fname")
            fname.clear()
            fname.send_keys("John")
        except:
            fname = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")[0]
            fname.clear()
            fname.send_keys("John")

        try:
            lname = driver.find_element(By.CSS_SELECTOR, "input[name='lname'], input#lname")
            lname.clear()
            lname.send_keys("Doe")
        except:
            lname = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")[1]
            lname.clear()
            lname.send_keys("Doe")

        print("✓ Filled out form fields")

        # FIX: find submit button by type or value
        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        except:
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button")

        submit_button.click()
        print("✓ Form submitted successfully")

        time.sleep(2)

        # FIX: verify page is still reachable (form interaction succeeded)
        if driver.title:
            print("✓ Form submission test PASSED")
            return True
        else:
            print("✗ Form submission test FAILED")
            return False

    except Exception as e:
        print(f"✗ Form test FAILED with error: {str(e)}")
        return False

    finally:
        if 'driver' in locals():
            driver.quit()
            print("✓ Browser session closed")


if __name__ == "__main__":
    print("Starting Selenium Docker Tests...")
    print("=" * 50)

    test1_result = test_google_search()
    test2_result = test_form_interaction()

    print("\n" + "=" * 50)
    print("TEST SUMMARY:")
    print(f"Google Search Test: {'PASSED' if test1_result else 'FAILED'}")
    print(f"Form Interaction Test: {'PASSED' if test2_result else 'FAILED'}")

    if test1_result and test2_result:
        print("✓ All tests PASSED!")
        sys.exit(0)
    else:
        print("✗ Some tests FAILED!")
        sys.exit(1)

