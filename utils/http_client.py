import requests
from typing import Dict, Any
import logging
import json
from utils.ssl_helper import disable_ssl_warnings

try:
    from jsonpath_ng import parse as jsonpath_parse
except ImportError:
    logging.error("jsonpath_ng not found, trying to install...")
    import subprocess
    try:
        subprocess.check_call(["pip", "install", "jsonpath-ng"])
        from jsonpath_ng import parse as jsonpath_parse
    except Exception as e:
        logging.error(f"Failed to install jsonpath_ng: {e}")
        raise

logger = logging.getLogger(__name__)

class HTTPClient:
    """
    HTTP客户端类，用于处理HTTP请求和响应
    
    主要功能：
    1. 发送HTTP请求
    2. 处理请求参数模板
    3. 提取响应数据
    4. 管理会话上下文
    
    属性:
        session (requests.Session): 用于维持HTTP会话
        context (dict): 存储提取的变量，用于参数替换
    """
    
    def __init__(self):
        """
        初始化HTTP客户端
        - 创建会话对象
        - 初始化上下文字典
        - 禁用SSL警告
        """
        self.session = requests.Session()
        self.context = {}
        disable_ssl_warnings()
    
    def send_request(self, case: Dict[str, Any]) -> requests.Response:
        """
        发送HTTP请求
        
        Args:
            case: 测试用例字典，包含以下字段：
                - url: 请求URL
                - method: 请求方法（GET, POST等）
                - headers: 请求头（可选）
                - params: 查询参数（可选）
                - body: 请求体（可选）
                - extract: 需要提取的响应数据（可选）
        
        Returns:
            requests.Response: 响应对象
        
        Raises:
            requests.exceptions.RequestException: 请求发生错误时抛出
        """
        try:
            # 处理URL中的动态参数
            url = self._process_template(case['url'])
            
            # 处理请求参数
            headers = self._process_template(case.get('headers', {}))
            params = self._process_template(case.get('params', {}))
            body = self._process_template(case.get('body', {}))
            
            # 记录请求信息
            logger.info(f"请求URL: {url}")
            logger.info(f"请求方法: {case['method']}")
            logger.info(f"请求头: {json.dumps(headers, ensure_ascii=False)}")
            if params:
                logger.info(f"查询参数: {json.dumps(params, ensure_ascii=False)}")
            if body:
                logger.info(f"请求体: {json.dumps(body, ensure_ascii=False)}")
            
            # 发送请求
            response = self.session.request(
                method=case['method'],
                url=url,
                headers=headers,
                params=params,
                json=body if body else None,
                timeout=10  # 添加超时设置
            )
            
            # 提取需要的数据
            if 'extract' in case:
                self._extract_data(response, case['extract'])
            
            return response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"请求发生错误: {str(e)}")
            raise
    
    def _process_template(self, template: Any) -> Any:
        """
        处理模板中的变量替换
        
        支持在字符串中使用 {variable} 格式的变量，
        变量值从context中获取
        
        Args:
            template: 要处理的模板，可以是字符串或字典
        
        Returns:
            处理后的值，保持原始类型
        """
        if isinstance(template, str):
            for key, value in self.context.items():
                template = template.replace(f"{{{key}}}", str(value))
            return template
        elif isinstance(template, dict):
            return {k: self._process_template(v) for k, v in template.items()}
        return template
    
    def _extract_data(self, response: requests.Response, extract_dict: Dict[str, str]):
        """
        从响应中提取数据并存储到上下文中
        
        Args:
            response: 响应对象
            extract_dict: 提取规则字典，格式为 {key: jsonpath表达式}
        
        示例:
            extract_dict = {
                "token": "$.body.token",
                "user_id": "$.body.user.id"
            }
        """
        response_data = {
            'body': response.json(),
            'headers': dict(response.headers),
            'status_code': response.status_code
        }
        
        for key, expr in extract_dict.items():
            if expr.startswith('$.'):
                try:
                    jsonpath_expr = jsonpath_parse(expr)
                    matches = [match.value for match in jsonpath_expr.find(response_data)]
                    if matches:
                        self.context[key] = matches[0]
                        logger.info(f"提取数据: {key} = {matches[0]}")
                except Exception as e:
                    logger.error(f"提取数据失败: {e}")
                    logger.error(f"表达式: {expr}")
                    logger.error(f"数据: {response_data}")
                    raise
    