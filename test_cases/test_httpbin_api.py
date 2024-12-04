import pytest
import logging
from typing import Dict, Any
from utils.data_loader import DataLoader, TestCase
from utils.keywords import Keywords
from ddt import ddt, data, file_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@ddt
class TestHttpbin:
    def setup_class(self):
        self.keywords = Keywords()
    
    @data(*DataLoader.load_test_cases("test_data/test_httpbin_api.json"))
    def test_json_cases(self, test_case: TestCase):
        """测试JSON文件中的用例"""
        self._execute_test_case(test_case)
    
    @data(*DataLoader.load_test_cases("test_data/test_httpbin_api.csv"))
    def test_csv_cases(self, test_case: TestCase):
        """测试CSV文件中的用例"""
        self._execute_test_case(test_case)
    
    def _execute_test_case(self, test_case: TestCase):
        """执行测试用例"""
        logger.info(f"开始执行测试用例: {test_case.case_name}")
        logger.info(f"测试描述: {test_case.description}")
        
        # 获取关键字方法
        keyword_func = getattr(self.keywords, test_case.keyword)
        
        # 执行关键字
        response = keyword_func(**test_case.params)
        
        # 验证结果
        self._verify_response(response, test_case.expected)
        
    def _verify_response(self, response, expected: Dict):
        """验证响应结果"""
        # 验证状态码
        if 'status_code' in expected:
            self.keywords.verify_status_code(response, expected['status_code'])
        
        # 验证响应字段
        for field, value in expected.items():
            if field != 'status_code':
                self.keywords.verify_response_field(response, field, value) 