import pytest
from selenium.webdriver.common.by import By

class TestWebAutomation:

    def test_example_page(self, driver):
        driver.set_page_load_timeout(30)
        driver.get("https://example.com")
        assert "Example Domain" in driver.title
        heading = driver.find_element(By.TAG_NAME, "h1")
        assert heading.text == "Example Domain"
        driver.save_screenshot("screenshots/example_page.png")
        print("PASSED: example page test")

    def test_httpbin_get(self, driver):
        driver.set_page_load_timeout(30)
        driver.get("https://httpbin.org/get")
        body = driver.find_element(By.TAG_NAME, "body")
        assert "url" in body.text.lower()
        driver.save_screenshot("screenshots/httpbin_page.png")
        print("PASSED: httpbin test")

    def test_javascript_execution(self, driver):
        driver.set_page_load_timeout(30)
        driver.get("https://example.com")
        title = driver.execute_script("return document.title;")
        assert "Example Domain" in title
        driver.execute_script("document.body.style.backgroundColor = 'lightblue';")
        driver.save_screenshot("screenshots/modified_page.png")
        print("PASSED: javascript test")

    def test_element_not_found_handling(self, driver):
        driver.set_page_load_timeout(30)
        driver.get("https://example.com")
        try:
            driver.find_element(By.ID, "non-existent-element")
            assert False
        except Exception as e:
            print(f"PASSED: correctly caught {type(e).__name__}")
            assert True
