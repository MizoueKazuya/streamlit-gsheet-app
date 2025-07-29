import streamlit as st
import pandas as pd

# Excelファイル
EXCEL_FILE = "福山Bコース.xlsx"

# Excel読み込み
xls = pd.ExcelFile(EXCEL_FILE)
sheet_names = [s for s in xls.sheet_names if s != "全件"]

# タイトルとシート選択
st.title("福山Bコース 閲覧アプリ")
selected_sheet = st.selectbox("表示する曜日を選んでください", sheet_names)

# データ取得
df = xls.parse(selected_sheet)

# 必須列がなければ追加
for col in ["備考"]:
    if col not in df.columns:
        df[col] = ""

# Data Editorを使って選択UI表示
st.markdown("### 📋 得意先一覧（クリックして選択）")
edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    disabled=True,
    hide_index=False,
    key="data_editor"
)

# 選択された行のインデックス取得
selected_row_index = st.session_state["data_editor"]["edited_rows"]
if selected_row_index:
    row_idx = list(selected_row_index.keys())[0]
    selected_row = df.iloc[row_idx]

    # NaNを空文字として表示する関数
    def format_value(val):
        return "" if pd.isna(val) else val

    # カード表示
    st.markdown("---")
    st.markdown("### 🧾 カード表示")

    st.markdown(f"""
    #### 🏪 {format_value(selected_row['得意先名'])}
    - 🔢 **得意先番号**: {format_value(selected_row['得意先番号'])}
    - 📅 **お盆休み**: {format_value(selected_row['お盆休み'])}
    - 📦 **来場予定数**: {format_value(selected_row['来場予定数'])}
    - 📝 **備考**: {format_value(selected_row.get('備考', ''))}
    """)
else:
    st.info("左の一覧から得意先を1行クリックしてください。")
