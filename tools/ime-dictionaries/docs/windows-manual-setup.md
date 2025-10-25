# Windows IME 辞書設定マニュアル

## 概要
WindowsでMicrosoft IME辞書を手動で設定する手順について説明します。

## 対応バージョン
- Windows 10 (バージョン 2004以降)
- Windows 11
- Microsoft IME

## 前提条件
- 日本語キーボード/入力方式が設定済み
- PowerShell実行権限がある
- 辞書ファイルが準備済み

## 自動セットアップの実行

### PowerShell実行ポリシーの設定
管理者権限でPowerShellを開き、以下を実行：

```powershell
Set-ExecutionPolicy RemoteSigned
```

### セットアップスクリプトの実行
```powershell
cd C:\path\to\dotfiles
.\scripts\windows\Setup-Dictionaries.ps1
```

### オプション付きで実行
```powershell
# 処理内容の確認のみ（実際には変更しない）
.\scripts\windows\Setup-Dictionaries.ps1 -WhatIf

# バックアップなしで実行
.\scripts\windows\Setup-Dictionaries.ps1 -Backup:$false
```

## 手動での辞書インポート手順

### Windows 10/11の場合

#### 1. 設定画面を開く
- スタートメニュー > 設定 (歯車アイコン)
- または `Windows + I` キー

#### 2. 言語設定を開く
- 「時刻と言語」をクリック
- 左側のメニューから「言語」を選択

#### 3. 日本語設定を開く
- 「優先する言語」で「日本語」を選択
- 「オプション」ボタンをクリック

#### 4. Microsoft IME設定を開く
- 「キーボード」セクションで「Microsoft IME」を選択
- 「オプション」ボタンをクリック

#### 5. 辞書設定を開く
- 「全般」タブの「辞書とプライバシー」をクリック

#### 6. ユーザー辞書を設定
- 「ユーザー辞書」セクションを見つける
- 「辞書ファイルからの一括登録」をクリック

#### 7. 辞書ファイルをインポート
- ファイル選択ダイアログで `dictionaries\merged_dictionary_windows.txt` を選択
- 「開く」をクリック
- インポート処理が完了するまで待つ

### 従来のIMEツールバーを使用する場合

#### 1. IMEツールバーを表示
- タスクバーの日本語入力アイコンを右クリック
- 「IMEツールバーの表示/非表示」を選択
- 「デスクトップ上でフロート表示」を選択

#### 2. 辞書ツールを開く
- IMEツールバーの「ツール」メニューをクリック
- 「辞書ツール」を選択

#### 3. 辞書ファイルをインポート
- 辞書ツールで「ツール」メニューをクリック
- 「テキストファイルからの登録」を選択
- `dictionaries\merged_dictionary_windows.txt` を選択
- インポート設定を確認して「OK」

## 辞書ファイルの形式

### Windows IME対応形式
```
!Microsoft IME Dictionary Tool
!Version=10.0
!CharSet=UTF-16LE
!Format=<Reading>	<Word>	<POS>	<Comment>

よみ	単語	名詞	説明
```

### 品詞の種類
- `名詞` - 一般的な名詞
- `人名` - 人の名前
- `地名` - 地名・場所名
- `固有名詞` - その他の固有名詞
- `短縮よみ` - 短縮形・略語

## 辞書の内容確認

### 変換候補の確認方法
1. 任意のテキストエディタ（メモ帳など）を開く
2. 日本語入力モードに切り替え
3. 登録した読みを入力
4. スペースキーで変換して候補を確認

### 例：登録内容の確認
- 「js」→ 「JavaScript」
- 「api」→ 「API」
- 「おつ」→ 「お疲れ様です」
- 「mtg」→ 「Meeting」

## 個別カテゴリのインポート

### カテゴリ別インポートの手順
特定のカテゴリのみインポートしたい場合：

```powershell
# 技術用語のみインポート
.\scripts\windows\Setup-Dictionaries.ps1 -Categories "tech"

# ビジネス用語のみインポート
.\scripts\windows\Setup-Dictionaries.ps1 -Categories "business"
```

## トラブルシューティング

### インポートに失敗する場合

#### 1. ファイル形式の確認
- ファイルがUTF-16LEエンコーディングか確認
- BOMが付いているか確認
- タブ区切りの形式になっているか確認

#### 2. 権限の問題
```powershell
# ファイルの権限確認
Get-Acl "dictionaries\merged_dictionary_windows.txt"

# 実行ポリシーの確認
Get-ExecutionPolicy
```

#### 3. IMEの再起動
- Windows を再起動
- または以下のコマンドでIMEプロセスを再起動：
```cmd
taskkill /f /im ctfmon.exe
start ctfmon.exe
```

### 変換候補に表示されない場合

#### 1. 学習辞書のクリア
- IME設定 > 辞書とプライバシー > 学習履歴の削除

#### 2. 変換エンジンのリセット
- IME設定 > 全般 > 詳細設定 > 変換エンジンをリセット

#### 3. ユーザー辞書の再構築
- IME設定でユーザー辞書を一度削除
- 辞書ファイルを再インポート

## 辞書の管理と更新

### 新しい単語の追加
1. 該当するカテゴリファイルに単語を追加
2. スクリプトを再実行して統合辞書を更新
3. 新しい辞書ファイルを再インポート

### 辞書の削除
- IME設定 > 辞書とプライバシー > ユーザー辞書の編集
- 不要なエントリを選択して削除

### バックアップの管理
バックアップファイルの場所：
```
%USERPROFILE%\.dotfiles_dictionary_backup_YYYYMMDD_HHMMSS\
```

## 高度な設定

### レジストリでの設定確認
```powershell
# IME設定の確認
Get-ItemProperty "HKCU:\Software\Microsoft\IME\15.0\IMEJP\Dictionaries"
```

### グループポリシーでの管理
企業環境での一括設定：
- `gpedit.msc` でローカルグループポリシーエディターを開く
- コンピューターの構成 > 管理用テンプレート > Windows コンポーネント > IME

## パフォーマンス最適化

### 大きな辞書ファイルの分割
辞書ファイルが大きい場合（10,000エントリ以上）：

```powershell
# 辞書を複数ファイルに分割
$DictContent = Get-Content "merged_dictionary_windows.txt"
$ChunkSize = 5000
for ($i = 0; $i -lt $DictContent.Length; $i += $ChunkSize) {
    $DictContent[$i..($i + $ChunkSize - 1)] | Out-File "dictionary_part_$($i/$ChunkSize + 1).txt" -Encoding Unicode
}
```

### 変換速度の最適化
- 使用頻度の高い単語を辞書の上部に配置
- 不要な辞書エントリを削除
- 定期的に学習履歴をクリア

## 参考情報

### 関連レジストリキー
```
HKEY_CURRENT_USER\Software\Microsoft\IME\15.0\IMEJP\Dictionaries
HKEY_CURRENT_USER\Software\Microsoft\InputMethod\Settings
```

### 便利なキーボードショートカット
- `Ctrl + F10` - IMEメニューを開く
- `Ctrl + Shift + カタカナひらがな` - IME無効化
- `Alt + カタカナひらがな` - IME有効化
- `F6` - ひらがな変換
- `F7` - カタカナ変換
- `F8` - 半角カナ変換
- `F9` - 全角アルファベット変換
- `F10` - 半角アルファベット変換