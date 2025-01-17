from setuptools import setup, find_packages

setup(
    name="api-test-framework",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pytest==7.1.3",
        "pytest-html==4.1.1",
        "pytest-metadata==3.0.0",
        "ddt==1.7.1",
        "requests==2.31.0",
        "pyyaml==6.0.1",
        "jsonpath-ng>=1.5.0",
        "allure-pytest==2.9.45",
        "allure-python-commons==2.9.45",
        "urllib3>=2.0.0",
        "certifi>=2023.7.22"
    ],
) 