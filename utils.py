from PyPDF2 import PdfReader

from langchain_community.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA



def generate_response(uploaded_doc, openai_api_key, query_text):
    # Load document if file is uploaded
    if uploaded_doc is not None:
        # Read the uploaded PDF document
        pdf_reader = PdfReader(uploaded_doc)
        text = ""
        # Extract text from each page
        for page in pdf_reader.pages:
            text += page.extract_text()

        documents = [text]
        
        # Split documents by chunk size
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = text_splitter.create_documents(documents)
        # Select embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        # Create a vectorstore from documents
        db = Chroma.from_documents(texts, embeddings)
        # Create retriever interface
        retriever = db.as_retriever()
        # Create QA chain
        qa = RetrievalQA.from_chain_type(llm=OpenAI(openai_api_key=openai_api_key), chain_type='stuff', retriever=retriever)
        return qa.run(query_text)
    else:
        return None
