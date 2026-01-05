import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()
secret_key = os.getenv("API_KEY")

st.title("My RAG App")

api_key = st.text_input("Enter API KEY", value = secret_key if secret_key else "", type="password")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

@st.cache_resource
def get_vectorstore_from_pdf(file_path, api_key):

    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()

    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001",google_api_key=api_key)
    vectorstore = FAISS.from_documents(pages, embeddings)
    return vectorstore

if uploaded_file is not None and api_key:
    os.environ["GOOGLE_API_KEY"] = api_key

    save_path = "./temp.pdf"
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.write("Processing PDF...")

    try:
        vectorstore = get_vectorstore_from_pdf(save_path, api_key)
        st.success("Vector store created! We are ready to search")
    except Exception as e:
        st.error(f"Error creating vector store: {e}")
        