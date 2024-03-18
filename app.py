# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from dotenv import load_dotenv

import streamlit as st
from streamlit.logger import get_logger

from langchain_community.llms import openai
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import retrieval_qa
from langchain_community.vectorstores import chroma
from langchain_community.embeddings import OpenAIEmbeddings


LOGGER = get_logger(__name__)

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_API_KEY')


def generate_response(uploaded_doc, openai_api_key, query_text):
    # Load document if file is uploaded
    if uploaded_doc is not None:
        documents = [uploaded_doc.read().decode()]
        # Split documents by chunk size
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = text_splitter.create_documents(documents)
        # Select embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        # Create a vectorstore from documents
        db = chroma.from_documents(texts, embeddings)
        # Create retriever interface
        retriever = db.as_retriever()
        # Create QA chain
        qa = retrieval_qa.from_chain_type(llm=openai(openai_api_key=openai_api_key), chain_type='stuff', retriever=retriever)
        return qa.run(query_text)
    else:
        return None


def run():
    st.set_page_config(
        page_title="Quick View",
        page_icon="📄🕵🏻",
    )

    st.header("About Quick View! 📄🕵🏻 ")
    st.write("""
    Welcome to Quick View!
    """)

    # File upload
    uploaded_doc = st.file_uploader('Upload a document', type='pdf')
    # Query text
    query_text = st.text_input('Enter your question:', placeholder = 'Please provide a short summary.', disabled=not uploaded_doc)

    # Form input and query
    result = []
    with st.form('myform', clear_on_submit=True):

        if not OPENAI_KEY:
            openai_api_key = st.text_input('OpenAI API Key', type='password', disabled=not (uploaded_doc and query_text))
        else:
            openai_api_key = OPENAI_KEY
        submitted = st.form_submit_button('Submit', disabled=not(uploaded_doc and query_text))
        if submitted and openai_api_key.startswith('sk-'):
            with st.spinner('Calculating...'):
                response = generate_response(uploaded_doc, openai_api_key, query_text)
                result.append(response)
                del openai_api_key

    if len(result):
        st.info(response)


if __name__ == "__main__":
    run()
