import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import langchain
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

langchain.debug=True

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_pdf_text(pdf_docs):
    
    #Extracts text from a list of PDF documents.

    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    
    #Splits a large text into smaller chunks for efficient processing.

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    
    #Creates a vector store from a list of text chunks.

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faisss_index")
    return vector_store


def get_conversional_chain():
    
    #Creates a conversational chain for question answering.

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details along with corresponding images and tables as well if asked. If the answer is not available in the context, just say, "answer is not available in the context", don't provide the wrong answer.
    Gnerate images from the PDF document whenever a question related to that image is asked.

    Context:
    {context}?

    Question:
    {question}

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain


def user_input(user_question, processed_pdf_text):
    
    #Processes user input and generates a response using the conversational chain

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faisss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversional_chain()

    # Combine user question and processed PDF text as context
    context = f"{processed_pdf_text}\n\nQuestion: {user_question}"

    response = chain({"input_documents": docs, "question": user_question, "context": context}, return_only_outputs=True)

    print(response)
    st.write("Response: ", response["output_text"])


def main():
    
    #Main function for the Streamlit app.

    st.set_page_config("Chat With Multiple PDF")
    st.header("Chat with PDF's ")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        if st.session_state.get("pdf_docs"):
            processed_pdf_text = get_pdf_text(st.session_state["pdf_docs"])
            user_input(user_question, processed_pdf_text)
        else:
            st.error("Please upload PDF files first.")

    with st.sidebar:
        st.title("Home:")
        pdf_docs = st.file_uploader("Upload Files & Click Submit to Proceed", type="pdf", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = ""
                text_chunks = []
                for pdf in pdf_docs:
                    pdf_reader = PdfReader(pdf)
                    for page in pdf_reader.pages:
                        raw_text += page.extract_text()
                text_chunks = get_text_chunks(raw_text)
                vector_store = get_vector_store(text_chunks)
                chain = get_conversional_chain()
                st.session_state["pdf_docs"] = pdf_docs
                st.session_state["text_chunks"] = text_chunks
                st.session_state["vector_store"] = vector_store
                st.session_state["chain"] = chain
                st.success("PDFs processed successfully!")

        if st.button("Reset"):
            st.session_state["pdf_docs"] = []
            st.session_state["text_chunks"] = []
            st.session_state["vector_store"] = None
            st.session_state["chain"] = None
            st.experimental_rerun()

        if st.session_state.get("pdf_docs"):
            st.subheader("Uploaded Files:")
            for i, pdf_doc in enumerate(st.session_state["pdf_docs"]):
                st.write(f"{i+1}. {pdf_doc.name}")


if __name__ == "__main__":
    main()