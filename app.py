import streamlit as st
import os

st.title("My RAG App")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    st.write("File uploaded..", uploaded_file.name)

    save_path = "./temp.pdf"

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File saved successfully to {save_path}")

