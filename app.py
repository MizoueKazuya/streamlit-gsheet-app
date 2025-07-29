import streamlit as st
import pandas as pd

# Excelファイル名
EXCEL_FILE = "福山Bコース.xlsx"

# ファイル読み込み
xls = pd.ExcelFile(EXCEL_FILE)
sheet_names = [s for s in xls.sheet_names if s != "全件"]

# UI：タイトルとシート選択
st.title("福山Bコース 閲覧アプリ")
selected_sheet = st.selectbox("表示する曜日を選んでください", sheet_names)

# シートからデータ取得
df = xls.parse(selected_sheet)

# 必要な列が存在しない場合は追加
for col in ["備考"]:
    if col not in df.columns:
        df[col] = ""

# UI：リスト表示（全体）
st.markdown("### 📋 得意先一覧")
st.dataframe(df)

# UI：行選択
st.markdown("### 🔍 表示したい得意先の行を選んでください")
selected_index = st.number_input(
    "行番号（0〜）", min_value=0, max_value=len(df) - 1, step=1
)

# NaNを空文字として表示する関数
def format_value(val):
    return "" if pd.isna(val) else val

# 選択された行を取得
selected_row = df.iloc[selected_index]

# UI：カード表示
st.markdown("---")
st.markdown("### 🧾 カード表示")

st.markdown(f"""
#### 🏪 {format_value(selected_row['得意先名'])}
- 🔢 **得意先番号**: {format_value(selected_row['得意先番号'])}
- 📅 **お盆休み**: {format_value(selected_row['お盆休み'])}
- 📦 **来場予定数**: {format_value(selected_row['来場予定数'])}
- 📝 **備考**: {format_value(selected_row.get('備考', ''))}
""")
