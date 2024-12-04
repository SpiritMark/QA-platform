#!/bin/bash

# 设置默认值
TEST_PATH="test_cases/test_httpbin_pytest.py"
PORT=8080

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -t|--test)
        TEST_PATH="$2"
        shift
        shift
        ;;
        -p|--port)
        PORT="$2"
        shift
        shift
        ;;
        -m|--markers)
        MARKERS="$2"
        shift
        shift
        ;;
        *)
        shift
        ;;
    esac
done

# 运行测试
if [ -n "$MARKERS" ]; then
    python run_tests.py --test-path "$TEST_PATH" --markers "$MARKERS" --port "$PORT"
else
    python run_tests.py --test-path "$TEST_PATH" --port "$PORT"
fi 