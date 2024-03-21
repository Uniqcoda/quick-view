import os
from dotenv import load_dotenv
import streamlit as st
from utils import process_image, process_pdf, generate_response

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_API_KEY')

def main():
    st.set_page_config(
        page_title="Quick View",
        page_icon="📄🕵🏻",
    )

    st.title("Welcome to  Quick View! 📄🕵🏻 ")

    st.write("""
    ### How to use Quick View
    
    Quick View is your trusted document assistant! 🚀 
    
    Simply upload a document (PDF, PNG, or JPG), and ask any questions you have about them. 
    Our advanced LangChain 🦜️🔗 and OpenAI technology will provide you with insightful answers while retaining context.

    If you're requested to enter your OpenAI API key, please make sure to provide it. App owner may have run out of free credits. Don't worry, it is never stored and it is safe! 🔒
    """)

    uploaded_doc = st.file_uploader('Upload your document', type=["pdf", "png", "jpg"])
    extracted_text = None
    
    if uploaded_doc is not None:
        file_bytes = uploaded_doc.read()
        # Process the file based on type
        if uploaded_doc.type == "application/pdf":
            extracted_text = process_pdf(uploaded_doc)
        else:
            extracted_text = process_image(file_bytes)

    query = st.text_input('Enter your question about the document:', disabled=not uploaded_doc)
   
    result = None
    
    with st.form('myform', clear_on_submit=True):
        openai_api_key = OPENAI_KEY or st.text_input('OpenAI API Key', type='password', disabled=not (uploaded_doc and query))
        submitted = st.form_submit_button('Submit', disabled=not(uploaded_doc and query))
        if submitted and openai_api_key.startswith('sk-') and extracted_text:
            with st.spinner('Loading...'):
                response = generate_response(extracted_text, openai_api_key, query)
                result = response
                del openai_api_key

    st.subheader("Result")
    if result:
        st.write(result)

    # Instructions for getting an OpenAI API key
    st.subheader("How to get your OpenAI API key")
    st.write("You can get your own OpenAI API key by following the instructions:")
    st.write("""
    1. Go to [OpenAI API Keys](https://platform.openai.com/account/api-keys).
    2. Click on the `+ Create new secret key` button.
    3. Next, enter an identifier name (optional) and click on the `Create secret key` button.
    """)

if __name__ == "__main__":
    main()

# What kind of job titles should I apply for with the CV attached?
# Rate this cover letter