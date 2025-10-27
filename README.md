# Dotfiles - 個人設定管理リポジトリ

複数端末間で個人設定を簡単に同期・管理するためのdotfilesリポジトリです。

## 🌐 Webツール

ブラウザから直接使えるWebツールを公開しています！

**🔗 [Webツールを使う](https://hirotaka42.github.io/dotfiles/)**

- 📚 [IME辞書管理ツール](https://hirotaka42.github.io/dotfiles/tools/ime-dictionaries/tools/web-editor/index.html) - JSON辞書の編集・エクスポート

> **Note**: GitHub Pagesで公開されています。インストール不要でブラウザから直接利用できます。

## 🎯 コンセプト

- **カテゴリ別管理**: 設定とツールを明確に分離
- **シンプル設計**: 個人利用に最適化、過度な複雑さを排除
- **拡張性**: 新しい設定やツールを簡単に追加可能
- **ドキュメント重視**: 各設定の使い方を明確に記載

## 📁 リポジトリ構造

```
dotfiles/
├── configs/               # 一般的な設定ファイル
│   ├── shell/            # シェル設定（zsh, bash）
│   ├── vim/              # Vim/Neovim設定
│   ├── git/              # Git設定
│   └── system/           # システム設定（クラウド等）
│
└── tools/                # 特定のツール・アプリケーション
    └── ime-dictionaries/ # IME辞書管理ツール ⭐
```

## 🚀 主な機能

### 1. IME辞書管理ツール ⭐

個人用IME辞書を効率的に管理するための統合システムです。

**特徴:**
- 📝 **Web編集ツール**: ブラウザで直感的に辞書を編集
- 🔄 **マルチプラットフォーム変換**: macOS・Windows・CSV形式に対応
- 📊 **JSON管理**: 人間にも機械にも扱いやすい形式
- 🏷️ **カテゴリ・タグ管理**: 辞書項目を整理して管理

**クイックスタート:**
```bash
cd tools/ime-dictionaries/tools/web-editor
python3 -m http.server 8000
# ブラウザで http://localhost:8000 を開く
```

詳細は [tools/ime-dictionaries/README.md](tools/ime-dictionaries/README.md) を参照してください。

### 2. システム設定

クラウドサービスやシステムレベルの設定を管理します。

- **AWS Bedrock設定**: `configs/system/cloud-services/Bedrock.md`
- **AIツール設定**: `configs/system/cloud-services/ai.md`

### 3. その他の設定（今後追加予定）

- **シェル設定**: `configs/shell/` - zsh, bash設定
- **Vim設定**: `configs/vim/` - Vim/Neovim設定
- **Git設定**: `configs/git/` - Git設定

## 📝 使い方

### IME辞書の編集

1. **Web編集ツールで編集**（推奨）
   ```bash
   cd tools/ime-dictionaries/tools/web-editor
   python3 -m http.server 8000
   ```
   - ブラウザで http://localhost:8000 を開く
   - `tools/ime-dictionaries/data/dictionary.json` を読み込み
   - 単語の追加・編集・削除
   - 編集後、JSONファイルを保存

2. **プラットフォーム用に変換**
   ```bash
   cd tools/ime-dictionaries/tools/converter

   # macOS用に変換
   python3 convert.py ../../data/dictionary.json --macos output_macos.txt

   # Windows用に変換
   python3 convert.py ../../data/dictionary.json --windows output_windows.txt

   # CSV形式で出力
   python3 convert.py ../../data/dictionary.json --csv output.csv

   # 全形式一括変換
   python3 convert.py ../../data/dictionary.json --all-formats --output-dir ./output
   ```

3. **各プラットフォームにインポート**
   - macOS: [手順書](tools/ime-dictionaries/docs/macos-manual-setup.md)
   - Windows: [手順書](tools/ime-dictionaries/docs/windows-manual-setup.md)

### 辞書データの例

サンプルデータには以下のカテゴリが含まれています：

- **記号・マーク**: ★、●、○、◎など
- **矢印**: →、←、↑、↓
- **チェックマーク**: ✅、✔️、❌
- **メールアドレス**: よく使うメールアドレスのショートカット
- **定型文**: よく使うフレーズや文章

## 🔧 新しい設定・ツールの追加方法

このリポジトリは拡張可能な設計になっています。

### 設定を追加する場合

```bash
mkdir -p configs/new-config/{data,scripts,docs}
```

### ツールを追加する場合

```bash
mkdir -p tools/new-tool/{src,data,docs}
```

各ディレクトリにREADME.mdを作成して、使い方を記載してください。

## 🔐 プライバシー・セキュリティ

### .gitignoreの設定

個人情報を含むファイルはGit管理から除外します：

```gitignore
# 個人辞書（オプション）
tools/ime-dictionaries/data/personal/

# システム固有ファイル
.DS_Store
Thumbs.db

# 一時ファイル
*.tmp
*.swp
```

### 機密情報の管理

- メールアドレスや個人情報は例として `example@example.com` などを使用
- 実際の情報を記載する場合は、ローカルのみで管理
- 必要に応じて暗号化や環境変数を使用

## 📊 統計情報

辞書の統計情報を確認：

```bash
cd tools/ime-dictionaries/tools/converter
python3 convert.py ../../data/dictionary.json --stats
```

出力例：
```
📊 辞書統計情報
  辞書名: 個人用IME辞書
  更新日: 2024-10-25
  カテゴリ数: 5
  総単語数: 26
  有効単語数: 26

  ✅ 記号・マーク: 7件 - よく使う記号や矢印、チェックマーク
  ✅ 矢印: 4件 - 方向を示す矢印記号
  ✅ チェックマーク: 5件 - 完了や確認を示すマーク
  ✅ メールアドレス: 5件 - よく使うメールアドレスのショートカット
  ✅ 定型文: 5件 - よく使う定型文やフレーズ
```

## 🛠️ トラブルシューティング

### Web編集ツールが開けない

**原因**: ローカルサーバーが起動していない

**解決方法**:
```bash
cd tools/ime-dictionaries/tools/web-editor
python3 -m http.server 8000
```

### 変換スクリプトでエラー

**原因**: Python 3.6以降が必要

**解決方法**:
```bash
python3 --version  # バージョン確認
# 必要に応じてPythonをアップデート
```

### 日本語が文字化けする

**原因**: ファイルのエンコーディング問題

**解決方法**:
- ファイルがUTF-8で保存されているか確認
- テキストエディタのエンコーディング設定を確認

## 🎯 今後の追加予定

### configs/ - 設定ファイル
- [ ] シェル設定（zsh, bash）の充実
- [ ] Vim/Neovim設定の追加
- [ ] Git設定（.gitconfig, グローバルフック）の追加
- [ ] VSCode設定の追加

### tools/ - ツール・アプリケーション
- [ ] スニペット管理ツール
- [ ] パスワード管理補助ツール
- [ ] 開発環境セットアップツール

## 🤝 貢献

改善提案やバグ報告は Issues でお知らせください。

## 📚 参考リンク

### IME辞書管理
- [IME辞書管理の詳細](tools/ime-dictionaries/README.md)
- [macOS設定手順](tools/ime-dictionaries/docs/macos-manual-setup.md)
- [Windows設定手順](tools/ime-dictionaries/docs/windows-manual-setup.md)
- [JSON変換スクリプト](tools/ime-dictionaries/tools/converter/convert.py)

### 設定ファイル
- [シェル設定](configs/shell/README.md)
- [Vim設定](configs/vim/README.md)
- [Git設定](configs/git/README.md)
- [システム設定](configs/system/README.md)

## 📄 ライセンス

MIT License

---

**作成日**: 2024-10-25
**最終更新**: 2024-10-25
**対応プラットフォーム**: macOS, Windows