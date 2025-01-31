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
        st.header("Upload a file")
        with st.form("my_form"):
            file_upload = st.file_uploader("Upload File", type=["xlsx", "csv"])
            submitted = st.form_submit_button("Run")

        st.divider()

    if submitted:
        if file_upload is not None:
            if file_upload.name.endswith('.xlsx'):
                data = pd.read_excel(file_upload)
            elif file_upload.name.endswith('.csv'):
                data = pd.read_csv(file_upload)
        
        data = data.astype(str).to_dict(orient="records")
        chunk_size = 2

        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        
        for i, chunk in enumerate(chunks):
            json_chunks = chunk_and_convert_to_json(data)
            json_data = json.dumps(json_chunks)
            res = requests.post(url_path, json=json_chunks)
            res = res.json()
            print(res)
            if res["status"] == 200:
                
                # results = [item["searchQuery"] for item in res["results"]["items"]]

                response_df = pd.DataFrame(res["results"]["items"])
                # response_df["Search Query"] = results
                print(response_df)
                # print(results)
                st.subheader(f"Result for chunk- {i+1} ", anchor=False, divider="rainbow")
                st.table(response_df)
            else:
                st.write(res["message"])