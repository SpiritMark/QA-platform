import subprocess
import os
from pathlib import Path
from datetime import datetime
import logging
import sys
import shutil

logger = logging.getLogger(__name__)

class TestRunner:
    def __init__(self):
        self.project_dir = Path(__file__).parent.parent
        self.reports_dir = self.project_dir / "reports"
        self.allure_results = self.reports_dir / "allure-results"
        self.allure_reports = self.reports_dir / "allure-reports"
        self.test_dir = self.project_dir / "test_cases"
        
        # 创建必要的目录
        for dir_path in [self.reports_dir, self.allure_results, self.allure_reports]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # 检查依赖
        self._check_dependencies()
        # 检查allure命令
        self._check_allure_installation()
    
    def _check_dependencies(self):
        """检查必要的依赖是否已安装"""
        try:
            import pytest
            import allure
            from jsonpath_ng import parse
            logger.info("所有依赖检查通过")
        except ImportError as e:
            logger.error(f"缺少必要的依赖: {e}")
            logger.info("请执行: pip install -r requirements.txt")
            sys.exit(1)
    
    def _check_allure_installation(self):
        """检查allure是否已安装"""
        try:
            subprocess.run(["allure", "--version"], 
                         check=True, 
                         capture_output=True, 
                         text=True)
        except FileNotFoundError:
            logger.error("未找到allure命令，请先安装allure。")
            logger.info("Mac上可以使用: brew install allure")
            logger.info("Windows上可以使用: scoop install allure")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            logger.error(f"检查allure安装时出错: {e}")
            sys.exit(1)
    
    def run_tests(self, test_path: str = None, markers: str = None):
        """运行测试并生成报告"""
        # 构建pytest命令
        cmd = ["python", "-m", "pytest", "-v"]
        
        # 处理测试路径
        if test_path:
            test_path = Path(test_path)
        else:
            test_path = self.test_dir
            
        if not test_path.exists():
            raise FileNotFoundError(f"测试路径不存在: {test_path}")
        
        cmd.append(str(test_path))
        
        # 添加markers
        if markers:
            cmd.extend(["-m", markers])
            
        # 添加allure参数
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_path = self.allure_results / timestamp
        result_path.mkdir(parents=True, exist_ok=True)
        cmd.extend(["--alluredir", str(result_path)])
        
        # 运行测试
        try:
            logger.info(f"执行命令: {' '.join(cmd)}")
            env = os.environ.copy()
            env["PYTHONPATH"] = str(self.project_dir)
            process = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
                env=env,
                cwd=self.project_dir
            )
            if process.stdout:
                logger.info(process.stdout)
            if process.stderr:
                logger.warning(process.stderr)
            logger.info("测试执行完成")
            return result_path
        except subprocess.CalledProcessError as e:
            logger.error(f"测试执行失败: {e}")
            if e.stdout:
                logger.error(f"标准输出: {e.stdout}")
            if e.stderr:
                logger.error(f"错误输出: {e.stderr}")
            raise
    
    def generate_report(self, result_path: Path):
        """生成HTML报告"""
        if not result_path.exists():
            raise FileNotFoundError(f"结果目录不存在: {result_path}")
            
        report_path = self.allure_reports / result_path.name
        cmd = ["allure", "generate", str(result_path), "-o", str(report_path), "--clean"]
        
        try:
            logger.info(f"生成报告: {' '.join(cmd)}")
            process = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            logger.info(process.stdout)
            if process.stderr:
                logger.warning(process.stderr)
            return report_path
        except subprocess.CalledProcessError as e:
            logger.error(f"生成报告失败: {e}")
            logger.error(f"错误输出: {e.stderr}")
            raise
    
    def serve_report(self, result_path: Path, port: int = 8080):
        """启动本地服务查看报告"""
        if not result_path.exists():
            raise FileNotFoundError(f"结果目录不存在: {result_path}")
            
        cmd = ["allure", "serve", str(result_path), "-p", str(port)]
        
        try:
            logger.info(f"启动报告服务: {' '.join(cmd)}")
            subprocess.run(cmd)
        except KeyboardInterrupt:
            logger.info("报告服务已停止")
        except subprocess.CalledProcessError as e:
            logger.error(f"启动报告服务失败: {e}")
            raise
    
    def clean_old_results(self, max_dirs: int = 5):
        """清理旧的测试结果"""
        try:
            for dir_path in [self.allure_results, self.allure_reports]:
                if not dir_path.exists():
                    continue
                    
                all_results = sorted(dir_path.glob("*"), key=os.path.getctime, reverse=True)
                for old_dir in all_results[max_dirs:]:
                    if old_dir.is_dir():
                        shutil.rmtree(old_dir)
                        logger.info(f"已删除旧报告: {old_dir}")
        except Exception as e:
            logger.error(f"清理旧报告失败: {e}")
            raise 