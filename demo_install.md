# Pushover CLI パッケージ インストール & 使用デモ

## 🎯 パッケージ化完了！

PushoverのCLI通知ツールがpip installable パッケージとして完成しました！

## 📦 パッケージ構造

```
my_pushover/
├── pushover_cli/           # メインパッケージ
│   ├── __init__.py        # パッケージ初期化
│   ├── cli.py             # CLIインターフェース
│   └── core.py            # コアロジック
├── examples/              # 使用例
│   └── system_monitor.sh  # システム監視スクリプト
├── tests/                 # テストファイル
│   └── test_pushover.py   # テストスクリプト
├── setup.py               # setuptools設定
├── pyproject.toml         # モダンなパッケージ設定
├── README.md              # ドキュメント
├── LICENSE                # MITライセンス
├── MANIFEST.in            # パッケージ含有ファイル指定
└── requirements.txt       # 依存関係
```

## 🚀 インストール方法

### 1. ローカル開発版（推奨 - 現在の状態）

```bash
# プロジェクトディレクトリで
pip install -e .
```

### 2. 将来的なインストール方法

```bash
# PyPIから（将来の公開後）
pip install pushover-cli

# GitHubから直接
pip install git+https://github.com/your-username/pushover-cli.git
```

## ✨ 新機能：超簡単な使用方法

### 従来の方法
```bash
python pushover_cli.py -t token -u user -m "message"
```

### 新しい方法（pip install後）
```bash
pushover -t token -u user -m "message"
```

## 🔧 設定例

### 環境変数を設定
```bash
export PUSHOVER_TOKEN="your_app_token"
export PUSHOVER_USER="your_user_key"
```

### 簡単な通知送信
```bash
pushover -m "Hello from pip-installed package!"
```

## 📋 動作確認済み機能

✅ pip install でのパッケージインストール  
✅ `pushover` コマンドでの直接実行  
✅ ヘルプメッセージ表示 (`pushover --help`)  
✅ バージョン表示 (`pushover --version`)  
✅ エラーハンドリング（認証情報不足時）  
✅ 環境変数からの設定読み込み  
✅ 設定ファイルからの設定読み込み  

## 🎪 デモ例

```bash
# パッケージがインストールされているか確認
pushover --version
# => pushover-cli 1.0.0

# ヘルプを表示
pushover --help

# 認証情報なしでのエラーハンドリングテスト
pushover -m "test"
# => エラー: Pushoverトークンが指定されていません

# 実際の通知送信（要：Pushoverアカウント設定）
pushover -t your_token -u your_user -m "pip installパッケージのテスト！"
```

## 🚀 開発者向け情報

### パッケージの再インストール
```bash
pip uninstall pushover-cli
pip install -e .
```

### テスト実行
```bash
python tests/test_pushover.py
```

### 配布用パッケージ作成
```bash
# sdist & wheel 作成
python setup.py sdist bdist_wheel

# PyPIへのアップロード（設定後）
# twine upload dist/*
```

## 🎉 主な改善点

1. **pip install対応**: 標準的なPythonパッケージとして配布可能
2. **グローバルコマンド**: `pushover`として直接実行可能
3. **モジュール構造**: 再利用可能なコアロジック分離
4. **標準的な配布**: PyPI準拠のパッケージ構造
5. **開発環境**: エディタブルインストール対応

これで、Pushover CLIツールはプロフェッショナルなPythonパッケージとして完成しました！ 🎊 