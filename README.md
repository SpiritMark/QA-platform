# 项目目录说明与功能概览  

[English](./README_EN.md) | 简体中文

## 目录结构  

- **`utils/`**: 工具类目录，包含各种辅助功能模块  
- **`test_cases/`**: 测试用例目录  
- **`test_data/`**: 测试数据目录  
- **`reports/`**: 测试报告目录  
- **`conftest.py`**: Pytest 配置文件  
- **`pytest.ini`**: Pytest 全局配置文件  

## 核心功能  

### 1. 数据驱动测试  
- 支持多种格式的数据驱动：  
  - **YAML**  
  - **JSON**  
  - **CSV**  

### 2. 测试报告生成  
- **Allure 报告**  
- **HTML 报告**  

### 3. 参数化测试  
- **直接参数化**  
- **数据文件参数化**  
- **Fixture 参数化**  

### 4. 日志记录  
- **请求日志**  
- **响应日志**  
- **错误日志**  

---

## 使用指南  

### 环境设置  

#### 1. 创建虚拟环境  
```bash  
python3 -m venv venv  
```  

#### 2. 激活虚拟环境  
- **Linux / MacOS**:  
  ```bash  
  source venv/bin/activate  
  ```  
- **Windows**:  
  ```cmd  
  venv\Scripts\activate  
  ```  

#### 3. 安装依赖  
```bash  
pip install -r requirements.txt  
```  

### 运行测试  

#### 运行单个测试用例并生成 Allure 报告：  
```bash  
pytest test_cases/test_httpbin_pytest.py --alluredir=./reports/allure-results  
```  

#### 本地查看 Allure 报告：  
```bash  
allure serve ./reports/allure-results/  
```  

---

## 贡献指南  

我们欢迎任何形式的贡献！请按照以下步骤操作：  

1. **Fork 项目**  
2. **创建分支**:  
   ```bash  
   git checkout -b feature/AmazingFeature  
   ```  
3. **提交更改**:  
   ```bash  
   git commit -m "Add some AmazingFeature"  
   ```  
4. **推送到分支**:  
   ```bash  
   git push origin feature/AmazingFeature  
   ```  
5. **创建 Pull Request**  

---

## 许可证  

本项目使用 [MIT License](LICENSE) 开源。  

---

## 联系方式  

- **作者**: Spiritmark  
- **邮箱**: 2509919428@qq.com  

---
