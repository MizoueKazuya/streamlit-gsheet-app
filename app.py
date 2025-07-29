import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# Excelファイルの読み込み
file_path = "福山Bコース.xlsx"
xls = pd.ExcelFile(file_path)
sheet_names = xls.sheet_names
selected_sheet = st.selectbox("表示するシートを選んでください", sheet_names)

# 選択したシートのデータを読み込んで表示
df = xls.parse(selected_sheet)
df.columns = df.columns.map(lambda x: str(x).strip())  # 列名を整形
df = df.astype(str)  # 全ての列を文字列として扱うことでエラー防止

# AgGridオプションの設定
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination()
gb.configure_default_column(resizable=True, filter=True, sortable=True)
gb.configure_selection("single", use_checkbox=True)
grid_options = gb.build()

# 表の表示と行の選択
st.markdown("### 📋 一覧表示")
grid_response = AgGrid(df, gridOptions=grid_options, height=300, width='100%', theme="streamlit")
selected = grid_response["selected_rows"]

# カード形式での表示
if isinstance(selected, list) and len(selected) > 0:
    row = selected[0]
    st.markdown("---")
    st.markdown("### 🧾 カード表示")

    st.markdown(f"""
    #### 🏪 {row.get('得意先名', '')}
    - 🔢 **得意先番号**: {row.get('得意先番号', '')}
    - 📅 **お盆休み**: {row.get('お盆休み', '')}
    - 📦 **来場予定数**: {row.get('来場予定数', '')}
    - 📝 **備考**: {row.get('備考', '')}
    """)
else:
    st.info("1件をチェックして選択してください。")
