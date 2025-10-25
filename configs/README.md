# Configs - 設定ファイル管理

個人的な設定ファイルを管理するディレクトリです。

## 📁 構成

```
configs/
├── shell/      # シェル設定（zsh, bash）
├── vim/        # Vim/Neovim設定
├── git/        # Git設定
└── system/     # システム設定（クラウドサービス等）
```

## 🎯 設計方針

### 設定ファイルの配置基準

このディレクトリには、以下のような**一般的な設定ファイル**を配置します：

- ✅ シェルの設定（.zshrc, .bashrc等）
- ✅ エディタの設定（.vimrc, init.vim等）
- ✅ Git設定（.gitconfig等）
- ✅ システムレベルの設定

### ツールとの違い

- **configs/**: 環境設定、dotfiles的なもの
- **tools/**: 独自開発のツール・アプリケーション

## 📝 各カテゴリの説明

### shell/
シェル関連の設定ファイル（zsh, bash等）

詳細: [shell/README.md](shell/README.md)

### vim/
Vim/Neovimのエディタ設定

詳細: [vim/README.md](vim/README.md)

### git/
Gitの設定（.gitconfig, グローバルフック等）

詳細: [git/README.md](git/README.md)

### system/
システムレベルの設定（クラウドサービス、OS設定等）

詳細: [system/README.md](system/README.md)

## 🔧 新しい設定カテゴリの追加

新しい設定を追加する場合：

```bash
mkdir -p configs/new-config/{data,scripts,docs}
cd configs/new-config
# README.mdを作成
cat > README.md << 'EOF'
# 新しい設定

## 概要
この設定の説明

## セットアップ方法
...

## 使い方
...
EOF
```

## 📚 参考

- [ルートREADME](../README.md)
- [ツール管理](../tools/README.md)