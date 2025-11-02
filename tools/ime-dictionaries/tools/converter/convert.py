#!/usr/bin/env python3
"""
IME辞書変換ツール
JSON形式の辞書データを各プラットフォーム用の形式に変換
"""

import json
import csv
import sys
import argparse
from pathlib import Path
from datetime import datetime


class DictionaryConverter:
    def __init__(self, json_file):
        """辞書変換器を初期化"""
        self.json_file = Path(json_file)
        self.data = self._load_json()

    def _load_json(self):
        """JSONファイルを読み込み"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"JSONファイルの読み込みに失敗: {e}")

    def list_categories(self):
        """カテゴリ一覧を表示"""
        categories = self.data.get('カテゴリ', {})
        print("📁 利用可能なカテゴリ:")
        for i, (cat_name, cat_data) in enumerate(categories.items(), 1):
            word_count = len(cat_data.get('単語リスト', []))
            status = "✅" if cat_data.get('有効', True) else "❌"
            print(f"  {i}. {status} {cat_name} ({word_count}件)")
            if cat_data.get('説明'):
                print(f"     {cat_data.get('説明')}")
        print()
        return list(categories.keys())

    def _get_all_words(self, categories=None):
        """全単語を取得（カテゴリフィルタあり）"""
        words = []
        all_categories = self.data.get('カテゴリ', {})

        for cat_name, cat_data in all_categories.items():
            # カテゴリフィルタ
            if categories and cat_name not in categories:
                continue

            # 無効なカテゴリはスキップ
            if cat_data.get('有効', True) is False:
                continue

            for word in cat_data.get('単語リスト', []):
                words.append({
                    **word,
                    'カテゴリ': cat_name
                })

        return words

    def to_csv(self, output_file, categories=None):
        """CSV形式で出力（正しいCSV形式）"""
        words = self._get_all_words(categories)

        if not words:
            print("⚠️  出力する単語がありません")
            return

        with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

            # ヘッダー
            writer.writerow(['読み', '読み_Windows', '単語', '品詞', '説明', 'タグ', 'カテゴリ'])

            # データ
            for word in words:
                tags = ';'.join(word.get('タグ', []))
                writer.writerow([
                    word.get('読み', ''),
                    word.get('読み_Windows', ''),
                    word.get('単語', ''),
                    word.get('品詞', '名詞'),
                    word.get('説明', ''),
                    tags,
                    word.get('カテゴリ', '')
                ])

        print(f"✅ CSV出力完了: {output_file} ({len(words)}件)")
        if categories:
            print(f"   対象カテゴリ: {', '.join(categories)}")

    def to_txt(self, output_file, categories=None):
        """タブ区切りテキスト形式で出力"""
        words = self._get_all_words(categories)

        if not words:
            print("⚠️  出力する単語がありません")
            return

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# IME辞書データ\n")
            f.write(f"# 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# 単語数: {len(words)}件\n")
            if categories:
                f.write(f"# カテゴリ: {', '.join(categories)}\n")
            f.write("# 形式: 読み<TAB>単語<TAB>品詞<TAB>説明\n")
            f.write("\n")

            for word in words:
                f.write(f"{word.get('読み', '')}\t{word.get('単語', '')}\t{word.get('品詞', '名詞')}\t{word.get('説明', '')}\n")

        print(f"✅ TXT出力完了: {output_file} ({len(words)}件)")
        if categories:
            print(f"   対象カテゴリ: {', '.join(categories)}")

    def to_macos_plist(self, output_file, categories=None):
        """macOS日本語入力用.plist形式で出力"""
        import xml.etree.ElementTree as ET
        from xml.dom import minidom

        words = self._get_all_words(categories)

        if not words:
            print("⚠️  出力する単語がありません")
            return

        # plist XML構造を作成
        plist = ET.Element('plist', version='1.0')
        array = ET.SubElement(plist, 'array')

        # 各単語をdictエントリに変換
        for word in words:
            dict_elem = ET.SubElement(array, 'dict')

            # phrase (変換後の単語)
            key_phrase = ET.SubElement(dict_elem, 'key')
            key_phrase.text = 'phrase'
            string_phrase = ET.SubElement(dict_elem, 'string')
            string_phrase.text = word.get('単語', '')

            # shortcut (読み)
            key_shortcut = ET.SubElement(dict_elem, 'key')
            key_shortcut.text = 'shortcut'
            string_shortcut = ET.SubElement(dict_elem, 'string')
            string_shortcut.text = word.get('読み', '')

        # XML宣言とDOCTYPEを追加してフォーマット
        xml_str = ET.tostring(plist, encoding='unicode')

        # minidomで整形
        dom = minidom.parseString(f'<?xml version="1.0" encoding="UTF-8"?>{xml_str}')
        pretty_xml = dom.toprettyxml(indent='\t', encoding='UTF-8').decode('utf-8')

        # 不要な空行を削除
        lines = [line for line in pretty_xml.split('\n') if line.strip()]

        # DOCTYPE追加
        final_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'
        ] + lines[1:]  # XML宣言を除去

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(final_lines))

        print(f"✅ macOS plist形式出力完了: {output_file} ({len(words)}件)")
        if categories:
            print(f"   対象カテゴリ: {', '.join(categories)}")

    def to_macos(self, output_file, categories=None):
        """macOS日本語入力用形式で出力（.plist形式）"""
        # 拡張子に応じて処理を振り分け
        if str(output_file).endswith('.plist'):
            self.to_macos_plist(output_file, categories)
        else:
            # 従来のテキスト形式（互換性のため残す）
            words = self._get_all_words(categories)

            if not words:
                print("⚠️  出力する単語がありません")
                return

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("# macOS日本語入力用辞書\n")
                f.write(f"# 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# 単語数: {len(words)}件\n")
                if categories:
                    f.write(f"# カテゴリ: {', '.join(categories)}\n")
                f.write("\n")

                # カテゴリ別に出力
                current_category = None
                for word in sorted(words, key=lambda x: x.get('カテゴリ', '')):
                    if word.get('カテゴリ') != current_category:
                        current_category = word.get('カテゴリ')
                        f.write(f"\n# {current_category}\n")

                    f.write(f"{word.get('読み', '')}\t{word.get('単語', '')}\t{word.get('品詞', '名詞')}\t{word.get('説明', '')}\n")

            print(f"✅ macOS形式出力完了: {output_file} ({len(words)}件)")
            if categories:
                print(f"   対象カテゴリ: {', '.join(categories)}")

    def _map_pos_for_windows(self, pos):
        """品詞をWindows IME用にマッピング"""
        # Windows IMEで使用可能な品詞
        windows_pos_map = {
            '記号': '短縮よみ',
            '名詞': '名詞',
            '動詞': '名詞',  # Windows IMEでは動詞は使えないので名詞に
            '形容詞': '名詞',  # Windows IMEでは形容詞は使えないので名詞に
            '副詞': '名詞',  # Windows IMEでは副詞は使えないので名詞に
            '人名': '人名',
            '地名': '地名',
            '固有名詞': '名詞',
            '短縮よみ': '短縮よみ',
            '顔文字': '顔文字',
            'サ変名詞': 'サ変名詞'
        }
        return windows_pos_map.get(pos, '名詞')

    def to_windows(self, output_file, categories=None):
        """Windows IME用形式で出力"""
        words = self._get_all_words(categories)

        if not words:
            print("⚠️  出力する単語がありません")
            return

        # BOM付きUTF-16LE（encoding='utf-16'を使うと自動でBOMが付く）
        with open(output_file, 'w', encoding='utf-16') as f:
            # Windows IMEヘッダー
            f.write("!Microsoft IME Dictionary Tool\n")
            f.write("!Version=10.0\n")
            f.write("!CharSet=UTF-16LE\n")
            f.write("!Format=<Reading>\t<Word>\t<POS>\t<Comment>\n")
            f.write("\n")

            # データ
            for word in words:
                pos = self._map_pos_for_windows(word.get('品詞', '名詞'))
                # Windows用読みが設定されていればそれを使用、なければ通常の読みを使用
                reading = word.get('読み_Windows') or word.get('読み', '')
                text = word.get('単語', '')
                comment = word.get('説明', '')

                f.write(f"{reading}\t{text}\t{pos}\t{comment}\n")

        print(f"✅ Windows形式出力完了: {output_file} ({len(words)}件)")
        if categories:
            print(f"   対象カテゴリ: {', '.join(categories)}")

    def show_stats(self):
        """統計情報を表示"""
        categories = self.data.get('カテゴリ', {})
        total_words = sum(len(cat.get('単語リスト', [])) for cat in categories.values())
        active_words = sum(
            len(cat.get('単語リスト', []))
            for cat in categories.values()
            if cat.get('有効', True)
        )

        print("📊 辞書統計情報")
        print(f"  辞書名: {self.data.get('辞書情報', {}).get('名前', 'N/A')}")
        print(f"  更新日: {self.data.get('辞書情報', {}).get('更新日', 'N/A')}")
        print(f"  カテゴリ数: {len(categories)}")
        print(f"  総単語数: {total_words}")
        print(f"  有効単語数: {active_words}")
        print()

        # カテゴリ別詳細
        for cat_name, cat_data in categories.items():
            status = "✅" if cat_data.get('有効', True) else "❌"
            word_count = len(cat_data.get('単語リスト', []))
            print(f"  {status} {cat_name}: {word_count}件 - {cat_data.get('説明', '')}")


def main():
    parser = argparse.ArgumentParser(
        description='IME辞書変換ツール - JSON辞書を各プラットフォーム形式に変換',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 統計情報とカテゴリ一覧を表示
  python convert.py dictionary.json --stats
  python convert.py dictionary.json --list-categories

  # 全カテゴリをCSV出力
  python convert.py dictionary.json --csv output.csv

  # 特定のカテゴリのみをCSV出力（複数選択可）
  python convert.py dictionary.json --csv output.csv --categories "記号・マーク,矢印"

  # macOS用.plist形式で出力（拡張子が.plistの場合は自動でplist形式）
  python convert.py dictionary.json --macos dictionary.plist --categories "記号・マーク,矢印"

  # 全形式で一括出力（macOSは.plist形式で出力）
  python convert.py dictionary.json --all-formats --output-dir ./output

  # 特定カテゴリのみ全形式出力
  python convert.py dictionary.json --all-formats --output-dir ./output --categories "記号・マーク"
        """
    )

    parser.add_argument('json_file', help='入力JSONファイル')
    parser.add_argument('--csv', help='CSV形式で出力')
    parser.add_argument('--txt', help='TXT形式で出力')
    parser.add_argument('--macos', help='macOS形式で出力（.plist拡張子でplist形式、それ以外はテキスト形式）')
    parser.add_argument('--windows', help='Windows形式で出力')
    parser.add_argument('--all-formats', action='store_true', help='全形式で出力')
    parser.add_argument('--output-dir', default='.', help='出力ディレクトリ（--all-formats時）')
    parser.add_argument('--categories', help='出力するカテゴリ（カンマ区切り）複数指定可能')
    parser.add_argument('--stats', action='store_true', help='統計情報を表示')
    parser.add_argument('--list-categories', action='store_true', help='カテゴリ一覧を表示')

    args = parser.parse_args()

    # 引数チェック
    if not any([args.csv, args.txt, args.macos, args.windows, args.all_formats, args.stats, args.list_categories]):
        print("❌ 出力形式を指定してください")
        print("   --csv, --txt, --macos, --windows, --all-formats")
        print("   または --stats, --list-categories")
        sys.exit(1)

    # 変換器を初期化
    try:
        converter = DictionaryConverter(args.json_file)
    except Exception as e:
        print(f"❌ エラー: {e}")
        sys.exit(1)

    # カテゴリ一覧表示
    if args.list_categories:
        converter.list_categories()
        return

    # 統計情報表示
    if args.stats:
        converter.show_stats()
        return

    # カテゴリフィルタ
    categories = None
    if args.categories:
        categories = [cat.strip() for cat in args.categories.split(',')]
        print(f"🔍 対象カテゴリ: {', '.join(categories)}")
        print()

    # 出力ディレクトリ作成
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 変換処理
    try:
        if args.all_formats:
            # 全形式出力
            base_name = Path(args.json_file).stem
            if categories:
                # カテゴリ指定時はファイル名に含める
                cat_suffix = "_" + "_".join(categories)[:30].replace('/', '_')  # ファイル名用に短縮
                base_name = f"{base_name}{cat_suffix}"

            converter.to_csv(output_dir / f"{base_name}.csv", categories)
            converter.to_txt(output_dir / f"{base_name}.txt", categories)
            converter.to_macos(output_dir / f"{base_name}.plist", categories)  # .plist形式で出力
            converter.to_windows(output_dir / f"{base_name}_windows.txt", categories)
        else:
            # 個別出力
            if args.csv:
                converter.to_csv(args.csv, categories)
            if args.txt:
                converter.to_txt(args.txt, categories)
            if args.macos:
                converter.to_macos(args.macos, categories)
            if args.windows:
                converter.to_windows(args.windows, categories)

    except Exception as e:
        print(f"❌ 変換エラー: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
