# シェル設定

シェル（bash, zsh等）の設定を管理します。

## 📌 ステータス

**🚧 今後追加予定**

このディレクトリは将来の拡張用に予約されています。

## 📝 追加予定の機能

- `.zshrc` / `.bashrc` の管理
- シェルエイリアスの設定
- 環境変数の管理
- プロンプトカスタマイズ
- シェル関数・スクリプト

## 💡 実装予定の構造

```
shell-config/
├── zsh/
│   ├── .zshrc
│   ├── aliases.zsh
│   └── functions.zsh
├── bash/
│   ├── .bashrc
│   └── aliases.bash
├── scripts/
│   └── setup.sh
└── README.md
```

## 🔗 参考

実装時には以下を参考にします：

- [dotfiles examples](https://dotfiles.github.io/)
- [zsh configuration guide](https://zsh.sourceforge.io/Guide/)

---

実装リクエストがあれば Issue を作成してください。