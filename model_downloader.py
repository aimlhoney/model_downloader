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
def convert_df(df):
    return df.to_csv().encode("utf-8")

csv = convert_df(optimized_df)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="all_models.csv",
    mime="text/csv",
    type="primary",
)

cols_per_row = 3
rows = [optimized_df[i:i + cols_per_row] for i in range(0, len(optimized_df), cols_per_row)]

# Display in 3-column layout
for row_data in rows:
    cols = st.columns(cols_per_row)
    for col, (_, row) in zip(cols, row_data.iterrows()):
        with col:
            with st.container(border=True, height=750):
                st.header(row['name'],divider=True)

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