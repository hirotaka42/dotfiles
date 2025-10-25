# システム設定

システムレベルの設定やクラウドサービスの設定を管理します。

## 📁 構成

```
system-configs/
├── cloud-services/      # クラウドサービス設定
│   ├── Bedrock.md      # AWS Bedrock設定
│   └── ai.md           # AIツール設定
└── README.md           # このファイル
```

## 📚 現在の設定

### クラウドサービス

#### AWS Bedrock
- Claude Code と AWS Bedrock の連携設定
- API設定とプロファイル管理
- 詳細: [cloud-services/Bedrock.md](cloud-services/Bedrock.md)

#### AIツール
- AWS CLI のインストール・設定
- assam CLI ツールの設定
- 詳細: [cloud-services/ai.md](cloud-services/ai.md)

## 🔧 追加予定の設定

将来的に以下のような設定を追加する可能性があります：

- macOS システム設定
- Windows レジストリ設定
- SSH設定
- その他のクラウドサービス設定（GCP、Azure等）

## 📝 使い方

各設定の詳細は、該当するマークダウンファイルを参照してください。

---

新しいシステム設定の追加リクエストがあれば Issue を作成してください。