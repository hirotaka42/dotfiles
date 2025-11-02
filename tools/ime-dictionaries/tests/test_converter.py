#!/usr/bin/env python3
"""
IME辞書変換ツールのユニットテスト
"""

import unittest
import sys
import os
import tempfile
from pathlib import Path
import csv
import xml.etree.ElementTree as ET

# テスト対象のモジュールをインポート
sys.path.insert(0, str(Path(__file__).parent.parent / 'tools' / 'converter'))
from convert import DictionaryConverter


class TestDictionaryConverter(unittest.TestCase):
    """DictionaryConverterクラスのテスト"""

    @classmethod
    def setUpClass(cls):
        """テストクラス全体の初期化"""
        cls.test_data_path = Path(__file__).parent / 'test_data.json'
        cls.converter = DictionaryConverter(cls.test_data_path)

    def setUp(self):
        """各テストの初期化"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """各テストの後処理"""
        # 一時ファイルを削除
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_load_json(self):
        """JSONファイルの読み込みテスト"""
        self.assertIsNotNone(self.converter.data)
        self.assertIn('辞書情報', self.converter.data)
        self.assertIn('カテゴリ', self.converter.data)

    def test_get_all_words(self):
        """全単語取得のテスト"""
        words = self.converter._get_all_words()
        # 有効なカテゴリのみ取得（記号2件 + 人名1件 + 定型文2件 = 5件）
        self.assertEqual(len(words), 5)
        # 無効なカテゴリは含まれない
        self.assertNotIn('無効', [w.get('単語') for w in words])

    def test_get_words_with_category_filter(self):
        """カテゴリフィルタ付き単語取得のテスト"""
        words = self.converter._get_all_words(categories=['記号'])
        self.assertEqual(len(words), 2)
        # 全てのカテゴリが'記号'
        for word in words:
            self.assertEqual(word.get('カテゴリ'), '記号')

    def test_csv_output(self):
        """CSV出力のテスト"""
        output_file = Path(self.temp_dir) / 'test.csv'
        self.converter.to_csv(output_file)

        # ファイルが作成されているか
        self.assertTrue(output_file.exists())

        # UTF-8-SIG (BOM付き) で読み込めるか
        with open(output_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # ヘッダー行を含めて6行（ヘッダー + データ5件）
        self.assertEqual(len(rows), 6)

        # ヘッダーの確認（読み_Windows列が追加されている）
        self.assertEqual(rows[0], ['読み', '読み_Windows', '単語', '品詞', '説明', 'タグ', 'カテゴリ'])

        # データ行の確認
        self.assertIn('みぎや', [row[0] for row in rows[1:]])

    def test_windows_pos_mapping(self):
        """Windows IME品詞マッピングのテスト"""
        # 記号 -> 短縮よみ
        self.assertEqual(self.converter._map_pos_for_windows('記号'), '短縮よみ')

        # 名詞 -> 名詞
        self.assertEqual(self.converter._map_pos_for_windows('名詞'), '名詞')

        # 人名 -> 人名
        self.assertEqual(self.converter._map_pos_for_windows('人名'), '人名')

        # 動詞 -> 名詞
        self.assertEqual(self.converter._map_pos_for_windows('動詞'), '名詞')

        # 未定義 -> 名詞（デフォルト）
        self.assertEqual(self.converter._map_pos_for_windows('未定義品詞'), '名詞')

    def test_windows_output(self):
        """Windows形式出力のテスト"""
        output_file = Path(self.temp_dir) / 'test_windows.txt'
        self.converter.to_windows(output_file)

        # ファイルが作成されているか
        self.assertTrue(output_file.exists())

        # UTF-16で読み込めるか
        with open(output_file, 'r', encoding='utf-16') as f:
            content = f.read()

        # ヘッダーの確認
        self.assertIn('!Microsoft IME Dictionary Tool', content)
        self.assertIn('!CharSet=UTF-16LE', content)

        # BOMの確認（バイトレベル）
        with open(output_file, 'rb') as f:
            bom = f.read(2)
            self.assertEqual(bom, b'\xff\xfe', 'UTF-16LE BOMが正しくありません')

        # 品詞が「短縮よみ」にマッピングされているか確認
        lines = content.split('\n')
        data_lines = [line for line in lines if line and not line.startswith('!')]
        for line in data_lines:
            if '\t' in line:
                parts = line.split('\t')
                if len(parts) >= 3:
                    pos = parts[2]
                    # 「記号」が「短縮よみ」に変換されているか
                    self.assertIn(pos, ['短縮よみ', '名詞', '人名', '地名', '顔文字', 'サ変名詞'])

    def test_macos_plist_output(self):
        """macOS plist形式出力のテスト"""
        output_file = Path(self.temp_dir) / 'test.plist'
        self.converter.to_macos_plist(output_file)

        # ファイルが作成されているか
        self.assertTrue(output_file.exists())

        # UTF-8で読み込めるか
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # DOCTYPE宣言の確認
        self.assertIn('<!DOCTYPE plist', content)
        self.assertIn('PropertyList-1.0.dtd', content)

        # XMLとして正しくパースできるか
        tree = ET.parse(output_file)
        root = tree.getroot()

        # plistルート要素の確認
        self.assertEqual(root.tag, 'plist')
        self.assertEqual(root.attrib.get('version'), '1.0')

        # array要素の確認
        array = root.find('array')
        self.assertIsNotNone(array)

        # dict要素（単語エントリ）の確認
        dicts = array.findall('dict')
        self.assertEqual(len(dicts), 5, 'エントリ数が正しくありません')

        # 最初のエントリの構造確認
        first_dict = dicts[0]
        keys = [key.text for key in first_dict.findall('key')]
        self.assertIn('phrase', keys)
        self.assertIn('shortcut', keys)

    def test_txt_output(self):
        """TXT形式出力のテスト"""
        output_file = Path(self.temp_dir) / 'test.txt'
        self.converter.to_txt(output_file)

        # ファイルが作成されているか
        self.assertTrue(output_file.exists())

        # UTF-8で読み込めるか
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # ヘッダーコメントの確認
        self.assertIn('# IME辞書データ', content)

        # タブ区切りデータの確認
        lines = content.split('\n')
        data_lines = [line for line in lines if line and not line.startswith('#')]

        for line in data_lines:
            # タブ区切りであることを確認
            self.assertIn('\t', line)

    def test_category_filter(self):
        """カテゴリフィルタのテスト"""
        # 記号カテゴリのみ
        output_file = Path(self.temp_dir) / 'test_filtered.csv'
        self.converter.to_csv(output_file, categories=['記号'])

        with open(output_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # ヘッダー + データ2件 = 3行
        self.assertEqual(len(rows), 3)

        # 全てのデータが'記号'カテゴリ
        for row in rows[1:]:  # ヘッダーをスキップ
            self.assertEqual(row[6], '記号')  # カテゴリ列（読み_Windows追加で1つずれた）

    def test_multiple_categories_filter(self):
        """複数カテゴリフィルタのテスト"""
        output_file = Path(self.temp_dir) / 'test_multi.csv'
        self.converter.to_csv(output_file, categories=['記号', '人名'])

        with open(output_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # ヘッダー + データ3件 = 4行
        self.assertEqual(len(rows), 4)

        # カテゴリが'記号'または'人名'
        categories = [row[6] for row in rows[1:]]  # 読み_Windows追加で1つずれた
        for cat in categories:
            self.assertIn(cat, ['記号', '人名'])

    def test_stats(self):
        """統計情報のテスト"""
        # エラーなく実行できることを確認
        try:
            self.converter.show_stats()
        except Exception as e:
            self.fail(f"show_stats()でエラーが発生: {e}")

    def test_list_categories(self):
        """カテゴリ一覧表示のテスト"""
        # エラーなく実行できることを確認
        try:
            categories = self.converter.list_categories()
            self.assertIsInstance(categories, list)
            self.assertEqual(len(categories), 4)  # 記号、人名、定型文、無効カテゴリ
            self.assertIn('記号', categories)
            self.assertIn('人名', categories)
            self.assertIn('定型文', categories)
        except Exception as e:
            self.fail(f"list_categories()でエラーが発生: {e}")

    def test_windows_reading_priority(self):
        """Windows用読みの優先使用テスト"""
        output_file = Path(self.temp_dir) / 'test_windows_priority.txt'
        self.converter.to_windows(output_file)

        # ファイルが作成されているか
        self.assertTrue(output_file.exists())

        # UTF-16で読み込み
        with open(output_file, 'r', encoding='utf-16') as f:
            content = f.read()

        # Windows用読みが優先的に使用されているか確認
        # "mem" は "めも" に変換されているはず
        self.assertIn('めも\t', content)
        self.assertNotIn('mem\t', content)

        # "meko" は "めーこ" に変換されているはず
        self.assertIn('めーこ\t', content)
        self.assertNotIn('meko\t', content)

        # Windows用読みがない通常の単語（ひらがな）はそのまま
        self.assertIn('みぎや\t', content)

    def test_macos_plist_uses_standard_reading(self):
        """macOS plist出力では通常の読みを使用することを確認"""
        output_file = Path(self.temp_dir) / 'test_macos_reading.plist'
        self.converter.to_macos_plist(output_file)

        # ファイルが作成されているか
        self.assertTrue(output_file.exists())

        # XMLとしてパース
        tree = ET.parse(output_file)
        root = tree.getroot()

        # shortcut（読み）の値を取得
        shortcuts = []
        array = root.find('array')
        for dict_elem in array.findall('dict'):
            keys = dict_elem.findall('key')
            strings = dict_elem.findall('string')
            for i, key in enumerate(keys):
                if key.text == 'shortcut':
                    shortcuts.append(strings[i].text)

        # macOSでは通常の読みが使用される
        self.assertIn('mem', shortcuts)  # Windows用読みではなく、通常の読み
        self.assertIn('meko', shortcuts)

    def test_macos_txt_output(self):
        """macOS TXT形式出力のテスト（.plist以外）"""
        output_file = Path(self.temp_dir) / 'test_macos.txt'
        self.converter.to_macos(output_file)

        # ファイルが作成されているか
        self.assertTrue(output_file.exists())

        # UTF-8で読み込めるか
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # ヘッダーコメントの確認
        self.assertIn('# macOS日本語入力用辞書', content)
        self.assertIn('# 生成日時:', content)

        # カテゴリ別に整理されているか
        self.assertIn('# 記号', content)
        self.assertIn('# 人名', content)

    def test_empty_words_output(self):
        """単語がない場合の出力テスト"""
        # 空のデータで試す
        empty_data = {
            "辞書情報": {"名前": "空", "説明": "", "更新日": "2025-01-01"},
            "カテゴリ": {}
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            import json
            json.dump(empty_data, f)
            temp_file = f.name

        try:
            converter = DictionaryConverter(temp_file)

            # CSV出力（単語なし）
            csv_file = Path(self.temp_dir) / 'empty.csv'
            converter.to_csv(csv_file)
            # エラーなく実行できることを確認

        finally:
            os.unlink(temp_file)


class TestEdgeCases(unittest.TestCase):
    """エッジケースのテスト"""

    def test_invalid_json_file(self):
        """不正なJSONファイルのテスト"""
        # 存在しないファイル
        with self.assertRaises(Exception) as context:
            DictionaryConverter('/nonexistent/file.json')
        self.assertIn('読み込みに失敗', str(context.exception))

    def test_empty_category(self):
        """空のカテゴリのテスト"""
        # 一時的なJSONファイルを作成
        empty_data = {
            "辞書情報": {"名前": "空", "説明": "", "更新日": "2025-01-01"},
            "カテゴリ": {
                "空カテゴリ": {
                    "説明": "空",
                    "有効": True,
                    "単語リスト": []
                }
            }
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            import json
            json.dump(empty_data, f)
            temp_file = f.name

        try:
            converter = DictionaryConverter(temp_file)
            words = converter._get_all_words()
            self.assertEqual(len(words), 0)
        finally:
            os.unlink(temp_file)

    def test_special_characters(self):
        """特殊文字のテスト"""
        # 特殊文字を含むデータ
        special_data = {
            "辞書情報": {"名前": "特殊", "説明": "", "更新日": "2025-01-01"},
            "カテゴリ": {
                "特殊": {
                    "説明": "特殊文字",
                    "有効": True,
                    "単語リスト": [
                        {
                            "読み": "かっこ",
                            "単語": "<test>",
                            "品詞": "記号",
                            "説明": "XMLエスケープテスト & \"引用符\"",
                            "タグ": []
                        }
                    ]
                }
            }
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            import json
            json.dump(special_data, f)
            temp_file = f.name

        try:
            converter = DictionaryConverter(temp_file)

            # plist出力でXMLエスケープが正しく動作するか
            with tempfile.TemporaryDirectory() as temp_dir:
                plist_file = Path(temp_dir) / 'special.plist'
                converter.to_macos_plist(plist_file)

                # XMLとしてパースできることを確認
                tree = ET.parse(plist_file)
                root = tree.getroot()

                # エスケープされた文字が正しく復元されるか
                strings = root.findall('.//string')
                texts = [s.text for s in strings if s.text]
                self.assertIn('<test>', texts)

        finally:
            os.unlink(temp_file)


def run_tests():
    """テストを実行"""
    # テストスイートを作成
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # テストクラスを追加
    suite.addTests(loader.loadTestsFromTestCase(TestDictionaryConverter))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))

    # テストを実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 結果を返す
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
