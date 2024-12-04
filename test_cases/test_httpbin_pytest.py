import pytest
import logging
from typing import Dict, Any
from utils.data_loader import DataLoader
from utils.keywords import Keywords
import json
import yaml
import csv
from pathlib import Path
import allure
from utils.ssl_helper import disable_ssl_warnings
import subprocess
from datetime import datetime

# 配置日志和禁用警告
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
disable_ssl_warnings()

@allure.epic("接口测试平台")
@allure.feature("HTTP接口测试")
class TestHttpbinPytest:
    """
    Httpbin API测试类
    
    主要测试内容：
    1. 参数化GET请求测试 - 测试不同参数组合
    2. 基于YAML/JSON/CSV数据的测试 - 测试数据驱动能力
    3. 不同HTTP方法组合测试 - 测试各种HTTP方法
    4. 状态码测试 - 测试不同响应状态
    5. 基于fixture的测试 - 测试参数化注入
    
    使用方法：
    pytest test_httpbin_pytest.py -v  # 运行所有测试
    pytest test_httpbin_pytest.py -m smoke  # 运行冒烟测试
    """
    
    @pytest.fixture(autouse=True)
    def setup_class(self):
        """初始化测试类，创建关键字实例"""
        self.keywords = Keywords()
    
    # 数据加载函数
    def get_yaml_data():
        """
        加载YAML格式的测试数据
        
        Returns:
            List[Dict]: 测试数据列表
        """
        yaml_file = Path(__file__).parent / "test_data/httpbin_data.yaml"
        with open(yaml_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def get_json_data():
        """
        加载JSON格式的测试数据
        
        Returns:
            List[Dict]: 测试数据列表
        """
        json_file = Path(__file__).parent / "test_data/httpbin_data.json"
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_csv_data():
        """
        加载CSV格式的测试数据
        
        Returns:
            List[Dict]: 测试数据列表，包含解析后的JSON字段
        """
        csv_file = Path(__file__).parent / "test_data/httpbin_data.csv"
        test_data = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # 解析CSV中的JSON字符串字段
                    row['params'] = json.loads(row['params'])
                    row['expected'] = json.loads(row['expected'])
                    test_data.append(row)
                except json.JSONDecodeError as e:
                    logger.error(f"解析JSON数据失败: {row}")
                    logger.error(f"错误信息: {str(e)}")
                    raise
        return test_data
    
    # 测试方法
    @allure.story("参数化GET请求")
    @allure.title("测试GET请求参数化")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.get
    @pytest.mark.parametrize("name,age,expected_status", [
        pytest.param("张三", "25", 200, ids="正常用户-验证基本参数"),
        pytest.param("李四", "30", 200, id="边界值测试-验证年龄边界"),
        pytest.param("王五", "35", 200, marks=pytest.mark.smoke, id="冒烟测试-验证基本功能"),
    ])
    def test_get_with_params(self, name: str, age: str, expected_status: int):
        """
        测试GET请求的参数处理
        
        测试步骤：
        1. 发送带参数的GET请求
        2. 验证响应状态码
        3. 验证响应数据中的参数
        
        Args:
            name: 用户名参数
            age: 年龄参数
            expected_status: 预期的响应状态码
        """
        with allure.step(f"发送GET请求，参数：name={name}, age={age}"):
            response = self.keywords.get_request(
                url="https://httpbin.org/get",
                params={"name": name, "age": age}
            )
        
        with allure.step(f"验证响应状态码为 {expected_status}"):
            assert response.status_code == expected_status
            
        with allure.step("验证响应数据"):
            response_data = response.json()
            with allure.step(f"验证name参数为: {name}"):
                assert response_data["args"]["name"] == name
            with allure.step(f"验证age参数为: {age}"):
                assert response_data["args"]["age"] == age
    
    @allure.story("YAML数据驱动测试")
    @allure.title("使用YAML数据测试接口")
    @pytest.mark.api
    @pytest.mark.parametrize("test_data", get_yaml_data(), ids=lambda x: f"YAML数据测试-{x['case_name']}")
    def test_with_yaml_data(self, test_data: Dict):
        """使用YAML数据参数化测试"""
        with allure.step(f"执行{test_data['keyword']}请求"):
            keyword_func = getattr(self.keywords, test_data["keyword"])
            response = keyword_func(**test_data["params"])
            
        with allure.step(f"验证响应状态码为 {test_data['expected']['status_code']}"):
            assert response.status_code == test_data["expected"]["status_code"]
    
    @pytest.mark.api
    @pytest.mark.parametrize("test_data", get_json_data(), ids=lambda x: f"JSON数据测试-{x['case_name']}")
    def test_with_json_data(self, test_data: Dict):
        """使用JSON数据参数化测试"""
        with allure.step(f"执行{test_data['keyword']}请求"):
            keyword_func = getattr(self.keywords, test_data["keyword"])
            response = keyword_func(**test_data["params"])
            
        with allure.step(f"验证响应状态码为 {test_data['expected']['status_code']}"):
            assert response.status_code == test_data["expected"]["status_code"]
    
    @pytest.mark.api
    @pytest.mark.parametrize("test_data", get_csv_data(), ids=lambda x: f"CSV数据测试-{x['case_name']}")
    def test_with_csv_data(self, test_data: Dict):
        """使用CSV数据参数化测试"""
        with allure.step(f"执行{test_data['keyword']}请求"):
            keyword_func = getattr(self.keywords, test_data["keyword"])
            response = keyword_func(**test_data["params"])
            
        with allure.step(f"验证响应状态码为 {test_data['expected']['status_code']}"):
            assert response.status_code == test_data["expected"]["status_code"]
    
    # 组合参数化
    @allure.story("状态码测试")
    @allure.title("测试不同状态码")
    @pytest.mark.api
    @pytest.mark.parametrize("method", ["GET", "POST"], ids=["GET方法测试", "POST方法测试"])
    @pytest.mark.parametrize("status_code", [200, 201, 404, 500], 
                           ids=["成功状态码", "创建成功状态码", "未找到状态码", "服务器错误状态码"])
    def test_status_codes(self, method: str, status_code: int):
        """测试不同的HTTP方法和状态码组合"""
        with allure.step(f"发送{method}请求到状态码{status_code}接口"):
            url = f"https://httpbin.org/status/{status_code}"
            if method == "GET":
                response = self.keywords.get_request(url=url)
            else:
                response = self.keywords.post_request(url=url)
                
        with allure.step(f"验证响应状态码为 {status_code}"):
            assert response.status_code == status_code
    
    # 使用fixture进行参数化
    @pytest.fixture(params=[
        pytest.param(("GET", "https://httpbin.org/get"), id="GET请求测试"),
        pytest.param(("POST", "https://httpbin.org/post"), id="POST请求测试"),
        pytest.param(("PUT", "https://httpbin.org/put"), id="PUT请求测试")
    ])
    def http_method_url(self, request):
        return request.param
    
    def test_with_fixture(self, http_method_url):
        """使用fixture参数化测试不同的HTTP方法"""
        method, url = http_method_url
        keyword_func = getattr(self.keywords, f"{method.lower()}_request")
        response = keyword_func(url=url)
        assert response.status_code == 200 

def main():
    """
    主函数，用于直接运行测试文件
    
    支持的命令行参数：
    -v, --verbose: 显示详细信息
    -m, --marker: 运行指定标记的测试
    --html: 生成HTML报告的路径
    --allure: 生成Allure报告的目录
    --no-warnings: 禁用警告信息
    --serve: 运行完成后启动报告服务
    
    示例：
    python test_httpbin_pytest.py --allure reports/allure-results
    python test_httpbin_pytest.py -m smoke --allure reports/allure-results --serve
    """
    import sys
    import argparse
    from datetime import datetime
    
    # 创建参数解析器
    parser = argparse.ArgumentParser(description="HTTP接口测试")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细信息")
    parser.add_argument("-m", "--marker", help="运行指定标记的测试")
    parser.add_argument("--html", help="生成HTML报告的路径")
    parser.add_argument("--allure", help="生成Allure报告的目录")
    parser.add_argument("--no-warnings", action="store_true", help="禁用警告信息")
    parser.add_argument("--serve", action="store_true", help="运行完成后启动报告服务")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 构建pytest参数
    pytest_args = [__file__, "-v", "-s"]
    
    if args.marker:
        pytest_args.extend(["-m", args.marker])
    
    if args.html:
        pytest_args.extend(["--html", args.html])
    
    result_dir = None
    if args.allure:
        # 使用时间戳创建唯一的结果目录
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_dir = f"{args.allure}/{timestamp}"
        pytest_args.extend(["--alluredir", result_dir])
        
        # 确保录存在
        Path(result_dir).mkdir(parents=True, exist_ok=True)
    
    if args.no_warnings:
        pytest_args.append("-p no:warnings")
    
    # 确保项目根目录在Python路径中
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    try:
        # 运行测试
        logger.info(f"开始执行测试，参数: {' '.join(pytest_args)}")
        exit_code = pytest.main(pytest_args)
        logger.info(f"测试执行完成，退出码: {exit_code}")
        
        # 如果生成了allure报告，则生成HTML报告
        if result_dir and Path(result_dir).exists():
            try:
                logger.info("正在生成Allure HTML报告...")
                report_dir = f"{args.allure}/html/{timestamp}"
                subprocess.run(
                    ["allure", "generate", result_dir, "-o", report_dir, "--clean"],
                    check=True
                )
                logger.info(f"报告已生成: {report_dir}")
                
                # 如果指定了serve参数，则启动报告服务
                if args.serve:
                    logger.info("启动报告服务...")
                    try:
                        subprocess.run(["allure", "serve", result_dir])
                    except KeyboardInterrupt:
                        logger.info("报告服务已停止")
                else:
                    logger.info(f"可以使用以下命令查看报告:")
                    logger.info(f"allure serve {result_dir}")
                    logger.info(f"或者打开HTML报告: {report_dir}/index.html")
                    
            except subprocess.CalledProcessError as e:
                logger.error(f"生成报告失败: {e}")
            except FileNotFoundError:
                logger.error("未找到allure命令，请确保已安装allure")
                logger.info("可以使用以下命令安装allure:")
                logger.info("Mac: brew install allure")
                logger.info("Windows: scoop install allure")
                
    except KeyboardInterrupt:
        logger.info("测试执行被用户中断")
        sys.exit(130)
    except Exception as e:
        logger.error(f"测试执行出错: {e}", exc_info=True)
        sys.exit(1)
    finally:
        # 返回测试执行的退出码
        sys.exit(exit_code)

if __name__ == "__main__":
    main()