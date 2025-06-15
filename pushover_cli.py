#!/usr/bin/env python3
"""
Pushover CLI - コマンドラインからPushover通知を送信するツール

使用方法:
    python pushover_cli.py -t <token> -u <user> -m <message> [オプション]

必要な設定:
    - Pushoverアプリトークン（https://pushover.net/apps/build）
    - Pushoverユーザーキー（ダッシュボードで確認可能）
"""

import argparse
import http.client
import urllib.parse
import json
import sys
import os
from typing import Optional, Tuple


class PushoverCLI:
    """Pushover通知を送信するCLIクラス"""
    
    API_HOST = "api.pushover.net"
    API_PORT = 443
    API_PATH = "/1/messages.json"
    
    def __init__(self, token: str, user: str):
        self.token = token
        self.user = user
    
    def send_notification(
        self,
        message: str,
        title: Optional[str] = None,
        priority: int = 0,
        url: Optional[str] = None,
        url_title: Optional[str] = None,
        device: Optional[str] = None,
        sound: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Pushover通知を送信
        
        Args:
            message: 送信するメッセージ
            title: 通知のタイトル（オプション）
            priority: 優先度 (-2: 最低, -1: 低, 0: 通常, 1: 高, 2: 緊急)
            url: メッセージに含めるURL（オプション）
            url_title: URLのタイトル（オプション）
            device: 送信先デバイス（オプション）
            sound: 通知音（オプション）
            
        Returns:
            (成功フラグ, レスポンスメッセージ)
        """
        
        # リクエストデータを構築
        data = {
            "token": self.token,
            "user": self.user,
            "message": message,
            "priority": str(priority)
        }
        
        # オプションパラメータを追加
        if title:
            data["title"] = title
        if url:
            data["url"] = url
        if url_title:
            data["url_title"] = url_title
        if device:
            data["device"] = device
        if sound:
            data["sound"] = sound
        
        try:
            # HTTPS接続を確立
            conn = http.client.HTTPSConnection(f"{self.API_HOST}:{self.API_PORT}")
            
            # POSTリクエストを送信
            conn.request(
                "POST",
                self.API_PATH,
                urllib.parse.urlencode(data),
                {"Content-type": "application/x-www-form-urlencoded"}
            )
            
            # レスポンスを取得
            response = conn.getresponse()
            response_data = response.read().decode('utf-8')
            
            # レスポンスをJSON解析
            response_json = json.loads(response_data)
            
            if response.status == 200 and response_json.get("status") == 1:
                return True, "通知が正常に送信されました"
            else:
                error_messages = response_json.get("errors", ["不明なエラー"])
                return False, f"送信エラー: {', '.join(error_messages)}"
                
        except Exception as e:
            return False, f"接続エラー: {str(e)}"
        finally:
            conn.close()


def load_config_from_file(config_path: str) -> dict:
    """設定ファイルから設定を読み込み"""
    if not os.path.exists(config_path):
        return {}
    
    try:
        with open(config_path, 'r') as f:
            config = {}
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
            return config
    except Exception:
        return {}


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="Pushover CLI - コマンドラインから通知を送信",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  %(prog)s -t abc123 -u user123 -m "Hello World"
  %(prog)s -t abc123 -u user123 -m "エラーが発生しました" --title "システムアラート" --priority 1
  %(prog)s -m "テストメッセージ"  # 環境変数または設定ファイルからtoken/userを取得

設定方法:
  1. 環境変数: PUSHOVER_TOKEN, PUSHOVER_USER
  2. 設定ファイル: ~/.pushover_config
     例:
     PUSHOVER_TOKEN=your_app_token_here
     PUSHOVER_USER=your_user_key_here

優先度:
  -2: 最低 (通知音なし)
  -1: 低 (静かな通知音)
   0: 通常 (デフォルト)
   1: 高 (重要な通知音)
   2: 緊急 (確認が必要)
        """
    )
    
    # 必須引数
    parser.add_argument("-m", "--message", required=True, help="送信するメッセージ")
    
    # 認証情報
    parser.add_argument("-t", "--token", help="Pushoverアプリトークン")
    parser.add_argument("-u", "--user", help="Pushoverユーザーキー")
    
    # オプション引数
    parser.add_argument("--title", help="通知のタイトル")
    parser.add_argument("--priority", type=int, choices=[-2, -1, 0, 1, 2], 
                       default=0, help="優先度 (-2〜2、デフォルト: 0)")
    parser.add_argument("--url", help="メッセージに含めるURL")
    parser.add_argument("--url-title", help="URLのタイトル")
    parser.add_argument("--device", help="送信先デバイス名")
    parser.add_argument("--sound", help="通知音")
    parser.add_argument("--config", default="~/.pushover_config", 
                       help="設定ファイルのパス (デフォルト: ~/.pushover_config)")
    
    args = parser.parse_args()
    
    # 設定の取得（優先順位: コマンドライン引数 > 環境変数 > 設定ファイル）
    config_path = os.path.expanduser(args.config)
    config = load_config_from_file(config_path)
    
    token = (args.token or 
             os.environ.get("PUSHOVER_TOKEN") or 
             config.get("PUSHOVER_TOKEN"))
    
    user = (args.user or 
            os.environ.get("PUSHOVER_USER") or 
            config.get("PUSHOVER_USER"))
    
    # 必須パラメータのチェック
    if not token:
        print("エラー: Pushoverトークンが指定されていません", file=sys.stderr)
        print("  -t オプション、PUSHOVER_TOKEN環境変数、または設定ファイルで指定してください", file=sys.stderr)
        sys.exit(1)
    
    if not user:
        print("エラー: Pushoverユーザーキーが指定されていません", file=sys.stderr)
        print("  -u オプション、PUSHOVER_USER環境変数、または設定ファイルで指定してください", file=sys.stderr)
        sys.exit(1)
    
    # PushoverCLIインスタンスを作成
    pushover = PushoverCLI(token, user)
    
    # 通知を送信
    success, message = pushover.send_notification(
        message=args.message,
        title=args.title,
        priority=args.priority,
        url=args.url,
        url_title=args.url_title,
        device=args.device,
        sound=args.sound
    )
    
    # 結果を出力
    if success:
        print(message)
        sys.exit(0)
    else:
        print(f"エラー: {message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()