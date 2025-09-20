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