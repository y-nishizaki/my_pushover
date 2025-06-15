"""
Pushover CLI - コマンドラインからPushover通知を送信するツール

シンプルで使いやすいPushover通知CLI
"""

__version__ = "1.0.0"
__author__ = "Pushover CLI"
__email__ = ""
__description__ = "コマンドラインからPushover通知を送信するシンプルなツール"

from .core import PushoverCLI
from .cli import main
from .config import ConfigManager

__all__ = ['PushoverCLI', 'main', 'ConfigManager'] 