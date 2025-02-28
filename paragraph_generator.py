def generate_paragraphs(json_data):
    """
    json_data: ページ情報のリスト。各ページは "zones" キーを持ち、
               各 zone は "blocks" キー、各 block は "lines" キー、
               各 line は "spans" キー（span は dictで "font", "size", "text" など）を持つ想定です。
               
    戻り値: {
         "styleRules": CSSルールの文字列,
         "paragraphsHTML": 各段落を <p> タグでラップした HTML 文字列
    }
    """
    paragraphs = []
    current_paragraph = {
        "text": "",
        "html": "",
        "isspanopen": False,
        "currentSpanStyle": "",
        "lastY": 0  # 前の line_bbox[1]
    }
    style_dict = {}

    def get_span_style(span):
        # フォントサイズを最も近い0.5に丸める
        rounded_size = round(span["size"] * 2) / 2
        # フォントサイズをゼロパディングして4桁にする
        size_str = f"{int(rounded_size * 10):04d}"
        # フォント名内の空白をアンダースコアに置換
        font_class = span["font"].replace(" ", "_")
        class_name = f"{font_class}_{size_str}"
        if class_name not in style_dict:
            style_dict[class_name] = f"font-family: {span['font']}; font-size: {rounded_size}px;"
        return class_name

    # JSONからすべての line を一括取得
    lines = []
    for page in json_data:
        if "zones" in page:
            for zone in page["zones"]:
                if "blocks" in zone:
                    for block in zone["blocks"]:
                        if "lines" in block:
                            for line in block["lines"]:
                                lines.append(line)

    def close_paragraph():
        nonlocal current_paragraph
        if current_paragraph["isspanopen"]:
            current_paragraph["html"] += "</span>"
            current_paragraph["isspanopen"] = False
        # current_paragraph をコピーして追加
        paragraphs.append(current_paragraph.copy())
        # 前回の currentSpanStyle と lastY を引き継いで初期化
        current_paragraph = {
            "text": "",
            "html": "",
            "isspanopen": False,
            "currentSpanStyle": current_paragraph["currentSpanStyle"],
            "lastY": current_paragraph["lastY"]
        }
        return current_paragraph

    def join_line_text(line, current_paragraph):
        for span in line.get("spans", []):
            new_style = get_span_style(span)
            if current_paragraph["currentSpanStyle"] != new_style:
                if current_paragraph["isspanopen"]:
                    current_paragraph["html"] += "</span>"
                    current_paragraph["isspanopen"] = False
            if not current_paragraph["isspanopen"]:
                current_paragraph["currentSpanStyle"] = new_style
                current_paragraph["html"] += f'<span class="{new_style}">'
                current_paragraph["isspanopen"] = True
            # タブ文字は </span>|<span class="new_style"> に変換
            processed_text = span["text"].replace("\t", f'</span>|<span class="{new_style}">')
            current_paragraph["text"] += span["text"]
            current_paragraph["html"] += processed_text
            # line_bbox[1] を更新（line_bbox はリスト形式と想定）
            current_paragraph["lastY"] = line["line_bbox"][1]
        return current_paragraph

    for line in lines:
        # spans が存在しない場合はスキップ
        if "spans" not in line or not line["spans"]:
            continue

        # 前の line と同じ Y 座標の場合は同じ段落に結合
        if current_paragraph["lastY"] == line["line_bbox"][1]:
            current_paragraph = join_line_text(line, current_paragraph)
        else:
            if current_paragraph["text"].endswith("\t"):
                current_paragraph = join_line_text(line, current_paragraph)
            elif current_paragraph["text"].rstrip() and current_paragraph["text"].rstrip()[-1] in ".!?":
                current_paragraph = close_paragraph()
                current_paragraph = join_line_text(line, current_paragraph)
            elif current_paragraph["text"].endswith(" ") and (current_paragraph["currentSpanStyle"] == get_span_style(line["spans"][0])):
                current_paragraph = join_line_text(line, current_paragraph)
            else:
                current_paragraph = close_paragraph()
                current_paragraph = join_line_text(line, current_paragraph)

    # ループ終了後、残った段落をクローズ
    if current_paragraph["text"]:
        close_paragraph()

    # 各段落の HTML を <p> タグでラップ
    paragraphs_html = "\n".join([f"<p>{para['html']}</p>" for para in paragraphs])
    # style_dict から CSS クラスのルールを生成
    style_rules = "\n".join([f".{key} {{ {value} }}" for key, value in style_dict.items()])
  
    # HTML ヘッダーを追加
    html_output = f"""<head>
<meta charset="UTF-8">
<title>PDF to HTML</title>
<style>
.page {{ margin-bottom: 20px; padding: 10px; border: 1px solid #000; }}
.nblock {{ margin: 10px 0; padding: 5px; border: 1px solid #555; }}
p {{ margin: 5px 0; padding: 5px; border: 1px solid #900; }}
span {{ border: 1px solid #ccc; }}
{style_rules}
</style>
</head>
<body>
{paragraphs_html}
</body>"""
    
    return html_output
