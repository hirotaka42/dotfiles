# Git設定

Gitの設定を管理します。

## 📌 ステータス

**🚧 今後追加予定**

このディレクトリは将来の拡張用に予約されています。

## 📝 追加予定の機能

- `.gitconfig` の管理
- Git エイリアスの設定
- コミットテンプレート
- Git hooks（グローバル）
- Git ignore パターン

## 💡 実装予定の構造

```
git-config/
├── .gitconfig
├── .gitignore_global
├── templates/
│   └── commit-template.txt
├── hooks/
│   ├── pre-commit
│   └── commit-msg
├── scripts/
│   └── setup.sh
└── README.md
```

## 🔗 参考

実装時には以下を参考にします：

- [Git configuration](https://git-scm.com/docs/git-config)
- [Git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [gitignore templates](https://github.com/github/gitignore)

---

実装リクエストがあれば Issue を作成してください。