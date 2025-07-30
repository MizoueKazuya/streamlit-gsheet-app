# app.py
import streamlit as st
import pandas as pd

# Excelファイル読み込み
df = pd.read_excel("福山Bコース.xlsx")

st.title("福山Bコース一覧")

# 一覧表示
st.dataframe(df)

# 得意先番号か得意先名で検索（簡易）
search = st.text_input("得意先番号または得意先名で検索")
if search:
    df_filtered = df[df.astype(str).apply(lambda x: search in x.to_string(), axis=1)]
else:
    df_filtered = df

# 行選択
selected = st.selectbox("詳細を見たい行を選択", df_filtered.index)
st.write("選択された得意先：", df_filtered.loc[selected]["得意先名"])

# 詳細表示
st.subheader("詳細情報")
st.write(df_filtered.loc[selected])
