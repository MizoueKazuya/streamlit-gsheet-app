import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import os

# Excelファイル名
EXCEL_FILE = "福山Bコース.xlsx"

# ファイル名からタイトル用のベースを取得
file_title = os.path.splitext(os.path.basename(EXCEL_FILE))[0]

# Excelファイルの読み込み
xls = pd.ExcelFile(EXCEL_FILE)
sheet_names = [s for s in xls.sheet_names if s != "全件"]

# タイトルとシート選択
st.title(f"📘 {file_title}")
selected_sheet = st.selectbox("表示する曜日を選んでください", sheet_names)

# シートからデータを読み込み
df = xls.parse(selected_sheet)

# 列名をクリーンアップ
df.columns = df.columns.map(lambda x: str(x).strip())

# 列型の調整
if "得意先番号" in df.columns:
    df["得意先番号"] = pd.to_numeric(df["得意先番号"], errors="coerce")

for col in ["得意先名", "お盆休み", "来場予定数", "備考"]:
    df[col] = df.get(col, "").astype(str)

# AgGridの設定
st.markdown("### 📋 得意先一覧（チェックして選択）")
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection('single', use_checkbox=True)
gb.configure_grid_options(domLayout='normal')
grid_options = gb.build()

# AgGrid 表示
grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    height=400,
    theme="streamlit",
    fit_columns_on_grid_load=True,
)

# 選択された行の取得
selected = grid_response.get('selected_rows', [])

# カード形式で選択行を表示
if selected:
    row = selected[0]

    def show_card(label, key, icon=""):
        value = row.get(key, "").strip()
        if value and value.lower() != "nan":
            st.markdown(f"- {icon} **{label}**: {value}")

    st.markdown("---")
    st.markdown("### 🧾 選択された得意先の情報")
    st.markdown(f"#### 🏪 {row.get('得意先名', '').strip()}")
    show_card("得意先番号", "得意先番号", "🔢")
    show_card("お盆休み", "お盆休み", "📅")
    show_card("来場予定数", "来場予定数", "📦")
    show_card("備考", "備考", "📝")
else:
    st.info("1件をチェックして選択してください。")
