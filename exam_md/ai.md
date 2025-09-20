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
~/.aws/config に以下の内容を設定してください

```
[profile sample_profile]
app_id_uri                     = https://signin.aws.amazon.com/saml
azure_tenant_id                = ※YOUR_UUID_HERE
default_session_duration_hours = 6
chrome_user_data_dir           = $HOME/.config/assam/chrome-user-data
region = ※YOUR_REGION_HERE
```
※profile名は何でもいいです

### ワンライナーで実施するには？

```
mkdir -p ~/.aws && cat <<'EOF' >> ~/.aws/config
[profile sample_profile]
app_id_uri                     = https://signin.aws.amazon.com/saml
azure_tenant_id                = ※YOUR_UUID_HEREを入力
default_session_duration_hours = 6
chrome_user_data_dir           = $HOME/.config/assam/chrome-user-data
region                         = ※YOUR_REGION_HEREを入力
EOF
```

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
echo "export AWS_PROFILE=sample_profile" >> ~/.zshrc
source ~/.zshrc
```