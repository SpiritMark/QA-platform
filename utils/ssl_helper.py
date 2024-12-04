import warnings
import urllib3
import logging

logger = logging.getLogger(__name__)

def disable_ssl_warnings():
    """
    禁用SSL警告的通用方法
    
    这个函数会尝试禁用所有常见的SSL相关警告，包括：
    - InsecureRequestWarning: 用于禁用不安全HTTPS请求的警告
    - SecurityWarning: 用于禁用一般安全相关的警告
    """
    try:
        # 禁用所有urllib3警告
        urllib3.disable_warnings()
        
        # 禁用特定警告
        warnings.filterwarnings('ignore', category=urllib3.exceptions.InsecureRequestWarning)
        warnings.filterwarnings('ignore', category=urllib3.exceptions.SecurityWarning)
        warnings.filterwarnings('ignore', message='.*OpenSSL.*')
        
        logger.debug("成功禁用SSL警告")
    except Exception as e:
        logger.warning(f"禁用SSL警告时出错: {e}") 