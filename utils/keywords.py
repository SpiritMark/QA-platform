from typing import Dict, Any
import logging
from utils.http_client import HTTPClient

logger = logging.getLogger(__name__)

class Keywords:
    def __init__(self):
        self.http_client = HTTPClient()
        
    def get_request(self, url: str, params: Dict = None, headers: Dict = None) -> Dict:
        """发送GET请求的关键字"""
        case = {
            'method': 'GET',
            'url': url,
            'params': params,
            'headers': headers
        }
        return self.http_client.send_request(case)
    
    def post_request(self, url: str, data: Dict = None, headers: Dict = None) -> Dict:
        """发送POST请求的关键字"""
        case = {
            'method': 'POST',
            'url': url,
            'body': data,
            'headers': headers
        }
        return self.http_client.send_request(case)
    
    def put_request(self, url: str, data: Dict = None, headers: Dict = None) -> Dict:
        """发送PUT请求的关键字"""
        case = {
            'method': 'PUT',
            'url': url,
            'body': data,
            'headers': headers
        }
        return self.http_client.send_request(case)
    
    def verify_status_code(self, response: Dict, expected_code: int):
        """验证状态码的关键字"""
        assert response.status_code == expected_code, \
            f"状态码不匹配，期望 {expected_code}，实际 {response.status_code}"
    
    def verify_response_field(self, response: Dict, field_path: str, expected_value: Any):
        """验证响应字段的关键字"""
        actual_value = self.http_client._extract_data(response, {field_path: field_path})
        assert actual_value == expected_value, \
            f"字段值不匹配，期望 {expected_value}，实际 {actual_value}" 