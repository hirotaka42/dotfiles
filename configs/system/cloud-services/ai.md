# Install `assam` on macOS (M1/M2/M3)

```bash
# ダウンロード & 展開
curl -L -o assam.tar.gz https://github.com/cybozu/assam/releases/download/v1.2.7/assam_1.2.7_Darwin_arm64.tar.gz
tar -xvzf assam.tar.gz

# バイナリ配置
sudo mv assam /usr/local/bin/

# 動作確認
assam --version
```


## 設定 

### 共有Bedrockを使用する際

👉[Bedrock.md](./Bedrock.md) を参考

### ログイン

ブラウザが起動されるのでEntraIDにログインする
MS Authenticator のOTPも聞かれるはず

```
assam -p sample_profile
```

### AWS CLIを使うとき

インストール

```
brew install awscli
aws --version
```

--profile オプションか、環境変数AWS_PROFILEを使って上記のsample_profileというプロファイル名を指定。

```
export AWS_PROFILE=sample_profile
aws s3 ls

# or

aws --profile sample_profile s3 ls
```

### AWS CLIを使うとき (ターミナル起動ごとに自動読み込むには)
※一度の実行でOK

```
cat <<'EOF' >> ~/.zshrc

# claude code: Bedrock
export AWS_PROFILE=sample_profile
EOF

source ~/.zshrc
```

### 