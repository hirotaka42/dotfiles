# Tools - ツール・アプリケーション管理

独自開発のツールやアプリケーションを管理するディレクトリです。

## 📁 構成

```
tools/
└── ime-dictionaries/    # IME辞書管理ツール ⭐
```

## 🎯 設計方針

### ツールの配置基準

このディレクトリには、以下のような**独自開発のツール・アプリケーション**を配置します：

- ✅ 独自のWebアプリケーション
- ✅ 専用の管理ツール
- ✅ データ処理・変換ツール
- ✅ 自動化スクリプト群

### 設定ファイルとの違い

- **configs/**: 環境設定、dotfiles的なもの
- **tools/**: 独自開発のツール・アプリケーション

## 📝 現在のツール

### ime-dictionaries/ ⭐

IME辞書を効率的に管理するための統合ツールです。

**主な機能:**
- Web編集ツール（HTML + JavaScript）
- JSON ↔ 各プラットフォーム形式変換（Python）
- カテゴリ・タグ管理
- 統計情報表示

**使い方:**
```bash
cd ime-dictionaries/tools/web-editor
python3 -m http.server 8000
```

詳細: [ime-dictionaries/README.md](ime-dictionaries/README.md)

## 🔧 新しいツールの追加

新しいツールを追加する場合：

```bash
mkdir -p tools/new-tool/{src,data,docs,tests}
cd tools/new-tool

# 基本的な構造
# src/       - ソースコード
# data/      - データファイル
# docs/      - ドキュメント
# tests/     - テストコード

# README.mdを作成
cat > README.md << 'EOF'
# 新しいツール

## 概要
このツールの説明

## インストール・セットアップ
...

## 使い方
...

## 開発
...
EOF
```

## 📊 推奨ツール構造

各ツールは以下のような構造を推奨します：

```
tools/your-tool/
├── README.md           # ツールの説明
├── src/               # ソースコード
│   ├── main.py (or index.html)
│   └── ...
├── data/              # データファイル
├── docs/              # 詳細ドキュメント
├── tests/             # テストコード
└── requirements.txt   # 依存関係（Python等）
```

## 🎯 今後の追加候補

- [ ] スニペット管理ツール
- [ ] パスワード管理補助ツール
- [ ] 開発環境セットアップツール
- [ ] ログ解析ツール
- [ ] バックアップ自動化ツール

## 📚 参考

- [ルートREADME](../README.md)
- [設定ファイル管理](../configs/README.md)