import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
import os

def get_files_from_dir(path):
    files=[]
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            files.append(file_path)
    return files

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.3, "max_length":1024})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
            
def initialise():
    load_dotenv()

    st.session_state.pdf_docs = get_files_from_dir('D:/College/BTECH PROJECT-1/ChatbotDTU_Final/files')

    # get pdf text
    st.session_state.raw_text = get_pdf_text(st.session_state.pdf_docs)

    # get the text chunks
    st.session_state.text_chunks = get_text_chunks(st.session_state.raw_text)

    # create vector store
    st.session_state.vectorstore = get_vectorstore(st.session_state.text_chunks)

    # create conversation chain
    st.session_state.conversation = get_conversation_chain(st.session_state.vectorstore)


def main():
    st.set_page_config(page_title="NIET Chatbot",
                       page_icon=":rocket:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if("pdf_docs" not in st.session_state):
        initialise()

    st.header("NIET Chatbot (Guidance of Mr.Praveen Kumar) v1 :rocket:")
    user_question = st.text_input("Ask a question about NIET...")
    if user_question:
        handle_userinput(user_question)


if __name__ == '__main__':
    main()