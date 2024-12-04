#!/usr/bin/env python3
import argparse
import logging
import sys
from pathlib import Path
from utils.test_runner import TestRunner

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def setup_logging(debug: bool = False):
    """
    配置日志系统
    
    Args:
        debug: 是否启用调试模式，True时显示更详细的日志
    """
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def main():
    """
    主函数，处理命令行参数并执行测试
    
    支持的命令行参数：
    --test-path: 指定测试文件或目录
    --markers: 指定要运行的测试标记
    --port: 指定报告服务端口
    --no-serve: 不启动报告服务
    --clean: 清理旧报告
    --max-reports: 保留的报告数量
    --debug: 启用调试日志
    
    使用示例：
    python run_tests.py --test-path test_cases/test_httpbin_pytest.py
    python run_tests.py --markers smoke
    python run_tests.py --clean --max-reports 3
    """
    parser = argparse.ArgumentParser(description="测试运行器")
    parser.add_argument("--test-path", help="测试文件或目录路径")
    parser.add_argument("--markers", help="要运行的测试标记")
    parser.add_argument("--port", type=int, default=8080, help="报告服务端口")
    parser.add_argument("--no-serve", action="store_true", help="不启动报告服务")
    parser.add_argument("--clean", action="store_true", help="清理旧报告")
    parser.add_argument("--max-reports", type=int, default=5, help="保留的报告数量")
    parser.add_argument("--debug", action="store_true", help="启用调试日志")
    
    args = parser.parse_args()
    
    # 设置日志级别
    setup_logging(args.debug)
    
    try:
        logger.info("开始执行测试...")
        runner = TestRunner()
        
        # 清理旧报告
        if args.clean:
            logger.info("清理旧报告...")
            runner.clean_old_results(args.max_reports)
        
        # 运行测试
        logger.info(f"运行测试: {args.test_path or '所有测试'}")
        result_path = runner.run_tests(args.test_path, args.markers)
        
        # 生成报告
        logger.info("生成测试报告...")
        report_path = runner.generate_report(result_path)
        logger.info(f"报告已生成: {report_path}")
        
        # 启动报告服务
        if not args.no_serve:
            logger.info(f"启动报告服务，端口: {args.port}")
            runner.serve_report(result_path, args.port)
            
    except KeyboardInterrupt:
        logger.info("用户中断执行")
        sys.exit(130)
    except Exception as e:
        logger.error(f"执行失败: {e}", exc_info=args.debug)
        sys.exit(1)
    else:
        logger.info("测试执行完成")

# python run_tests.py --test-path test_cases/test_httpbin_pytest.py
if __name__ == "__main__":
    main() 