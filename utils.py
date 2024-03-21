import os
import numpy as np
from PyPDF2 import PdfReader
import cv2
import pytesseract
import openai
from langchain_community.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()

# OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def process_pdf(file):
    pdf_file = PdfReader(file)
    text = ""
    # Extract text from each page
    for page in pdf_file.pages:
        text += page.extract_text()
    return text

def process_image(file_bytes):
    # Convert bytes to numpy array
    nparr = np.frombuffer(file_bytes, np.uint8)
    
    # Decode image
    image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Perform OCR on the preprocessed image
    text = pytesseract.image_to_string(img_rgb)
    
    return text

def generate_response(doc_text, openai_api_key, query_text):
    try:
        # Split documents by chunk size
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        text = text_splitter.create_documents(doc_text)

        # Create embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        # Create a vectorstore from documents
        db = Chroma.from_documents(text, embeddings)
        # Create retriever interface
        retriever = db.as_retriever()
        # Create QA chain
        qa = RetrievalQA.from_chain_type(llm=OpenAI(openai_api_key=openai_api_key), chain_type='stuff', retriever=retriever)
        return qa.run(query_text)
    except Exception as e:
        print(f"An error occurred with OpenAI: {e}")
        print(type(e))
        return f"An error occurred with OpenAI"
   