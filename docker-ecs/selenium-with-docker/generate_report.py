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
