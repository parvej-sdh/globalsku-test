import streamlit as st 
import pandas as pd 
import json
import requests

st.set_page_config(layout="wide")
url_path = "http://ai-lb-776202452.us-east-2.elb.amazonaws.com/generate/query_generator/"
# url_path = "http://0.0.0.0:5000/generate/query_generator/"

def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )

def chunk_and_convert_to_json(chunk):
    json_chunk = {"rows": []}
    for row in chunk:
        json_row = [{"header": key, "value": (value if pd.notna(value) else None)} for key, value in row.items()]
        json_chunk["rows"].append(json_row)
    return json_chunk

if __name__ == "__main__":
    icon("GlobalSKU")

    st.subheader("Welcome to the GlobalSKU Search Query Generator",
                 divider="rainbow", anchor=False)

    
    with st.sidebar:
        st.header("👇Upload an Excel file")
        with st.form("my_form"):
            file_upload = st.file_uploader("Upload File", type=["xlsx"])
            submitted = st.form_submit_button("Run")

        st.divider()

    if submitted:
        data = pd.read_excel(file_upload)
        data = data.to_dict(orient="records")
        chunk_size = 3

        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        
        for i, chunk in enumerate(chunks):
            json_chunks = chunk_and_convert_to_json(data)
            json_data = json.dumps(json_chunks)
            res = requests.post(url_path, json=json_chunks)
            res = res.json()
            print(res)
            if res["status"] == 200:
                results = [item for item in res["result"]["itmes"]["searchQuery"]]

                response_df = pd.DataFrame(chunk)
                response_df["Search Query"] = results
                print(response_df)
                st.subheader(f"Result for {i+1} chunk: ", anchor=False, divider="rainbow")
                st.write(response_df)
            else:
                st.write(res["message"])