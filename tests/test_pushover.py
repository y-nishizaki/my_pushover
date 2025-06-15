#!/usr/bin/env python3
"""
Pushover CLI テストスクリプト

このスクリプトは実際のPushover APIを呼び出さずに、
CLI機能をテストするためのものです。
"""

import sys
import os
import subprocess
from unittest.mock import patch, MagicMock

# プロジェクトのルートディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_cli_help():
    """ヘルプメッセージのテスト"""
    print("=== ヘルプメッセージのテスト ===")
    result = subprocess.run([sys.executable, "pushover_cli.py", "--help"], 
                          capture_output=True, text=True)
    print("終了コード:", result.returncode)
    if result.returncode == 0:
        print("✅ ヘルプメッセージが正常に表示されました")
        print(result.stdout[:200] + "...")
    else:
        print("❌ ヘルプメッセージの表示に失敗しました")
        print(result.stderr)
    print()

def test_missing_args():
    """必須引数不足のテスト"""
    print("=== 必須引数不足のテスト ===")
    result = subprocess.run([sys.executable, "pushover_cli.py"], 
                          capture_output=True, text=True)
    print("終了コード:", result.returncode)
    if result.returncode != 0:
        print("✅ 必須引数不足が正しく検出されました")
    else:
        print("❌ 必須引数不足の検出に失敗しました")
    print()

def test_missing_credentials():
    """認証情報不足のテスト"""
    print("=== 認証情報不足のテスト ===")
    result = subprocess.run([sys.executable, "pushover_cli.py", "-m", "test"], 
                          capture_output=True, text=True)
    print("終了コード:", result.returncode)
    if result.returncode != 0 and "トークン" in result.stderr:
        print("✅ 認証情報不足が正しく検出されました")
    else:
        print("❌ 認証情報不足の検出に失敗しました")
    print("エラーメッセージ:", result.stderr.strip())
    print()

def test_mock_api_success():
    """API成功のモックテスト"""
    print("=== API成功のモックテスト ===")
    
    # 環境変数を設定してテスト実行
    env = os.environ.copy()
    env['PUSHOVER_TOKEN'] = 'test_token'
    env['PUSHOVER_USER'] = 'test_user'
    
    # モック用の一時的なスクリプトを作成
    mock_script = """
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unittest.mock import patch, MagicMock
import pushover_cli

# HTTPSConnectionをモック
with patch('http.client.HTTPSConnection') as mock_conn:
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'{"status": 1}'
    mock_conn.return_value.getresponse.return_value = mock_response
    
    # CLIを実行
    sys.argv = ['pushover_cli.py', '-m', 'テストメッセージ']
    try:
        pushover_cli.main()
        print("✅ モックAPIテストが成功しました")
    except SystemExit as e:
        if e.code == 0:
            print("✅ モックAPIテストが成功しました")
        else:
            print(f"❌ モックAPIテストが失敗しました (終了コード: {e.code})")
    except Exception as e:
        print(f"❌ モックAPIテストでエラーが発生しました: {e}")
"""
    
    with open('temp_mock_test.py', 'w') as f:
        f.write(mock_script)
    
    try:
        result = subprocess.run([sys.executable, 'temp_mock_test.py'], 
                              capture_output=True, text=True, env=env)
        print(result.stdout.strip())
        if result.stderr:
            print("エラー出力:", result.stderr.strip())
    finally:
        # 一時ファイルをクリーンアップ
        if os.path.exists('temp_mock_test.py'):
            os.remove('temp_mock_test.py')
    print()

def test_config_file():
    """設定ファイルのテスト"""
    print("=== 設定ファイルのテスト ===")
    
    # 一時的な設定ファイルを作成
    config_content = """PUSHOVER_TOKEN=test_token_from_config
PUSHOVER_USER=test_user_from_config"""
    
    with open('temp_config', 'w') as f:
        f.write(config_content)
    
    try:
        result = subprocess.run([
            sys.executable, "pushover_cli.py", 
            "--config", "temp_config",
            "-m", "設定ファイルテスト"
        ], capture_output=True, text=True)
        
        if "接続エラー" in result.stderr:
            print("✅ 設定ファイルが正しく読み込まれました（接続エラーは予期される動作）")
        else:
            print("設定ファイルテストの結果:")
            print("stdout:", result.stdout)
            print("stderr:", result.stderr)
    finally:
        # 一時ファイルをクリーンアップ
        if os.path.exists('temp_config'):
            os.remove('temp_config')
    print()

def main():
    """テストを実行"""
    print("Pushover CLI テストスイート")
    print("=" * 40)
    
    test_cli_help()
    test_missing_args()
    test_missing_credentials()
    test_mock_api_success()
    test_config_file()
    
    print("テスト完了！")
    print("\n実際の通知をテストするには、以下のコマンドを使用してください:")
    print("python pushover_cli.py -t YOUR_TOKEN -u YOUR_USER -m 'テストメッセージ'")

if __name__ == "__main__":
    main() 