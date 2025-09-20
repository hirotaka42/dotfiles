## 共有Bedrockとは
Amazon Bedrockは、AWSが提供する生成AI基盤サービスで、Claude、Llama、Titanなどの大規模言語モデル（LLM）をAPI経由で利用できます。

### 使い方
前提条件
検証用AWS環境#CLIを使う場合 を参照して、設定したプロファイル名 で AWS CLIを利用可能な状態にしてください。

#### Claude Code で Bedrock を使う
Claude Code は Anthropic が提供する CLI 型の AI Agent です。 まず、以下のコマンドを実行しインストールしてください。

```
npm install -g @anthropic-ai/claude-code
```
Note: インストールするためには Node.js が必要です。

インストールが完了すると claude コマンドが利用可能になります。
Bedrock を使って Claude Code を開始するには、以下の環境変数を設定します。

```
export AWS_PROFILE=※事前設定したプロフィール名
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1
export ANTHROPIC_MODEL='us.anthropic.claude-sonnet-4-20250514-v1:0'
## 現在OPUS4は非常に繋がりにくくなっています
# export ANTHROPIC_MODEL='us.anthropic.claude-opus-4-20250514-v1:0'
```

おすすめ: 設定ファイルでの簡単設定 (~/.claude/settings.json)#
環境変数を毎回設定する代わりに、以下の設定を ~/.claude/settings.json に保存しておくと便利です。

{
  "model": "us.anthropic.claude-sonnet-4-20250514-v1:0",
  "env": {
    "CLAUDE_CODE_USE_BEDROCK": "1",
    "AWS_PROFILE": "※事前設定したプロフィール名",
    "AWS_REGION": "us-east-1"
  }
}
claude を起動し、 /model から使いたいLLMモデルを選択できます。

Claude Code Model Selection

これで準備完了です 🎉
