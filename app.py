import os
from dotenv import load_dotenv

import streamlit as st
from utils import generate_response

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_API_KEY')

def run():
    st.set_page_config(
        page_title="Quick View",
        page_icon="📄🕵🏻",
    )

    st.header("Welcome to  Quick View! 📄🕵🏻 ")

    st.write("""
    ### How to use Quick View
    
    Quick View is your trusty document assistant! 🚀 
    
    Simply upload one or more documents, and ask any questions you have about them. 
    Our advanced LangChain 🦜️🔗 and OpenAI technology will provide you with insightful answers while retaining context.
    
    **Here's how to get started:**
    1. **Upload your document:** You can upload PDF files.
    2. **Enter your question:** Type your question about the doc in the text box provided.
    3. **Submit and wait for the magic:** Click on the "Submit" button, and our Quick View assistant will do the rest!
    
    If you're requested to enter your OpenAI API key, please make sure to provide it. App owner may have run out of free credits. Don't worry, it is never stored and it is safe! 🔒

    """)

    uploaded_doc = st.file_uploader('Upload your document', type='pdf')
    query = st.text_input('Enter your question:', disabled=not uploaded_doc)
    result = None
    
    with st.form('myform', clear_on_submit=True):
        if not OPENAI_KEY:
            openai_api_key = st.text_input('OpenAI API Key', type='password', disabled=not (uploaded_doc and query))
        else:
            openai_api_key = OPENAI_KEY
        submitted = st.form_submit_button('Submit', disabled=not(uploaded_doc and query))
        if submitted and openai_api_key.startswith('sk-'):
            with st.spinner('Loading...'):
                response = generate_response(uploaded_doc, openai_api_key, query)
                result = response
                del openai_api_key

    if result:
        st.info(result)

    # Instructions for getting an OpenAI API key
    st.subheader("How to get your OpenAI API key")
    st.write("You can get your own OpenAI API key by following the instructions:")
    st.write("""
    1. Go to [OpenAI API Keys](https://platform.openai.com/account/api-keys).
    2. Click on the `+ Create new secret key` button.
    3. Next, enter an identifier name (optional) and click on the `Create secret key` button.
    """)

if __name__ == "__main__":
    run()

# What kind of job titles should I apply for with the CV attached?
# Rate this cover letter