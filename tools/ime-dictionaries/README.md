# IME辞書管理システム

個人用IME辞書を効率的に管理・運用するためのツールセットです。

## 🎯 特徴

- **JSON形式での管理**: 人間にも機械にも読みやすい形式
- **Webエディタ**: ブラウザで直感的に編集
- **マルチプラットフォーム対応**: macOS・Windows・CSV等に変換
- **プラットフォーム別読み対応**: Windows/macOS用の読みを個別管理 ⭐ NEW
- **カテゴリ管理**: 用途別に辞書を分類
- **シンプル設計**: 個人利用に最適化

## 📁 構造

```
ime-dictionaries/
├── data/                    # 辞書データ
│   ├── dictionary.json     # メイン辞書データ
│   └── schema.json         # JSON スキーマ定義
├── tools/                  # 管理ツール
│   ├── web-editor/         # Web編集ツール
│   │   ├── index.html     # メインページ
│   │   └── app.js         # JavaScript
│   └── converter/          # 形式変換ツール
│       └── convert.py     # Python変換スクリプト
├── docs/                   # ドキュメント
├── scripts/               # セットアップスクリプト
└── README.md              # このファイル
```

## 🚀 クイックスタート

### 1. Web編集ツールを使う

```bash
cd ime-dictionaries/tools/web-editor
# ローカルサーバーで開く（例: Python）
python3 -m http.server 8000
# ブラウザで http://localhost:8000 を開く
```

### 2. JSONファイルを読み込む

- ブラウザで「JSONファイルを読み込み」をクリック
- `data/dictionary.json` を選択
- 編集・管理を開始

### 3. 各プラットフォーム用に変換

```bash
cd tools/converter

# カテゴリ一覧を表示
python3 convert.py ../../data/dictionary.json --list-categories

# 統計情報表示
python3 convert.py ../../data/dictionary.json --stats

# 全カテゴリをCSV形式で出力
python3 convert.py ../../data/dictionary.json --csv output.csv

# 特定カテゴリのみをCSV出力（複数カテゴリを1つのファイルに統合）
python3 convert.py ../../data/dictionary.json --csv output.csv --categories "記号・マーク,矢印"

# macOS用.plist形式で出力（複数カテゴリ対応）
python3 convert.py ../../data/dictionary.json --macos dictionary.plist --categories "記号・マーク,矢印,チェックマーク"

# Windows用に変換
python3 convert.py ../../data/dictionary.json --windows windows_dict.txt

# 全形式一括変換
python3 convert.py ../../data/dictionary.json --all-formats --output-dir ./output

# 特定カテゴリのみ全形式出力
python3 convert.py ../../data/dictionary.json --all-formats --output-dir ./output --categories "矢印"
```

## 📝 辞書データの編集

### Web編集ツールでの操作

1. **カテゴリ管理**
   - カテゴリ追加・削除
   - カテゴリ別の単語表示

2. **単語管理**
   - 読み・単語・品詞の設定
   - 説明・タグの追加
   - 検索・フィルタ機能

3. **エクスポート** ⭐ 複数カテゴリ選択対応
   - チェックボックスで複数カテゴリを選択
   - 選択したカテゴリを1つのファイルに統合出力
   - CSV、TXT、macOS、Windows形式に対応
   - 「全て選択」「全て解除」で一括操作

### JSON直接編集

```json
{
  "辞書情報": {
    "名前": "個人用IME辞書",
    "説明": "説明文",
    "更新日": "2024-10-25"
  },
  "カテゴリ": {
    "カテゴリ名": {
      "説明": "カテゴリの説明",
      "有効": true,
      "単語リスト": [
        {
          "読み": "よみ",
          "読み_Windows": "よみ（Windows用、オプション）",
          "単語": "変換後の単語",
          "品詞": "名詞",
          "説明": "説明文",
          "タグ": ["タグ1", "タグ2"]
        }
      ]
    }
  }
}
```

#### プラットフォーム別読み対応 ⭐ NEW

- **`読み`**: macOS用の読み（必須）
- **`読み_Windows`**: Windows IME用の読み（オプション）
  - 半角英語のみの読み（例: "mem", "meko"）の場合、Windows IMEでは動作しないため、ひらがなの読みを設定
  - 設定した場合、Windows出力時に `読み_Windows` が優先使用される
  - macOS出力時は常に `読み` が使用される

**例：半角英語の読みの場合**
```json
{
  "読み": "mem",
  "読み_Windows": "めも",
  "単語": "メモを確認する",
  "品詞": "名詞"
}
```

## 🔧 変換形式

### 対応出力形式

| 形式 | 用途 | 説明 | エンコーディング |
|------|------|------|------------------|
| CSV | 表計算ソフト | Excel・Google Sheetsでの編集（BOM付きUTF-8） | UTF-8-SIG |
| TXT | 汎用 | タブ区切りテキスト | UTF-8 |
| macOS (.plist) | macOS日本語入力 | 最新macOS用Property List形式 | UTF-8 |
| Windows | Microsoft IME | Windows IME用形式 | UTF-16LE |

### カテゴリ選択機能 ⭐ 新機能

複数のカテゴリを選択して、**1つのファイルに統合して出力**できます。

```bash
# カテゴリ一覧を表示
python3 convert.py dictionary.json --list-categories

# 特定の複数カテゴリを1つのCSVファイルに統合
python3 convert.py dictionary.json --csv output.csv --categories "記号・マーク,矢印,チェックマーク"

# 特定カテゴリのみmacOS用.plist形式で出力
python3 convert.py dictionary.json --macos dictionary.plist --categories "記号・マーク"

# 複数形式同時変換（同じカテゴリ選択）
python3 convert.py dictionary.json --csv out.csv --macos dictionary.plist --categories "矢印"
```

## 📊 統計・管理機能

### 統計情報表示

```bash
python3 convert.py dictionary.json --stats
```

出力例:
```
📊 辞書統計情報
  辞書名: 個人用IME辞書
  更新日: 2024-10-25
  カテゴリ数: 5
  総単語数: 156
  有効単語数: 142

  ✅ 記号・マーク: 7件 - よく使う記号や矢印、チェックマーク
  ✅ 矢印: 4件 - 方向を示す矢印記号
  ✅ チェックマーク: 5件 - 完了や確認を示すマーク
  ✅ メールアドレス: 5件 - よく使うメールアドレスのショートカット
  ✅ 定型文: 5件 - よく使う定型文やフレーズ
```

## 🔄 ワークフロー

### 推奨作業フロー

1. **編集**: Web編集ツールで単語を追加・編集
2. **保存**: JSONファイルとして保存
3. **変換**: 使用プラットフォーム用に変換
4. **インポート**: 各IMEに辞書をインポート
5. **同期**: Gitで変更履歴を管理

### バックアップ・同期

```bash
# Git管理（推奨）
git add ime-dictionaries/data/dictionary.json
git commit -m "辞書更新: 新しい技術用語を追加"

# 定期バックアップ
cp data/dictionary.json "backup/dictionary_$(date +%Y%m%d).json"
```

## 🎨 カスタマイズ

### 新しいカテゴリの追加

1. Web編集ツールで「カテゴリ追加」
2. または、JSON直接編集で追加

### 品詞の拡張

`tools/web-editor/index.html` の品詞選択肢を編集:

```html
<select id="wordPOS">
    <option value="名詞">名詞</option>
    <option value="カスタム品詞">カスタム品詞</option>
</select>
```

### 新しい出力形式の追加

`tools/converter/convert.py` にメソッドを追加:

```python
def to_custom_format(self, output_file, categories=None):
    """カスタム形式で出力"""
    words = self._get_all_words(categories)
    # カスタム形式の処理
```

## 🐛 トラブルシューティング

### よくある問題

**Q: Web編集ツールが開けない**
A: ローカルサーバーを起動してください
```bash
python3 -m http.server 8000
```

**Q: 日本語が文字化けする**
A: ファイルがUTF-8で保存されているか確認

**Q: 変換スクリプトでエラー**
A: Python 3.6以降が必要です
```bash
python3 --version
```

### ログ・デバッグ

変換スクリプトの詳細出力:
```bash
python3 convert.py dictionary.json --stats --verbose
```

## 🧪 テスト

品質を保証するため、Python版とWeb版の両方にユニットテストが用意されています。

### Python版テストの実行

```bash
cd tests
python3 test_converter.py
```

**結果例**:
```
Ran 13 tests in 0.049s

OK
```

### Web版テストの実行

ブラウザで `tests/test_web.html` を開いて「全テストを実行」ボタンをクリック

### テストカバレッジ

- **Python版**: 13個のテスト（出力形式、品詞マッピング、エンコーディング等）
- **Web版**: 17個のテスト（エスケープ処理、UTF-16LE変換、カテゴリフィルタ等）

詳細は [tests/README.md](tests/README.md) を参照してください。

## 📚 参考資料

- [macOS日本語入力設定方法](docs/macos-manual-setup.md)
- [Windows IME設定方法](docs/windows-manual-setup.md)
- [JSON Schema仕様](data/schema.json)
- [テスト実行ガイド](tests/README.md)

## 🤝 貢献

改善提案やバグ報告は Issues でお知らせください。
プルリクエストを送る前にテストを実行してください。

## 📄 ライセンス

MIT License