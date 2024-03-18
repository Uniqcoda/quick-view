import os
from dotenv import load_dotenv

import streamlit as st
from streamlit.logger import get_logger
from utils import generate_response

LOGGER = get_logger(__name__)

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_API_KEY')

def run():
    st.set_page_config(
        page_title="Quick View",
        page_icon="📄🕵🏻",
    )

    st.header("Welcome to  Quick View! 📄🕵🏻 ")
    st.write("""
    About Us
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
            with st.spinner('Loading...'):
                response = generate_response(uploaded_doc, openai_api_key, query_text)
                result.append(response)
                del openai_api_key

    if len(result):
        st.info(response)


if __name__ == "__main__":
    run()

# What kind of job titles should I apply for with the CV attached?
# Rate this cover letter