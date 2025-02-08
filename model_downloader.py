import os

import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Model Downloader")

st.header("GPT4ALL Model Downloader", divider="rainbow")

dir = "./model_info"

st.subheader("References :")
st.info("https://github.com/nomic-ai/gpt4all/blob/main/gpt4all-chat/metadata/models.json")
st.info("https://github.com/nomic-ai/gpt4all/blob/main/gpt4all-chat/metadata/models2.json")

files = [dir+"/"+f for f in os.listdir(dir)]
dataframe_arr = []
for f in files:
    dataframe_arr.append(pd.read_json(f))
optimized_df = pd.concat(dataframe_arr).drop_duplicates()[['name', 'filename', 'filesize', 'ramrequired', 'parameters', 'quant', 'type', 'description', 'url']]
#st.dataframe(optimized_df, hide_index=True, use_container_width=True)

@st.cache_data
def convert_df(df, type):
    if type ==  "csv":
        return df.to_csv().encode("utf-8")
    elif type == "json":
        return df.to_json(orient="records")

def display_model_detail(row):
    st.header(row['name'], divider=True)

    # Download button
    try:
        st.link_button(f"Download {row['name']}", row['url'], type="secondary", use_container_width=True)
    except:
        st.error("No Downloads available")

    # Model Properties
    st.subheader("Model Property")
    st.write(f"**File Name:** {row['filename']}")
    st.write(f"**File Size:** {row['filesize']} MB")
    st.write(f"**RAM Required:** {row['ramrequired']} GB")
    st.write(f"**Parameters:** {row['parameters']}")
    st.write(f"**Quant:** {row['quant']}")
    st.write(f"**Type:** {row['type']}")

    # Description
    st.subheader("Description")
    st.markdown(str(row['description']), unsafe_allow_html=True)


@st.dialog("Show Model Implementation", width="large")
def show_model_implementation():
    select_model = st.selectbox("Select Model", optimized_df['name'].unique())
    filename = optimized_df[optimized_df["name"] == select_model]["filename"].values[0]
    body_col = st.columns(2, gap="small")
    with body_col[0]:
        code = "```python Installation\n\n !pip install gpt4all\n\n"
        code += """
from gpt4all import GPT4All
llm_model = GPT4All('"""+filename+"""')
        """
        st.markdown(code)
    with body_col[1]:
        for i, item_row in  optimized_df[optimized_df["name"] == select_model].head(1).iterrows():
            with st.container(border=True):
                display_model_detail(item_row)


csv = convert_df(optimized_df, "csv")
json = convert_df(optimized_df, "json")
download_button_cols = st.columns([0.5,0.5,0.5,1.8], gap="small")
with download_button_cols[0]:
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name="all_models.csv",
        mime="text/csv",
        type="primary",
    )
with download_button_cols[1]:
    st.download_button(
        label="Download data as JSON",
        data=json,
        file_name="all_models.json",
        mime="application/json",
        type="primary",
    )
with download_button_cols[2]:
    if st.button(
        label="Show Implementation",
        type="primary"
    ):
        show_model_implementation()


cols_per_row = 3
rows = [optimized_df[i:i + cols_per_row] for i in range(0, len(optimized_df), cols_per_row)]




# Display in 3-column layout
for row_data in rows:
    cols = st.columns(cols_per_row)
    for col, (_, item_row) in zip(cols, row_data.iterrows()):
        with col:
            with st.container(border=True, height=750):
                display_model_detail(item_row)