import yaml
import json
import csv
import os
from typing import Dict, List, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class TestCase:
    case_name: str
    description: str
    keyword: str
    params: Dict[str, Any]
    expected: Dict[str, Any]

class DataLoader:
    @staticmethod
    def load_test_cases(file_path: str) -> List[TestCase]:
        """根据文件扩展名自动选择加载器"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.yaml' or ext == '.yml':
            return DataLoader._load_yaml(file_path)
        elif ext == '.json':
            return DataLoader._load_json(file_path)
        elif ext == '.csv':
            return DataLoader._load_csv(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {ext}")
    
    @staticmethod
    def _load_yaml(file_path: str) -> List[TestCase]:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return [DataLoader._convert_to_test_case(case) for case in data]
    
    @staticmethod
    def _load_json(file_path: str) -> List[TestCase]:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [DataLoader._convert_to_test_case(case) for case in data]
    
    @staticmethod
    def _load_csv(file_path: str) -> List[TestCase]:
        test_cases = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, dialect='excel')
            for row in reader:
                try:
                    params = json.loads(row['params'].strip())
                    expected = json.loads(row['expected'].strip())
                    test_case = TestCase(
                        case_name=row['case_name'],
                        description=row['description'],
                        keyword=row['keyword'],
                        params=params,
                        expected=expected
                    )
                    test_cases.append(test_case)
                except json.JSONDecodeError as e:
                    logger.error(f"行数据: {row}")
                    logger.error(f"params: {row['params']}")
                    logger.error(f"expected: {row['expected']}")
                    logger.error(f"错误: {str(e)}")
                    raise
        return test_cases
    
    @staticmethod
    def _convert_to_test_case(data: Dict) -> TestCase:
        return TestCase(
            case_name=data['case_name'],
            description=data.get('description', ''),
            keyword=data['keyword'],
            params=data.get('params', {}),
            expected=data.get('expected', {})
        )