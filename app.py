import os
import streamlit as st
import pandas as pd
# ファビコン変更
st.set_page_config(
    page_title="2025年_お盆",
    page_icon="Kicon.PNG"
)

# 🔸 福山●コース.xlsx に一致するファイルだけを対象とする
excel_files = sorted([f for f in os.listdir() if f.startswith("福山") and f.endswith("コース.xlsx")])

# ファイルが存在する場合のみ処理する
if excel_files:
    selected_file = st.selectbox("表示するコースファイルを選択してください", excel_files)
    file_basename = os.path.splitext(selected_file)[0]

    # 全シート読み込み
    sheet_dict = pd.read_excel(selected_file, sheet_name=None)

    # シート選択
    sheet_names = list(sheet_dict.keys())
    selected_sheet = st.selectbox("表示する曜日を選択", sheet_names)

    # データ取得
    df = sheet_dict[selected_sheet]

    # タイトル表示
    st.title(f"{file_basename}：{selected_sheet}表示")

    # 検索
    search_term = st.text_input("得意先番号または得意先名で検索")
    if search_term:
        df = df[df.apply(lambda row: search_term in str(row.get('得意先番号', '')) or 
                                        search_term in str(row.get('得意先名', '')), axis=1)]

    # カード表示
    for index, row in df.iterrows():
        with st.container():
            st.markdown("---")
            st.markdown(f"### {row['得意先名']}")
            st.markdown(f"""
            <div style="font-size:20px;">
                <b>得意先番号：</b>{row['得意先番号']}
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"- お盆休み：**{row['お盆休み']}**")
            st.markdown(f"- 来場予定数：**{row['来場予定数']}**")
            st.markdown(f"- 備考：{row['備考']}")
else:
    st.warning("対象のExcelファイル（福山●コース.xlsx）が見つかりません。")
