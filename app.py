# importing deps
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Function to get user input for Google API key
def get_google_api_key():
    st.sidebar.subheader("Enter your Google API Key")
    google_api_key = st.sidebar.text_input("Google API Key", type="password")
    return google_api_key

# Function to configure Google API key
def configure_google_api_key(google_api_key):
    genai.configure(api_key=google_api_key)

# input single or multiple pdf's 
def get_pdf_text(pdf_doc):
    text = ''
    for pdf in pdf_doc:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    
# After pdf input, transform into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 10000, chunk_overlap = 1000)
    chunks = text_splitter.split_text(text)
    return chunks

# generating embeddings for the chunks & saving vectors in local
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = 'models/embedding-001')
    vector_store= FAISS.from_texts(text_chunks, embedding= embeddings)
    vector_store.save_local("faiss_index")
    
def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                                   client=genai,
                                   temperature=0.3,
                                   )
    prompt = PromptTemplate(template=prompt_template,
                            input_variables=["context", "question"])
    chain = load_qa_chain(llm=model, chain_type="stuff", prompt=prompt)
    return chain


def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001")  # type: ignore

    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents": docs, "question": user_question}, return_only_outputs=True)

    print(response)
    st.write("Reply: ", response['output_text'])
    


def main():
    st.set_page_config("Askaway")
    st.header("Askaway your PDF's!😃")

    # Section to configure Google API key
    google_api_key = get_google_api_key()
    if google_api_key:
        configure_google_api_key(google_api_key)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")

    user_question = st.text_input("Ask question's from the PDF Files")

    if user_question:
        user_input(user_question)

if __name__ == "__main__":
    main()
