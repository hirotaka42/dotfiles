# IME辞書管理ツール - テスト

このディレクトリにはIME辞書管理ツールのテストが含まれています。

## 📁 ファイル構成

```
tests/
├── README.md           # このファイル
├── test_data.json      # テスト用辞書データ
├── test_converter.py   # Python版のユニットテスト
└── test_web.html       # Web版のテスト（ブラウザで実行）
```

## 🧪 Python版テストの実行

### 必要要件
- Python 3.7以降
- 標準ライブラリのみ（追加インストール不要）

### 実行方法

```bash
# testsディレクトリに移動
cd tests

# テストを実行
python3 test_converter.py

# または、プロジェクトルートから
python3 -m tests.test_converter
```

### テスト内容

Python版では以下のテストを実施します：

#### 基本機能
- ✅ JSONファイルの読み込み
- ✅ 全単語の取得
- ✅ カテゴリフィルタ付き単語取得
- ✅ 統計情報の表示

#### 出力形式
- ✅ CSV出力（UTF-8-SIG、BOM付き）
- ✅ TXT出力（UTF-8、タブ区切り）
- ✅ Windows IME形式（UTF-16LE、BOM付き）
- ✅ macOS plist形式（UTF-8、XML）

#### 品詞マッピング
- ✅ Windows IME用の品詞マッピング
- ✅ 「記号」→「短縮よみ」変換
- ✅ 未定義品詞のデフォルト値

#### カテゴリフィルタリング
- ✅ 単一カテゴリフィルタ
- ✅ 複数カテゴリフィルタ
- ✅ 無効カテゴリの除外

#### エッジケース
- ✅ 空のカテゴリ処理
- ✅ XML特殊文字のエスケープ

### テスト結果の見方

```
test_csv_output (CSV出力のテスト) ... ok
test_windows_output (Windows形式出力のテスト) ... ok
...

----------------------------------------------------------------------
Ran 13 tests in 0.049s

OK
```

- `ok`: テスト成功
- `ERROR`: テスト実行エラー
- `FAIL`: アサーション失敗

## 🌐 Web版テストの実行

### 実行方法

1. ブラウザで `test_web.html` を開く
2. 「全テストを実行」ボタンをクリック
3. テスト結果が表示される

### テスト内容

Web版では以下のテストを実施します：

#### エスケープ処理
- ✅ CSVフィールドのエスケープ（通常文字列）
- ✅ CSVフィールドのエスケープ（ダブルクォート）
- ✅ CSVフィールドのエスケープ（null値）
- ✅ XML特殊文字のエスケープ

#### 品詞マッピング
- ✅ Windows品詞マッピング - 記号
- ✅ Windows品詞マッピング - 名詞
- ✅ Windows品詞マッピング - 人名
- ✅ Windows品詞マッピング - 動詞
- ✅ Windows品詞マッピング - 未定義品詞

#### データ処理
- ✅ テストデータのカテゴリ数
- ✅ カテゴリ別の単語数
- ✅ CSVヘッダー生成
- ✅ 品詞の一貫性

#### エンコーディング
- ✅ UTF-16LE BOMの確認
- ✅ UTF-16LE文字エンコード

#### カテゴリフィルタリング
- ✅ 単一カテゴリフィルタ
- ✅ 複数カテゴリフィルタ

### テスト結果の見方

- ✅ 緑色 = テスト成功
- ❌ 赤色 = テスト失敗（エラー詳細が表示されます）

## 📊 テストカバレッジ

### カバレッジ率

| 対象 | カバレッジ |
|------|----------|
| convert.py | **67%** ✅ |
| test_converter.py | **98%** |
| **合計** | **81%** |

詳細は [COVERAGE.md](COVERAGE.md) を参照してください。

### Python版
| カテゴリ | テスト数 |
|---------|---------|
| 基本機能 | 5 |
| 出力形式 | 5 |
| 品詞マッピング | 1 |
| カテゴリフィルタ | 3 |
| エッジケース | 3 |
| **合計** | **17** |

### Web版
| カテゴリ | テスト数 |
|---------|---------|
| エスケープ処理 | 4 |
| 品詞マッピング | 5 |
| データ処理 | 4 |
| エンコーディング | 2 |
| カテゴリフィルタ | 2 |
| **合計** | **17** |

## 🔧 テストデータ

`test_data.json` には以下のテストデータが含まれています：

- **記号カテゴリ**: 2件の単語（→, ○）
- **人名カテゴリ**: 1件の単語（田中）
- **無効カテゴリ**: 1件の単語（無効化されているため出力されない）

## 🐛 テストが失敗する場合

### Python版

1. **Pythonのバージョンを確認**
   ```bash
   python3 --version  # 3.7以降が必要
   ```

2. **パスの問題**
   - `tests/` ディレクトリから実行していることを確認
   - または、プロジェクトルートから相対パスで実行

3. **権限の問題**
   ```bash
   chmod +x test_converter.py
   ```

### Web版

1. **ブラウザのコンソールを確認**
   - F12を押して開発者ツールを開く
   - Consoleタブでエラーメッセージを確認

2. **ローカルファイルの制限**
   - ブラウザによってはローカルファイルの実行に制限がある場合があります
   - その場合は簡易HTTPサーバーで実行：
     ```bash
     cd tests
     python3 -m http.server 8000
     # ブラウザで http://localhost:8000/test_web.html を開く
     ```

## 📝 新しいテストの追加

### Python版

`test_converter.py` に新しいテストメソッドを追加：

```python
def test_new_feature(self):
    """新機能のテスト"""
    # テストコードを記述
    self.assertEqual(actual, expected)
```

### Web版

`test_web.html` の `defineTests()` 関数に追加：

```javascript
runner.test('新機能のテスト', () => {
    const result = newFunction();
    assertEqual(result, expected);
});
```

## 🚀 CI/CDでの実行

### GitHub Actions例

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Run Python tests
        run: |
          cd tools/ime-dictionaries/tests
          python3 test_converter.py
```

## 📚 参考資料

- [Python unittest ドキュメント](https://docs.python.org/ja/3/library/unittest.html)
- [XML.etree.ElementTree](https://docs.python.org/ja/3/library/xml.etree.elementtree.html)
- [CSV ファイルフォーマット](https://tools.ietf.org/html/rfc4180)
- [UTF-16エンコーディング](https://www.unicode.org/faq/utf_bom.html)

## 🤝 貢献

テストの追加や改善のプルリクエストを歓迎します！
