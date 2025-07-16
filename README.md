# 🛒 Procurement AI Assistant

**An interactive AI-powered chatbot for procurement teams, built with Streamlit, LangChain, and OpenAI.**  

---

## ✨ Features

- 💬 **Chat with an AI procurement assistant** for questions, email drafting, and scenario advice.
- 📄 **Upload procurement PDF documents** and ask questions about their contents (Retrieval-Augmented Generation).
- 🧠 **Multi-turn conversation memory** – remembers your chat context.
- 🤖 **Powered by GPT-3.5 Turbo (OpenAI) via LangChain**
- ☁️ **Easy deployment on Streamlit Community Cloud**

---

## 🖥️ Demo Screenshot

<img width="1862" height="1013" alt="image" src="https://github.com/user-attachments/assets/f2f2b981-fe9e-4215-9017-f7fc003581bc" />


---

## 🛠 Tech Stack

- [Streamlit](https://streamlit.io/) — Python UI & deployment
- [LangChain](https://www.langchain.com/) — LLM orchestration & retrieval
- [OpenAI GPT-3.5](https://platform.openai.com/) — Language model
- [FAISS](https://github.com/facebookresearch/faiss) — Vector search for document retrieval
- [PyPDF](https://pypi.org/project/pypdf/) — PDF parsing

---

## 🚀 Local Setup

1. **Clone the repo:**
    ```bash
    git clone https://github.com/rahulsnath206/procurement-chatbot.git
    cd procurement-chatbot
    ```

2. **Create a virtual environment and activate:**
    ```bash
    python -m venv venv
    venv\Scripts\activate      # On Windows
    # or
    source venv/bin/activate  # On Mac/Linux
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your OpenAI API key:**  
   Create a `.env` file in this folder with OPENAI_API_KEY=sk-xxxxxx


5. **Run the app:**
 ```bash
 streamlit run app.py
 ```

---

## ☁️ Deploy on Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click “New app”, select this repo and `app.py`
4. Set your OpenAI API key in “Secrets” on Streamlit Cloud
5. Click “Deploy” and share your public app link!

---

## 📄 Example Use Cases

- “Draft a reminder email to a supplier for a missed delivery.”
- “How do I onboard a new supplier?”
- “Compare these two supplier quotes: A is cheaper, B is faster.”
- “Summarize the key risks in this procurement contract PDF.”

---

\*\* Built with ❤️ using OpenAI, LangChain, and Streamlit. By Rahul Sajeendra Nath\*\*



