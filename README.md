# Pushover CLI

PushoverサービスでCLIから通知を送信するシンプルなツールです。

## 機能

- コマンドラインから簡単にPushover通知を送信
- **🆕 永続設定**: 一度設定すれば自動的に環境変数を使用
- 環境変数や設定ファイルからの認証情報読み込み
- 通知の優先度、タイトル、URL、音声などのカスタマイズ
- 複数の設定方法をサポート

## セットアップ

### 1. Pushoverアカウントの準備

1. [Pushover](https://pushover.net/)でアカウントを作成
2. [アプリケーション作成ページ](https://pushover.net/apps/build)でアプリを作成してトークンを取得
3. ダッシュボードでユーザーキーを確認

### 2. インストール

#### pip installで簡単インストール（推奨）

```bash
# PyPIからインストール（将来的に利用可能）
pip install pushover-cli

# または、開発版をGitHubから直接インストール
pip install git+https://github.com/your-username/pushover-cli.git

# ローカル開発版をインストール
git clone <このリポジトリ>
cd my_pushover
pip install -e .
```

#### 従来の方法

```bash
git clone <このリポジトリ>
cd my_pushover
chmod +x pushover_cli.py
```

### 3. 設定

#### ✨ A. 永続設定（推奨・NEW!）

一度設定すれば、以降は自動的に使用されます：

```bash
# 対話形式で設定
pushover config set

# または直接指定
pushover config set -t your_app_token -u your_user_key

# 設定確認
pushover config show

# 設定テスト
pushover config test

# 通知送信（設定後はこれだけ！）
pushover -m "Hello World"
```

#### B. コマンドライン引数（一時的な使用）
```bash
pushover -t your_app_token -u your_user_key -m "Hello World"
```

#### C. 環境変数（手動設定）
```bash
export PUSHOVER_TOKEN="your_app_token"
export PUSHOVER_USER="your_user_key"
pushover -m "Hello World"
```

#### D. 設定ファイル
`~/.pushover_config`ファイルを作成：
```
PUSHOVER_TOKEN=your_app_token
PUSHOVER_USER=your_user_key
```

## 使用方法

### 基本的な使用例

```bash
# 簡単なメッセージ送信
pushover -m "Hello World"

# タイトル付きメッセージ
pushover -m "サーバーが復旧しました" --title "システム通知"

# 優先度を指定
pushover -m "緊急！サーバーダウン" --title "緊急アラート" --priority 2

# URLを含むメッセージ
pushover -m "デプロイが完了しました" --url "https://example.com" --url-title "アプリを確認"

# 特定のデバイスに送信
pushover -m "モバイル専用通知" --device "iPhone"

# カスタム通知音
pushover -m "特別な通知" --sound "siren"
```

#### 従来の方法（開発版）

```bash
# 従来の方法でも利用可能
python pushover_cli.py -m "Hello World"
```

### 設定管理コマンド

```bash
# 設定を永続化（推奨）
pushover config set

# 現在の設定を表示
pushover config show

# 設定をテスト
pushover config test

# 設定をクリア
pushover config clear

# 設定のヘルプ
pushover config --help
```

### コマンドラインオプション

```
必須引数:
  -m, --message         送信するメッセージ

認証情報:
  -t, --token          Pushoverアプリトークン
  -u, --user           Pushoverユーザーキー

オプション:
  --title              通知のタイトル
  --priority {-2,-1,0,1,2}  優先度 (-2:最低, -1:低, 0:通常, 1:高, 2:緊急)
  --url                メッセージに含めるURL
  --url-title          URLのタイトル
  --device             送信先デバイス名
  --sound              通知音
  --config             設定ファイルのパス (デフォルト: ~/.pushover_config)

設定管理:
  config show          現在の設定を表示
  config set           設定を永続化
  config clear         設定をクリア
  config test          設定をテスト
```

### 優先度について

- **-2 (最低)**: 通知音なし、バナー表示なし
- **-1 (低)**: 静かな通知音
- **0 (通常)**: デフォルトの通知音
- **1 (高)**: 重要な通知音でバイパス
- **2 (緊急)**: 確認が必要（30秒ごとに再通知）

## 実用的な使用例

### システム監視
```bash
# ディスク容量チェック
if [ $(df / | tail -1 | awk '{print $5}' | sed 's/%//') -gt 90 ]; then
    pushover -m "ディスク使用量が90%を超えました" --title "システム警告" --priority 1
fi

# サービス監視
if ! systemctl is-active --quiet nginx; then
    pushover -m "Nginxサービスがダウンしています" --title "サービス障害" --priority 2
fi
```

### 自動化とスクリプト
```bash
# バックアップ完了通知
./backup_script.sh && pushover -m "バックアップが正常に完了しました" --title "バックアップ"

# 長時間実行タスクの完了通知
python long_running_task.py; pushover -m "長時間タスクが完了しました" --title "タスク完了"
```

## トラブルシューティング

### よくある問題

1. **トークンまたはユーザーキーが無効**
   - Pushoverダッシュボードで正しいトークンとユーザーキーを確認
   - アプリケーションが有効になっているか確認

2. **ネットワーク接続エラー**
   - インターネット接続を確認
   - ファイアウォール設定を確認

3. **文字化け**
   - メッセージにUTF-8文字が含まれている場合、適切にエンコードされているか確認

4. **永続設定が反映されない**
   - 新しいターミナルセッションを開始
   - または `source ~/.zshrc` （あなたのシェル設定ファイル）を実行

### デバッグモード

詳細なエラー情報が必要な場合は、Pythonのデバッグモードを使用：

```bash
python -u pushover_cli.py -m "テストメッセージ"
```

## 🆕 新機能ハイライト

### 永続設定機能
- **自動シェル検出**: bash, zsh, fish をサポート
- **設定ファイル管理**: `.bashrc`, `.zshrc` などに自動書き込み
- **安全な設定更新**: 既存設定の上書きと削除に対応
- **設定テスト**: 実際に通知を送信してテスト

### 使いやすさの向上
- **設定の優先順位**: 永続設定 > コマンドライン > 環境変数 > 設定ファイル
- **分かりやすいエラーメッセージ**: 設定方法を具体的に案内
- **サブコマンド対応**: `pushover config` で設定管理

## ライセンス

MIT License - 自由に使用、修正、配布可能です。

## 貢献

バグ報告や機能リクエストはGitHubのIssueでお知らせください。 