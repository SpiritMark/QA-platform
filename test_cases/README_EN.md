Here’s an English description of the Python project:  

---

# Python Project Overview

## Directory Structure

- **`utils/`**: Utility functions and helper modules.  
- **`test_cases/`**: Test case directory containing all test scripts.  
- **`test_data/`**: Directory for storing test data in various formats.  
- **`reports/`**: Directory for generated test reports.  
- **`conftest.py`**: Configuration file for Pytest.  
- **`pytest.ini`**: Global configuration for Pytest.  

---

## Key Features

### 1. **Data-Driven Testing**
- Supports testing with data from:
  - **YAML**
  - **JSON**
  - **CSV**

### 2. **Test Reporting**
- Generate detailed test reports:
  - **Allure reports**  
  - **HTML reports**

### 3. **Parameterized Testing**
- Flexible parameterization methods:
  - **Direct parameterization**  
  - **Data file parameterization**  
  - **Fixture-based parameterization**

### 4. **Logging**
- Comprehensive logging for:
  - **Request logs**  
  - **Response logs**  
  - **Error logs**

---

## Getting Started

### Setting Up the Environment

#### 1. Create a Virtual Environment
```bash
python3 -m venv venv
```

#### 2. Activate the Virtual Environment
- **Linux / MacOS**:
  ```bash
  source venv/bin/activate
  ```
- **Windows**:
  ```cmd
  venv\Scripts\activate
  ```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### Running Tests

#### Run a specific test case with Allure report:
```bash
pytest test_cases/test_httpbin_pytest.py --alluredir=./reports/allure-results
```

#### Serve Allure report locally:
```bash
allure serve ./reports/allure-results/
```

---

## Contribution Guide

Contributions are welcome! Follow these steps to contribute:

1. **Fork the repository**  
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**:
   ```bash
   git commit -m "Add some AmazingFeature"
   ```
4. **Push to your branch**:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Submit a Pull Request**

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

- **Author**: [Your Name]  
- **Email**: [Your Email]  

--- 

This English description provides a clear and concise overview of the project, making it easy for contributors or users to understand and use.