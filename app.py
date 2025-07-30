import streamlit as st
import pandas as pd

# Excelファイル読み込み
df = pd.read_excel("福山Bコース.xlsx")

st.title("福山Bコース：カード表示")

# 検索機能（任意）
search = st.text_input("得意先番号または得意先名で検索")

if search:
    df_filtered = df[df.astype(str).apply(lambda x: search in x.to_string(), axis=1)]
else:
    df_filtered = df

# カード表示
for index, row in df_filtered.iterrows():
    with st.container():
        st.markdown("---")
        st.markdown(f"### 🏢 {row['得意先名']}")
        st.markdown(f"- 得意先番号：`{row['得意先番号']}`")
        st.markdown(f"- お盆休み：**{row['お盆休み']}**")
        st.markdown(f"- 来場予定数：**{row['来場予定数']}**")
        st.markdown(f"- 備考：{row['備考']}")
