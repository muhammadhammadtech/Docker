import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    hub_url = os.getenv("SELENIUM_HUB_URL", "http://localhost:4444/wd/hub")  # <-- fixed

    driver = webdriver.Remote(
        command_executor=hub_url,
        options=chrome_options
    )
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    # Auto-screenshot on failure                                               <-- fixed
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            os.makedirs("screenshots", exist_ok=True)
            path = f"screenshots/{item.nodeid.replace('/', '_').replace('::', '_')}.png"
            driver.save_screenshot(path)
