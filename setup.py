#!/usr/bin/env python3
"""
Pushover CLI セットアップスクリプト
"""

from setuptools import setup, find_packages
import os

# README.mdファイルを読み込む
def read_long_description():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

# バージョン情報を取得
def get_version():
    version_file = "pushover_cli/__init__.py"
    with open(version_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    return "1.0.0"

setup(
    name="pushover-cli",
    version=get_version(),
    author="Pushover CLI Team",
    author_email="",
    description="コマンドラインからPushover通知を送信するシンプルなツール",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/pushover-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        # 標準ライブラリのみ使用のため、依存関係なし
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pushover=pushover_cli.cli:main",
        ],
    },
    keywords="pushover notification cli command-line alert monitoring",
    project_urls={
        "Bug Reports": "https://github.com/your-username/pushover-cli/issues",
        "Source": "https://github.com/your-username/pushover-cli",
        "Documentation": "https://github.com/your-username/pushover-cli#readme",
    },
    include_package_data=True,
    zip_safe=False,
)