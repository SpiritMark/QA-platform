import pytest
from typing import Dict, Any

def test_api(test_case: Dict[str, Any], http_client):
    """执行API测试用例"""
    # 发送请求
    response = http_client.send_request(test_case)
    
    # 验证响应
    expected = test_case['expected_response']
    
    # 验证状态码
    assert response.status_code == expected['status_code']
    
    # 验证响应体
    if 'body' in expected:
        response_json = response.json()
        for key, value in expected['body'].items():
            assert response_json[key] == value 