#!/usr/bin/env python3
"""
Pushover CLI - コマンドラインインターフェース
"""

import argparse
import sys
import os
from .core import PushoverCLI, load_config_from_file
from .config import ConfigManager


def handle_config_command(args):
    """設定コマンドの処理"""
    config_manager = ConfigManager()
    
    if args.config_action == 'show':
        # 現在の設定を表示
        current_config = config_manager.get_current_config()
        shell = config_manager.detect_shell()
        config_file = config_manager.get_shell_config_file()
        
        print("🔧 Pushover CLI 現在の設定")
        print(f"シェル: {shell}")
        print(f"設定ファイル: {config_file}")
        print()
        print("環境変数:")
        for key, value in current_config.items():
            if value:
                masked_value = value[:8] + "..." if len(value) > 8 else value
                print(f"  {key}: {masked_value}")
            else:
                print(f"  {key}: (未設定)")
        
        # 設定ファイルから設定を読み込み
        file_config = load_config_from_file(os.path.expanduser("~/.pushover_config"))
        if file_config:
            print()
            print("設定ファイル (~/.pushover_config):")
            for key in ['PUSHOVER_TOKEN', 'PUSHOVER_USER']:
                value = file_config.get(key)
                if value:
                    masked_value = value[:8] + "..." if len(value) > 8 else value
                    print(f"  {key}: {masked_value}")
        
    elif args.config_action == 'set':
        # 設定を永続化
        token = args.token or input("Pushoverアプリトークンを入力してください: ").strip()
        user = args.user or input("Pushoverユーザーキーを入力してください: ").strip()
        
        if not token or not user:
            print("エラー: トークンとユーザーキーの両方が必要です", file=sys.stderr)
            sys.exit(1)
        
        success, message = config_manager.set_environment_variables(token, user)
        
        if success:
            print("✅", message)
            print()
            print(config_manager.show_setup_instructions())
            print()
            print("💡 ヒント: 新しいターミナルウィンドウを開くか、以下を実行して設定を反映してください:")
            shell = config_manager.detect_shell()
            config_file = config_manager.get_shell_config_file()
            print(f"  source {config_file}")
        else:
            print(f"❌ {message}", file=sys.stderr)
            sys.exit(1)
    
    elif args.config_action == 'clear':
        # 設定を削除
        success, message = config_manager.remove_environment_variables()
        
        if success:
            print("✅", message)
            print("💡 新しいターミナルセッションで変更が反映されます")
        else:
            print(f"❌ {message}", file=sys.stderr)
            sys.exit(1)
    
    elif args.config_action == 'test':
        # 設定をテスト
        current_config = config_manager.get_current_config()
        token = current_config.get('PUSHOVER_TOKEN')
        user = current_config.get('PUSHOVER_USER')
        
        if not token or not user:
            print("❌ 環境変数が設定されていません", file=sys.stderr)
            print("   以下のコマンドで設定してください: pushover config set", file=sys.stderr)
            sys.exit(1)
        
        # テスト通知を送信
        pushover = PushoverCLI(token, user)
        success, message = pushover.send_notification(
            message="🧪 Pushover CLI 設定テスト",
            title="設定テスト"
        )
        
        if success:
            print("✅ 設定テスト成功！通知が送信されました")
        else:
            print(f"❌ 設定テスト失敗: {message}", file=sys.stderr)
            sys.exit(1)


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="Pushover CLI - コマンドラインから通知を送信",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    # サブコマンドを作成
    subparsers = parser.add_subparsers(dest='command', help='利用可能なコマンド')
    
    # メイン送信コマンド（デフォルト）
    send_parser = subparsers.add_parser('send', help='通知を送信（デフォルト）', add_help=False)
    
    # 設定コマンド
    config_parser = subparsers.add_parser('config', help='設定管理')
    config_subparsers = config_parser.add_subparsers(dest='config_action', help='設定操作')
    
    # 設定サブコマンド
    config_show = config_subparsers.add_parser('show', help='現在の設定を表示')
    
    config_set = config_subparsers.add_parser('set', help='設定を永続化')
    config_set.add_argument('-t', '--token', help='Pushoverアプリトークン')
    config_set.add_argument('-u', '--user', help='Pushoverユーザーキー')
    
    config_clear = config_subparsers.add_parser('clear', help='設定をクリア')
    config_test = config_subparsers.add_parser('test', help='設定をテスト')
    
    # 引数が何もない場合は送信コマンドとして処理
    if len(sys.argv) == 1 or (len(sys.argv) > 1 and not sys.argv[1] in ['config']):
        # 送信コマンドの引数を追加
        parser.add_argument("-m", "--message", required=True, help="送信するメッセージ")
        parser.add_argument("-t", "--token", help="Pushoverアプリトークン")
        parser.add_argument("-u", "--user", help="Pushoverユーザーキー")
        parser.add_argument("--title", help="通知のタイトル")
        parser.add_argument("--priority", type=int, choices=[-2, -1, 0, 1, 2], 
                           default=0, help="優先度 (-2〜2、デフォルト: 0)")
        parser.add_argument("--url", help="メッセージに含めるURL")
        parser.add_argument("--url-title", help="URLのタイトル")
        parser.add_argument("--device", help="送信先デバイス名")
        parser.add_argument("--sound", help="通知音")
        parser.add_argument("--config", default="~/.pushover_config", 
                           help="設定ファイルのパス (デフォルト: ~/.pushover_config)")
        parser.add_argument("--version", action="version", version="pushover-cli 1.0.0")
        
        parser.epilog = """
使用例:
  pushover -m "Hello World"
  pushover -m "エラーが発生しました" --title "システムアラート" --priority 1
  pushover config set                    # 永続設定
  pushover config show                   # 設定確認
  pushover config test                   # 設定テスト

設定方法:
  1. 永続設定: pushover config set
  2. 環境変数: PUSHOVER_TOKEN, PUSHOVER_USER
  3. 設定ファイル: ~/.pushover_config

優先度:
  -2: 最低 (通知音なし)
  -1: 低 (静かな通知音)
   0: 通常 (デフォルト)
   1: 高 (重要な通知音)
   2: 緊急 (確認が必要)
        """
    
    args = parser.parse_args()
    
    # コマンドに応じて処理を分岐
    if args.command == 'config':
        handle_config_command(args)
        return
    
    # 送信コマンドの処理（デフォルト）
    if not hasattr(args, 'message'):
        parser.error("通知メッセージが必要です。-m オプションを使用してください。")
    
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
        print("  設定方法:", file=sys.stderr)
        print("    pushover config set    # 永続設定（推奨）", file=sys.stderr)
        print("    -t オプション          # 一時的な指定", file=sys.stderr)
        print("    PUSHOVER_TOKEN環境変数 # 手動設定", file=sys.stderr)
        sys.exit(1)
    
    if not user:
        print("エラー: Pushoverユーザーキーが指定されていません", file=sys.stderr)
        print("  設定方法:", file=sys.stderr)
        print("    pushover config set    # 永続設定（推奨）", file=sys.stderr)
        print("    -u オプション          # 一時的な指定", file=sys.stderr)
        print("    PUSHOVER_USER環境変数  # 手動設定", file=sys.stderr)
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