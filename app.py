import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Excelファイルの読み込み
EXCEL_FILE = "福山Bコース.xlsx"
xls = pd.ExcelFile(EXCEL_FILE)
sheet_names = [s for s in xls.sheet_names if s != "全件"]

# タイトルとシート選択
st.title("福山Bコース 閲覧アプリ（AgGrid版）")
selected_sheet = st.selectbox("表示する曜日を選んでください", sheet_names)

# シートのデータを読み込み
df = xls.parse(selected_sheet)
df.columns = df.columns.map(lambda x: str(x).strip())

# 「備考」列がなければ追加、あればstr型に統一
if "備考" not in df.columns:
    df["備考"] = ""
else:
    df["備考"] = df["備考"].astype(str)

# AgGridの設定
st.markdown("### 📋 得意先一覧（チェックして選択）")
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection('single', use_checkbox=True)
gb.configure_grid_options(domLayout='normal')
grid_options = gb.build()

# 表の表示（AgGrid）
grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    height=400,
    theme="streamlit",
    fit_columns_on_grid_load=True,
)

# 選択された行を取得
selected = grid_response.get('selected_rows', [])

# NaNやNoneに対応した表示用フォーマッタ
def format_value(val):
    if pd.isna(val) or str(val).lower() in ["nan", "none"]:
        return ""
    return str(val)

# カード形式で表示
if isinstance(selected, list) and len(selected) > 0:
    row = selected[0]
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
