# PDF ParaPara2Html
**英文のPDF** を **段組み** や **囲み記事** などの文章構造を解析し、**読み順に整えた HTML** を生成する WIndows 用ツールです！✍

**PDF をドラッグ＆ドロップ** するだけ！

- Htmlタグに元のフォント情報を style として埋め込んでいます。<br>head内の style を変更すれば、好きな style を適用できます。
- テキストを成形したい方向けに、**JSONデータ** も出力します。
- **OCR**はしていません。文字が埋め込まれている英文PDFが対象です。

## 使い方 🛠
1. **[pdf_parapara2html.exe](https://github.com/runequest77/pdf_parapara2html/releases) をダウンロード**
2. **変換したい PDF を `pdf_parapara2html.exe` にドラッグ＆ドロップ**
3. **PDF と同じフォルダに `PDF名.json` と `PDF名.html` が生成されます。**
### ⚠️ 注 意 ⚠️
初回実行時、「Windows によって PC が保護されました」 や 「発行元が不明なアプリ」 の警告が出ます。

⇒「詳細情報」をクリックして「実行」ボタンを押して起動してください。
> 実行ファイルは Python スクリプトを PyInstaller でビルドしたものです。<br>
> 安全性に懸念のある方は Python の実行環境を整え、`pdf_parapara2html.py` を お使いください。<br>
> スクリプトとして実行すれば Windows 以外でも使えます。

## 一部の方々向け情報 💻
**PDF ParaPara2Html** は作成中の自動翻訳ツールから英文の構造化テキスト抽出の機能だけ抜き出したツールです。
TRPGのルールブックは文章だけだと読み取りにくいため、現在、画面上でPDFと原文と訳文を並べて表示できる **「PDF ParaParaTran」** を作成しています。
Web系のUI開発に不慣れで手探り状態ですので、お手伝いいただける方がいましたらお声がけいただけるとありがたいです。
[X(twitter) @nayuta77](https://x.com/nayuta77)


---


## 技術詳細（興味のある方向け
### 段組み（カラム）の検出
1. テキストブロックのバウンディングボックス（`bbox`）を取得  
2. ページ幅を基準に「大きな隙間」を解析し、カラムを分離
3. 見出しや横断テキストを特別処理し、適切な順序に配置
4. 行間のギャップ解析 → 一定の間隔を超えると新しい段落と判断

### パラグラフの終了判定
1. 英文PDFの特徴として行末にスペースがある場合はパラグラフを閉じない
2. 「行末が句読点（. ! ?）」ならパラグラフを閉じる
3. 文中に混ざるタブは|に置換
5. フォントサイズ・スタイルが変化するごとにスパンタグで括り、スタイルの事後設定を可能に

### 技術スタック
1. `PyMuPDF` を使用したpage-block-line-spanの構造と位置、fontとsizeの抽出
2. multi_column.py による背景画像に基づいたbboxのグループ化
