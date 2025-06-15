"""
Pushover CLI 設定管理モジュール
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Tuple


class ConfigManager:
    """設定管理クラス"""
    
    def __init__(self):
        self.home = Path.home()
        self.shell_configs = {
            'bash': ['.bashrc', '.bash_profile'],
            'zsh': ['.zshrc', '.zprofile'],
            'fish': ['.config/fish/config.fish'],
        }
    
    def detect_shell(self) -> str:
        """現在使用しているシェルを検出"""
        shell = os.environ.get('SHELL', '/bin/bash')
        shell_name = Path(shell).name
        
        # よく使われるシェルをサポート
        if shell_name in ['bash', 'zsh', 'fish']:
            return shell_name
        else:
            # デフォルトはbash
            return 'bash'
    
    def get_shell_config_file(self, shell: Optional[str] = None) -> Path:
        """シェル設定ファイルのパスを取得"""
        if not shell:
            shell = self.detect_shell()
        
        config_files = self.shell_configs.get(shell, self.shell_configs['bash'])
        
        # 既存のファイルがあるかチェック
        for config_file in config_files:
            config_path = self.home / config_file
            if config_path.exists():
                return config_path
        
        # 既存ファイルがない場合は最初のファイルを使用
        return self.home / config_files[0]
    
    def get_current_config(self) -> Dict[str, Optional[str]]:
        """現在の設定を取得"""
        return {
            'PUSHOVER_TOKEN': os.environ.get('PUSHOVER_TOKEN'),
            'PUSHOVER_USER': os.environ.get('PUSHOVER_USER'),
        }
    
    def set_environment_variables(self, token: str, user: str, shell: Optional[str] = None) -> Tuple[bool, str]:
        """環境変数をシェル設定ファイルに永続的に設定"""
        try:
            config_file = self.get_shell_config_file(shell)
            shell_name = shell or self.detect_shell()
            
            # 既存の設定を読み込み
            content = ""
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            # Pushover設定のマーカー
            start_marker = "# === Pushover CLI Configuration - Start ==="
            end_marker = "# === Pushover CLI Configuration - End ==="
            
            # 既存の設定を削除
            if start_marker in content and end_marker in content:
                start_idx = content.find(start_marker)
                end_idx = content.find(end_marker) + len(end_marker)
                content = content[:start_idx] + content[end_idx + 1:]
                content = content.rstrip() + '\n'
            
            # 新しい設定を追加
            if shell_name == 'fish':
                new_config = f"""
{start_marker}
set -gx PUSHOVER_TOKEN "{token}"
set -gx PUSHOVER_USER "{user}"
{end_marker}
"""
            else:
                new_config = f"""
{start_marker}
export PUSHOVER_TOKEN="{token}"
export PUSHOVER_USER="{user}"
{end_marker}
"""
            
            # ファイルに書き込み
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(content + new_config)
            
            return True, f"設定が {config_file} に保存されました"
            
        except Exception as e:
            return False, f"設定の保存に失敗しました: {str(e)}"
    
    def remove_environment_variables(self, shell: Optional[str] = None) -> Tuple[bool, str]:
        """環境変数をシェル設定ファイルから削除"""
        try:
            config_file = self.get_shell_config_file(shell)
            
            if not config_file.exists():
                return True, "設定ファイルが存在しません"
            
            # 既存の設定を読み込み
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Pushover設定のマーカー
            start_marker = "# === Pushover CLI Configuration - Start ==="
            end_marker = "# === Pushover CLI Configuration - End ==="
            
            # 既存の設定を削除
            if start_marker in content and end_marker in content:
                start_idx = content.find(start_marker)
                end_idx = content.find(end_marker) + len(end_marker)
                new_content = content[:start_idx] + content[end_idx + 1:]
                new_content = new_content.rstrip() + '\n' if new_content.strip() else ''
                
                # ファイルに書き込み
                with open(config_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                return True, f"設定が {config_file} から削除されました"
            else:
                return True, "Pushover設定が見つかりませんでした"
                
        except Exception as e:
            return False, f"設定の削除に失敗しました: {str(e)}"
    
    def show_setup_instructions(self, shell: Optional[str] = None) -> str:
        """セットアップ手順を表示"""
        shell_name = shell or self.detect_shell()
        config_file = self.get_shell_config_file(shell_name)
        
        instructions = f"""
🔧 Pushover CLI 永続設定手順

現在のシェル: {shell_name}
設定ファイル: {config_file}

設定後は新しいターミナルセッションで自動的に環境変数が読み込まれます。
現在のセッションで即座に適用するには以下を実行してください:

"""
        
        if shell_name == 'fish':
            instructions += f"source {config_file}"
        else:
            instructions += f"source {config_file}"
        
        return instructions