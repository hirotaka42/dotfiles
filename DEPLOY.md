# GitHub Pages デプロイガイド

このドキュメントでは、dotfilesのWebツールをGitHub Pagesで公開する手順を説明します。

## 📋 前提条件

- GitHubアカウント
- このリポジトリへのpush権限
- リポジトリがpublic（またはGitHub Pro）

## 🚀 初回セットアップ

### 1. GitHub Pages を有効化

1. GitHubリポジトリページを開く
2. **Settings** タブをクリック
3. 左側のメニューから **Pages** を選択
4. **Source** セクションで以下を選択：
   - **Source**: GitHub Actions
5. 設定は自動保存されます

### 2. ワークフローの確認

`.github/workflows/deploy-pages.yml` が正しく配置されていることを確認：

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:
...
```

### 3. 初回デプロイ

```bash
# 変更をコミット
git add .
git commit -m "feat: GitHub Pagesを有効化"

# mainブランチにpush
git push origin main
```

### 4. デプロイ状況の確認

1. リポジトリの **Actions** タブを開く
2. "Deploy to GitHub Pages" ワークフローを確認
3. 緑色のチェックマーク ✅ が表示されれば成功
4. 2〜3分でデプロイ完了

### 5. 公開URLにアクセス

```
https://hirotaka42.github.io/dotfiles/
```

## 🔄 更新デプロイ

通常の開発フローで、mainブランチにpushするだけで自動デプロイされます。

```bash
# 変更を加える
edit index.html

# コミット & push
git add .
git commit -m "update: トップページのデザインを改善"
git push origin main
```

→ 自動的にGitHub Actionsが実行され、2〜3分で反映されます。

## 📁 公開されるファイル

以下のファイルがGitHub Pagesで公開されます：

```
dotfiles/ (ルート)
├── index.html                          # トップページ
├── tools/
│   └── ime-dictionaries/
│       └── tools/
│           └── web-editor/
│               ├── index.html         # IME辞書管理ツール
│               └── app.js
└── tests/
    └── test_web.html                  # Webテスト
```

## 🔗 公開URL

| ページ | URL |
|--------|-----|
| トップページ | https://hirotaka42.github.io/dotfiles/ |
| IME辞書管理 | https://hirotaka42.github.io/dotfiles/tools/ime-dictionaries/tools/web-editor/index.html |
| Webテスト | https://hirotaka42.github.io/dotfiles/tests/test_web.html |

## ⚙️ カスタムドメイン設定（オプション）

独自ドメインを使用する場合：

### 1. DNSレコードを設定

```
# Aレコード
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153

# CNAMEレコード
your-domain.com → hirotaka42.github.io
```

### 2. GitHub Pages設定

1. Settings > Pages > Custom domain
2. ドメイン名を入力（例: tools.your-domain.com）
3. "Save" をクリック
4. "Enforce HTTPS" を有効化

### 3. CNAMEファイルを追加

```bash
# リポジトリルートにCNAMEファイルを作成
echo "tools.your-domain.com" > CNAME
git add CNAME
git commit -m "add: カスタムドメイン設定"
git push origin main
```

## 🐛 トラブルシューティング

### デプロイが失敗する

**症状**: Actions タブで赤い ❌ が表示される

**対処法**:
1. ワークフローログを確認
2. エラーメッセージを読む
3. 権限設定を確認:
   - Settings > Actions > General
   - "Workflow permissions" を "Read and write permissions" に設定

### 404 Not Found

**症状**: ページにアクセスすると404エラー

**対処法**:
1. Settings > Pages で Source が "GitHub Actions" になっているか確認
2. デプロイが完了しているか確認（Actions タブ）
3. 5〜10分待ってからリロード（キャッシュが原因の場合）

### 変更が反映されない

**症状**: pushしても古いページが表示される

**対処法**:
1. ブラウザのキャッシュをクリア（Ctrl+Shift+R / Cmd+Shift+R）
2. Actions タブでデプロイが完了しているか確認
3. シークレットモードで確認

### パーミッションエラー

**症状**: "Resource not accessible by integration"

**対処法**:
1. Settings > Actions > General
2. "Workflow permissions" セクション
3. "Read and write permissions" を選択
4. "Allow GitHub Actions to create and approve pull requests" にチェック
5. Save

## 📊 デプロイステータスバッジ

READMEにステータスバッジを追加：

```markdown
![Deploy Status](https://github.com/hirotaka42/dotfiles/actions/workflows/deploy-pages.yml/badge.svg)
```

結果:
![Deploy Status](https://github.com/hirotaka42/dotfiles/actions/workflows/deploy-pages.yml/badge.svg)

## 🔐 セキュリティ

### 公開される情報

- すべてのファイルがpublicに公開されます
- 個人情報や機密情報を含むファイルは `.gitignore` で除外してください

### 除外されるファイル

`.gitignore` に以下が設定されています：

```
# 個人情報
data/personal/
*.secret
*.key

# テスト生成ファイル
tests/htmlcov/
tests/.coverage
```

## 📚 参考資料

- [GitHub Pages Documentation](https://docs.github.com/ja/pages)
- [GitHub Actions Documentation](https://docs.github.com/ja/actions)
- [Custom Domain Setup](https://docs.github.com/ja/pages/configuring-a-custom-domain-for-your-github-pages-site)

## 💡 ベストプラクティス

1. **定期的なテスト**: デプロイ前にローカルでテスト
2. **段階的なロールアウト**: 大きな変更は段階的に
3. **バージョニング**: 重要な変更にはタグを付ける
4. **ドキュメント**: 変更内容をコミットメッセージに記載
5. **モニタリング**: Actions タブで定期的にチェック

---

**最終更新**: 2025-10-26
