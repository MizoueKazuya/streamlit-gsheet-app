import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Excelファイル名
EXCEL_FILE = "福山Bコース.xlsx"

# Excelファイルの読み込み
xls = pd.ExcelFile(EXCEL_FILE)
sheet_names = [s for s in xls.sheet_names if s != "全件"]

# タイトルとシート選択
st.title("福山Bコース 閲覧アプリ（AgGrid版）")
selected_sheet = st.selectbox("表示する曜日を選んでください", sheet_names)

# シートからデータを読み込み
df = xls.parse(selected_sheet)

# 列名をクリーンアップ（空白や改行の削除）
df.columns = df.columns.map(lambda x: str(x).strip())

# 必要な列がなければ追加（空欄列）
for col in ["備考"]:
    if col not in df.columns:
        df[col] = ""

# AgGridの設定
st.markdown("### 📋 得意先一覧（クリックして選択）")
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection('single', use_checkbox=True)  # 単一選択（チェックボックス式）
gb.configure_grid_options(domLayout='normal')
grid_options = gb.build()

# AgGridの表示
grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    height=400,
    theme="streamlit",
    fit_columns_on_grid_load=True,
)

# 選択された行の取得
selected = grid_response['selected_rows']

# カード形式で表示
if len(selected) > 0:
    # 安全に辞書形式へ（DataFrameやSeries対応）
    row = selected[0]
    if isinstance(row, pd.Series):
        row = row.to_dict()

    def format_value(val):
        return "" if pd.isna(val) else val

    st.markdown("---")
    st.markdown("### 🧾 カード表示")

    st.markdown(f"""
    #### 🏪 {format_value(row.get('得意先名', ''))}
    - 🔢 **得意先番号**: {format_value(row.get('得意先番号', ''))}
    - 📅 **お盆休み**: {format_value(row.get('お盆休み', ''))}
    - 📦 **来場予定数**: {format_value(row.get('来場予定数', ''))}
    - 📝 **備考**: {format_value(row.get('備考', ''))}
    """)
else:
    st.info("1件をチェックして選択してください。")
