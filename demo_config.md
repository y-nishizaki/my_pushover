# 🔧 Pushover CLI 永続設定機能デモ

## ✨ 新機能: 一度設定すれば永続的に使用可能！

環境変数を一度設定すれば、以降は自動的にそれを使用する機能が追加されました。

## 🚀 使用方法

### 1. 永続設定の作成

```bash
# 対話形式で設定（推奨）
pushover config set

# または、直接指定
pushover config set -t your_app_token -u your_user_key
```

### 2. 設定の確認

```bash
# 現在の設定状況を表示
pushover config show
```

出力例：
```
🔧 Pushover CLI 現在の設定
シェル: zsh
設定ファイル: /Users/yn/.zshrc

環境変数:
  PUSHOVER_TOKEN: abc12345...
  PUSHOVER_USER: user6789...
```

### 3. 設定のテスト

```bash
# 実際に通知を送信してテスト
pushover config test
```

### 4. 簡単な通知送信

設定後は、毎回認証情報を指定する必要がありません：

```bash
# 超簡単！認証情報は自動で読み込まれます
pushover -m "設定完了！"
pushover -m "サーバー監視アラート" --title "警告" --priority 1
pushover -m "デプロイ完了" --title "CI/CD" --url "https://app.example.com"
```

## 🛠️ 技術的な仕組み

### サポートするシェル
- **bash**: `.bashrc`, `.bash_profile`
- **zsh**: `.zshrc`, `.zprofile`  
- **fish**: `.config/fish/config.fish`

### 設定ファイルの書き込み例

`.zshrc` に以下のような設定が自動的に追加されます：

```bash
# === Pushover CLI Configuration - Start ===
export PUSHOVER_TOKEN="your_app_token"
export PUSHOVER_USER="your_user_key"
# === Pushover CLI Configuration - End ===
```

### 設定の優先順位

1. **コマンドライン引数** (`-t`, `-u`)
2. **環境変数** (`PUSHOVER_TOKEN`, `PUSHOVER_USER`)
3. **設定ファイル** (`~/.pushover_config`)

## 📋 管理コマンド

### 設定表示
```bash
pushover config show
```

### 設定変更
```bash
pushover config set -t new_token -u new_user
```

### 設定削除
```bash
pushover config clear
```

### 設定テスト
```bash
pushover config test
```

## ⚡ デモシナリオ

### 初回セットアップ

```bash
# 1. 設定を対話形式で入力
$ pushover config set
Pushoverアプリトークンを入力してください: abc123...
Pushoverユーザーキーを入力してください: user456...

✅ 設定が /Users/yn/.zshrc に保存されました

🔧 Pushover CLI 永続設定手順

現在のシェル: zsh
設定ファイル: /Users/yn/.zshrc

設定後は新しいターミナルセッションで自動的に環境変数が読み込まれます。
現在のセッションで即座に適用するには以下を実行してください:

source /Users/yn/.zshrc

💡 ヒント: 新しいターミナルウィンドウを開くか、以下を実行して設定を反映してください:
  source /Users/yn/.zshrc
```

### 新しいターミナルセッション

```bash
# 新しいターミナルを開く、または source で反映

# 2. 設定を確認
$ pushover config show
🔧 Pushover CLI 現在の設定
シェル: zsh
設定ファイル: /Users/yn/.zshrc

環境変数:
  PUSHOVER_TOKEN: abc12345...
  PUSHOVER_USER: user6789...

# 3. テスト送信
$ pushover config test
✅ 設定テスト成功！通知が送信されました

# 4. 通常利用（認証情報不要！）
$ pushover -m "永続設定のテスト"
通知が正常に送信されました

$ pushover -m "サーバー復旧" --title "システム通知" --priority 1
通知が正常に送信されました
```

## 🎯 メリット

1. **一度設定すれば永続的**: 毎回トークンを入力する必要なし
2. **自動シェル検出**: 使用中のシェルを自動判別
3. **安全な更新**: 既存設定の安全な更新・削除
4. **複数設定方法対応**: 一時的な上書きも可能
5. **設定テスト**: 実際の通知でテスト可能

## 🔧 トラブルシューティング

### 設定が反映されない場合

```bash
# 現在のセッションで即座に反映
source ~/.zshrc  # zshの場合
source ~/.bashrc # bashの場合

# または新しいターミナルセッションを開く
```

### 設定を確認したい場合

```bash
# 詳細な設定状況を表示
pushover config show

# 環境変数を直接確認
echo $PUSHOVER_TOKEN
echo $PUSHOVER_USER
```

### 設定をリセットしたい場合

```bash
# 永続設定を削除
pushover config clear

# 新しい設定を作成
pushover config set
```

## 🎉 これで完璧！

永続設定機能により、Pushover CLIがさらに使いやすくなりました。一度設定すれば、あとは `pushover -m "メッセージ"` だけで通知を送信できます！ 