import sys
import os
import json
from pdf_to_html_structure import extract_pdf_structure
from paragraph_generator import generate_paragraphs

def main():
    if len(sys.argv) < 2:
        print("使い方: PDFファイルをこの実行ファイルにドラッグ＆ドロップしてください。")
        sys.exit(1)

    pdf_path = sys.argv[1]
    if not pdf_path.lower().endswith(".pdf"):
        print("エラー: 対象ファイルはPDFではありません。")
        sys.exit(1)

    # PDFの構造抽出
    print("PDFの解析を開始します...")
    json_data = extract_pdf_structure(pdf_path)

    # 出力ファイル名の作成
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    folder = os.path.dirname(pdf_path)
    json_output = os.path.join(folder, f"{base_name}.json")
    html_output = os.path.join(folder, f"{base_name}.html")

    # JSON出力
    with open(json_output, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print(f"構造情報を {json_output} に保存しました。")

    # HTML出力（JSONデータをもとに段落生成）
    print("HTMLファイルの生成を開始します...")
    html_data = generate_paragraphs(json_data)
    with open(html_output, "w", encoding="utf-8") as f:
        f.write(html_data)
    print(f"HTMLファイルを {html_output} に保存しました。")

if __name__ == "__main__":
    main()
