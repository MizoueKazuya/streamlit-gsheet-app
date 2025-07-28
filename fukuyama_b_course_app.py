
import streamlit as st
import pandas as pd

# Excelファイルの読み込み
xls = pd.ExcelFile("福山Bコース.xlsx")

# シート名（全件を除く）
sheet_names = [name for name in xls.sheet_names if name != "全件"]

# タイトル
st.title("福山Bコース 閲覧アプリ")
st.markdown("※ 得意先番号または得意先名で検索できます。")

# シート選択
selected_sheet = st.selectbox("表示する曜日を選んでください", sheet_names)

# データ読み込み
df = xls.parse(selected_sheet)

# 検索入力
search_term = st.text_input("得意先番号 または 得意先名 で検索", "")

# フィルター処理
if search_term:
    filtered_df = df[
        df.astype(str).apply(lambda row: search_term in row.to_string(), axis=1)
    ]
else:
    filtered_df = df

# 表示
st.dataframe(filtered_df)
