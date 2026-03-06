
# Dheo Claveria Playwright Python BDD 2026

## Prerequisites
*   Python 3.8+
*   pip

## Installation Guide

### 1.Clone the git : 
```bash
git clone https://github.com/BlissCoders/playwright_fundamentals.git
```

### 2. Open project folder in IDE 
You can now open your preferred IDE and 'Open a Project Folder' and select the folder path you cloned.

And install the [Playwright Pytest plugin](https://playwright.dev) using this command :
```bash
   pip install -r requirements.txt
```

### 3. Create Virtual Environment
In your IDE, open a new terminal and paste the following commands : 
1. ```bash
   python -m venv .env
    ```
2. ```bash
   venv\Scripts\activate    # for windows
   source venv/bin/activate # for mac/linux
    ```

### 4. Test Script Execution 

* Run all tests in /tests directory:
   ```bash
   pytest tests
   ```
   
* Run specific tests using marks e.g.('login_only') in /tests directory:
   ```bash
   pytest tests -m "TC1"
   ```

* Run in test script Parallel(s):
   ```bash
   pytest tests -m "login" -n 2 #it will run in 2 parallel testing
   ```  
   ```bash
   pytest tests -m "login" -n auto #pytest will automatically distribute worker based on the tags scripts
   ```  
  
