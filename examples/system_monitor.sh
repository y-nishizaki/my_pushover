#!/bin/bash

# システム監視スクリプト - Pushover通知付き
# このスクリプトは定期的に実行してシステムの状態を監視し、
# 問題が発生した場合にPushover経由で通知を送信します

# 設定
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PUSHOVER_CLI="$SCRIPT_DIR/../pushover_cli.py"

# Pushover CLI が存在するかチェック
if [ ! -f "$PUSHOVER_CLI" ]; then
    echo "エラー: pushover_cli.py が見つかりません: $PUSHOVER_CLI"
    exit 1
fi

# 関数: 通知送信
send_notification() {
    local message="$1"
    local title="$2"
    local priority="${3:-0}"
    
    python "$PUSHOVER_CLI" -m "$message" --title "$title" --priority "$priority"
}

# 1. ディスク使用量チェック
echo "ディスク使用量をチェック中..."
disk_usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$disk_usage" -gt 90 ]; then
    send_notification "ディスク使用量が${disk_usage}%に達しました" "ディスク容量警告" 1
elif [ "$disk_usage" -gt 95 ]; then
    send_notification "ディスク使用量が${disk_usage}%に達しました！緊急対応が必要です" "ディスク容量緊急" 2
fi

# 2. メモリ使用量チェック
echo "メモリ使用量をチェック中..."
mem_usage=$(free | grep '^Mem:' | awk '{printf "%.0f", ($3/$2)*100}')
if [ "$mem_usage" -gt 90 ]; then
    send_notification "メモリ使用量が${mem_usage}%に達しました" "メモリ使用量警告" 1
fi

# 3. CPU使用率チェック（1分間の平均負荷）
echo "CPU負荷をチェック中..."
cpu_cores=$(nproc)
load_avg=$(uptime | awk '{print $10}' | sed 's/,//')
load_percentage=$(echo "$load_avg * 100 / $cpu_cores" | bc -l | cut -d. -f1)

if [ "$load_percentage" -gt 80 ]; then
    send_notification "CPU負荷が${load_percentage}%に達しました（平均負荷: $load_avg）" "CPU負荷警告" 1
fi

# 4. 重要なサービス状態チェック
echo "サービス状態をチェック中..."
services=("ssh" "nginx" "mysql" "postgresql")

for service in "${services[@]}"; do
    if systemctl is-enabled "$service" >/dev/null 2>&1; then
        if ! systemctl is-active --quiet "$service"; then
            send_notification "${service}サービスが停止しています" "サービス障害" 2
        fi
    fi
done

# 5. ネットワーク接続チェック
echo "ネットワーク接続をチェック中..."
if ! ping -c 1 8.8.8.8 >/dev/null 2>&1; then
    send_notification "外部ネットワークへの接続に失敗しました" "ネットワーク障害" 2
fi

# 6. ログファイルのエラーチェック（過去1時間）
echo "ログエラーをチェック中..."
error_count=$(journalctl --since "1 hour ago" --priority=err --no-pager --quiet | wc -l)
if [ "$error_count" -gt 10 ]; then
    send_notification "過去1時間で${error_count}件のエラーが記録されました" "システムエラー" 1
fi

echo "システム監視完了" 