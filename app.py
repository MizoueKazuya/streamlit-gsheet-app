import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Excelファイル
EXCEL_FILE = "福山Bコース.xlsx"

# 読み込み
xls = pd.ExcelFile(EXCEL_FILE)
sheet_names = [s for s in xls.sheet_names if s != "全件"]

# タイトルとシート選択
st.title("福山Bコース 閲覧アプリ（AgGrid版）")
selected_sheet = st.selectbox("表示する曜日を選んでください", sheet_names)

# データ読み込み
df = xls.parse(selected_sheet)

# 必要な列を補完
if "備考" not in df.columns:
    df["備考"] = ""

# UI: Excel風テーブル（AgGrid）
st.markdown("### 📋 得意先一覧（クリックして選択）")

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection('single', use_checkbox=True)  # 1行選択 & チェックボックス表示
gb.configure_grid_options(domLayout='normal')
grid_options = gb.build()

grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    height=400,
    theme="streamlit",  # "alpine", "material", "streamlit" など
    fit_columns_on_grid_load=True,
)

# 選択行の取得
selected = grid_response['selected_rows']

# カードUI表示（選択時のみ）
if selected:
    row = selected[0]

    def format_value(val):
        return "" if pd.isna(val) else val

    st.markdown("---")
    st.markdown("### 🧾 カード表示")

    st.markdown(f"""
    #### 🏪 {format_value(row['得意先名'])}
    - 🔢 **得意先番号**: {format_value(row['得意先番号'])}
    - 📅 **お盆休み**: {format_value(row['お盆休み'])}
    - 📦 **来場予定数**: {format_value(row['来場予定数'])}
    - 📝 **備考**: {format_value(row.get('備考', ''))}
    """)
else:
    st.info("1件をクリックまたはチェックして選択してください。")
