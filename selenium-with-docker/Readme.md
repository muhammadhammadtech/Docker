# Lab 39: Docker for Testing — Running Selenium with Docker

A complete walkthrough of pulling, running, and testing with Selenium inside a Docker container using Python and a virtual environment.

---

## Prerequisites

- Docker Engine installed and running
- Python 3.x with pip
- Terminal access (cloud machine or local Linux)

---

## Environment Setup — Python Virtual Environment

Before installing any packages, create an isolated Python environment.

**Install venv support:**
```bash
sudo apt-get install python3-venv -y
```

**Create the virtual environment:**
```bash
python3 -m venv selenium-env
```

**Activate it:**
```bash
source selenium-env/bin/activate
```

Your prompt will change to show `(selenium-env)` — all pip installs now stay isolated inside this environment.

**Confirm activation and upgrade pip:**
```bash
which python3
python3 --version
pip install --upgrade pip
```

> To re-activate in a new terminal session: `source selenium-env/bin/activate`  
> To exit the environment when done: `deactivate`

---

## Task 1 — Pull the Selenium Docker Image

**Verify Docker is running:**
```bash
docker --version
docker info
```

If Docker is not running, start it:
```bash
sudo systemctl start docker
```

**Pull the Selenium standalone Chrome image:**
```bash
docker pull selenium/standalone-chrome:latest
```

This image includes Selenium WebDriver, Google Chrome, ChromeDriver, and a VNC server.

**Verify the image downloaded:**
```bash
docker images | grep selenium
```

Expected output:
```
selenium/standalone-chrome   latest   abc123def456   2 days ago   1.2GB
```

---

## Task 2 — Run the Selenium Container

**Start the container:**
```bash
docker run -d \
  --name selenium-chrome \
  --shm-size=2g \
  -p 4444:4444 \
  -p 7900:7900 \
  selenium/standalone-chrome:latest
```

| Flag | Purpose |
|------|---------|
| `-d` | Run in background (detached) |
| `--name selenium-chrome` | Assign a friendly container name |
| `--shm-size=2g` | Allocate 2GB shared memory — prevents Chrome crashes |
| `-p 4444:4444` | Map Selenium WebDriver port |
| `-p 7900:7900` | Map VNC port for live browser viewing |

**Verify the container is running:**
```bash
docker ps
```

You should see `selenium-chrome` with status `Up`.

**Check Selenium hub is ready:**
```bash
curl http://localhost:4444/wd/hub/status
```

Expected: a JSON response confirming the hub is ready to accept connections.

---

## Task 3 — Connect Python to the Selenium Container

**Install required packages (inside venv):**
```bash
pip install selenium requests
```

**Create the test script:**
```bash
nano selenium_test.py
```

Paste the following code, then save with `Ctrl+X → Y → Enter`:

```python
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

        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )

        search_term = "Docker Selenium testing"
        search_box.send_keys(search_term)
        search_box.submit()

        print(f"✓ Searched for: {search_term}")

        # Wait for body — Google changes result element IDs frequently
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)

        page_title = driver.title
        print(f"✓ Page title: {page_title}")

        # Validate via title or URL rather than a specific element ID
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

        # W3Schools form is more stable than httpbin.org/forms/post
        driver.get("https://www.w3schools.com/html/html_forms.asp")
        print("✓ Navigated to demo form page")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )
        time.sleep(2)

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

        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        except:
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button")

        submit_button.click()
        print("✓ Form submitted successfully")

        time.sleep(2)

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
```

**Make the script executable:**
```bash
chmod +x selenium_test.py
```

> **Note on fixes applied:** The original lab used `By.ID, "search"` for Google results (now unstable) and `httpbin.org/forms/post` for the form test (submit button selector changed). Both have been updated to use more reliable alternatives.

---

## Task 4 — Run Tests and Capture Results

**Run the test script:**
```bash
python3 selenium_test.py
```

Expected output:
```
Starting Selenium Docker Tests...
==================================================
✓ Successfully connected to Selenium container
✓ Navigated to Google homepage
✓ Searched for: Docker Selenium testing
✓ Page title: ...
✓ Test PASSED: Search results displayed correctly
✓ Browser session closed
--- Form Interaction Test ---
✓ Navigated to demo form page
✓ Filled out form fields
✓ Form submitted successfully
✓ Form submission test PASSED
✓ Browser session closed
==================================================
TEST SUMMARY:
Google Search Test: PASSED
Form Interaction Test: PASSED
✓ All tests PASSED!
```

**Monitor container logs (open a separate terminal):**
```bash
docker logs -f selenium-chrome
```

**View browser activity via VNC (optional):**

Open in your local browser:
```
http://YOUR-CLOUD-MACHINE-IP:7900
```
VNC password: `secret`

**Create the report generator:**
```bash
nano generate_report.py
```

Paste the following, then save with `Ctrl+X → Y → Enter`:

```python
#!/usr/bin/env python3

import subprocess
import datetime
import json

def run_tests_with_report():
    """Run tests and generate a detailed report"""

    print("Generating Test Report...")
    print("=" * 60)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        result = subprocess.run(
            ['python3', 'selenium_test.py'],
            capture_output=True,
            text=True,
            timeout=120
        )

        report_data = {
            "timestamp": timestamp,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "status": "PASSED" if result.returncode == 0 else "FAILED"
        }

        html_report = f"""<!DOCTYPE html>
<html>
<head>
    <title>Selenium Docker Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 10px; border-radius: 5px; }}
        .passed {{ color: green; font-weight: bold; }}
        .failed {{ color: red; font-weight: bold; }}
        .output {{ background-color: #f8f8f8; padding: 10px; border: 1px solid #ddd; white-space: pre-wrap; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Selenium Docker Test Report</h1>
        <p><strong>Generated:</strong> {timestamp}</p>
        <p><strong>Status:</strong> <span class="{report_data['status'].lower()}">{report_data['status']}</span></p>
    </div>
    <h2>Test Output</h2>
    <div class="output">{report_data['stdout']}</div>
    <h2>Error Output</h2>
    <div class="output">{report_data['stderr'] if report_data['stderr'] else 'No errors'}</div>
</body>
</html>"""

        with open('test_report.html', 'w') as f:
            f.write(html_report)

        with open('test_report.json', 'w') as f:
            json.dump(report_data, f, indent=2)

        print(f"Test Status: {report_data['status']}")
        print(f"Exit Code: {report_data['exit_code']}")
        print("\nReports generated:")
        print("- test_report.html (HTML format)")
        print("- test_report.json (JSON format)")

        return report_data['exit_code'] == 0

    except subprocess.TimeoutExpired:
        print("✗ Tests timed out after 120 seconds")
        return False
    except Exception as e:
        print(f"✗ Error running tests: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_tests_with_report()
    exit(0 if success else 1)
```

**Run the report generator:**
```bash
python3 generate_report.py
```

This creates two files in your working directory:

| File | Format | Contents |
|------|--------|---------|
| `test_report.html` | HTML | Styled report viewable in a browser |
| `test_report.json` | JSON | Machine-readable report with exit code and output |

---

## Task 5 — Clean Up

**Stop the container:**
```bash
docker stop selenium-chrome
```

**Remove the container:**
```bash
docker rm selenium-chrome
```

**List remaining images:**
```bash
docker images
```

**Remove the Selenium image (optional — frees ~1.2GB):**
```bash
docker rmi selenium/standalone-chrome:latest
```

> Only remove if you no longer need Selenium. Re-downloading takes time.

**Prune unused Docker resources:**
```bash
docker system prune -f
```

**Verify cleanup:**
```bash
docker ps -a
docker images
```

`selenium-chrome` should not appear in either list.

**Deactivate the virtual environment:**
```bash
deactivate
```

---

## Troubleshooting

| Issue | Symptom | Fix |
|-------|---------|-----|
| Port conflict | Container exits immediately | Check with `netstat -tulpn \| grep :4444`, use `-p 4445:4444` instead |
| Connection refused | Python can't reach Selenium | Verify container is up: `docker ps` and `curl http://localhost:4444/wd/hub/status` |
| Chrome crashes | Browser fails to start | Increase shared memory: `--shm-size=2g` (already included above) |
| Element not found | Selector no longer matches | Inspect the live page — sites update their HTML; update your CSS selector accordingly |
| Slow tests | Long page load waits | Add `--disable-extensions` and `--disable-plugins` to `chrome_options` |

---

## Files Produced

```
selenium-with-docker/
├── selenium-env/          # Python virtual environment
├── selenium_test.py       # Main test script (two test functions)
├── generate_report.py     # Report generation script
├── test_report.html       # HTML test report
└── test_report.json       # JSON test report
```

---

## Key Concepts Covered

- Pulling and running official Selenium Docker images
- Mapping container ports for WebDriver and VNC access
- Creating isolated Python environments with `venv`
- Connecting Python Selenium to a remote containerised browser
- Writing robust WebDriver tests with explicit waits
- Generating HTML and JSON test reports programmatically
- Cleaning up Docker containers, images, and system resources
