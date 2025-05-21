# 📄 Chat with PDF using LangChain + Gemini + Streamlit

This project allows you to **chat with multiple PDF documents** using Google's **Gemini (Generative AI)** and **LangChain** for question-answering. You can upload multiple PDF files, and ask questions directly — the system will extract relevant context and generate accurate, detailed answers from the content.

---

## 🚀 Features

- 📄 Upload and process multiple PDFs
- 🤖 Ask questions and get context-aware answers
- 🧠 Powered by Google Gemini + LangChain
- ⚡ Uses FAISS for vector-based document retrieval
- 🧩 Clean Streamlit UI for interaction

---

## 🧰 Tech Stack

- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [Google Generative AI (Gemini)](https://ai.google.dev/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [dotenv](https://pypi.org/project/python-dotenv/)

---

## 📁 Directory Structure

.
├── app.py # Main Streamlit app
├── faisss_index/ # Vector store (auto-generated)
├── .env # Environment variables 
├── requirements.txt # Dependencies
└── README.md # Project documentation


▶️ Run the App

streamlit run app.py
Open your browser and go to: http://localhost:8501 (or Streamlit will auto-launch it).


📄 License
This project is licensed under the MIT License.

---------🙋‍♀️ Author---------
Marpally Latha Devi,
Prompt Engineer | Generative AI Developer,
GitHub: lathadevi158