"""
Pushover CLI コアモジュール
"""

import http.client
import urllib.parse
import json
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
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
            return config
    except Exception:
        return {} 