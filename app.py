import streamlit as st
import pandas as pd
import os

# Excelファイルパスとファイル名の処理
excel_path = "福山Bコース.xlsx"
file_basename = os.path.splitext(os.path.basename(excel_path))[0]

# 全シート読み込み
sheet_dict = pd.read_excel(excel_path, sheet_name=None)

# シート選択（タブ名をプルダウンで選択）
sheet_names = list(sheet_dict.keys())
selected_sheet = st.selectbox("表示する曜日を選択", sheet_names)

# 選択されたシートのDataFrameを取得
df = sheet_dict[selected_sheet]

# ✅ タイトルにファイル名（xxxx）を使用
st.title(f"{file_basename}：{selected_sheet}表示")

# ✅ 検索機能（得意先番号・得意先名の部分一致）
search_term = st.text_input("得意先番号または得意先名で検索")

if search_term:
    df = df[df.apply(lambda row: search_term in str(row.get('得意先番号', '')) or 
                                    search_term in str(row.get('得意先名', '')), axis=1)]

# ✅ カード表示
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
