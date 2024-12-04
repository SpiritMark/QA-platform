import pytest
from utils.data_loader import DataLoader
from utils.http_client import HTTPClient
from typing import Dict, Any
import os
import sys
import warnings
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 过滤警告
def pytest_configure(config):
    """配置pytest的全局设置"""
    warnings.filterwarnings(
        "ignore",
        category=Warning,
        message=".*urllib3 v2 only supports OpenSSL.*"
    )
    
    # 可以添加其他全局配置
    config.addinivalue_line(
        "markers",
        "smoke: 冒烟测试用例"
    )
    config.addinivalue_line(
        "markers",
        "api: API测试用例"
    )

def pytest_generate_tests(metafunc):
    if "test_case" in metafunc.fixturenames:
        # 获取测试用例文件路径
        test_file = metafunc.module.__file__
        case_file = test_file.replace('.py', '.yaml')
        
        # 加载测试用例
        test_cases = DataLoader.load_yaml(case_file)
        
        # 参数化测试用例
        metafunc.parametrize("test_case", test_cases)


# def pytest_collection_modifyitems(items):
#     for item in items:
#         item.name = item.name.encode("utf-8").decode("unicode_escape")
#         item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")

@pytest.fixture(scope="session")
def http_client():
    return HTTPClient() 