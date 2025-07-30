import streamlit as st
import pandas as pd

# Excelの全シート読み込み
sheet_dict = pd.read_excel("福山Bコース.xlsx", sheet_name=None)

# シート名から選択（全件、月曜日〜土曜日）
sheet_names = list(sheet_dict.keys())
selected_sheet = st.selectbox("表示する曜日を選択", sheet_names)

# 選択されたシートのDataFrameを取得
df = sheet_dict[selected_sheet]

# タイトル
st.title(f"{selected_sheet}：カード表示")

# カード表示
for index, row in df.iterrows():
    with st.container():
        st.markdown("---")
        st.markdown(f"### {row['得意先名']}")  # ← アイコン削除済み
        st.markdown(f"""
        <div style="font-size:20px;">
            <b>得意先番号：</b>{row['得意先番号']}
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"- お盆休み：**{row['お盆休み']}**")
        st.markdown(f"- 来場予定数：**{row['来場予定数']}**")
        st.markdown(f"- 備考：{row['備考']}")
