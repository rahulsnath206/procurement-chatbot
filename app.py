import os
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Procurement AI Assistant", page_icon="🛒")
st.markdown("<h1 style='color: #0e3761;'>🛒 Procurement AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("##### Upload procurement documents (PDF), chat, and get AI-powered insights!")

# PERSONALIZED SYSTEM PROMPT (edit this!)
SYSTEM_PROMPT = (
    "You are expert Procurement AI Assistant. "
    "You help users with procurement policies, vendor management, and decision support. "
    "If the user uploads a document, use ONLY that document for specific answers. "
    "If the answer is not found in the document, say you don't have enough info and suggest general guidance. "
    "Always be concise, accurate, and use a friendly, professional tone. "
    "If the user asks for a summary, contract risks, or compliance issues, look for key points in the file. "
    "Greet users warmly as a Procurement digital assistant."
)

# Document upload + retrieval
uploaded_file = st.file_uploader("Upload a procurement document (PDF only)", type=["pdf"])

retriever = None

if uploaded_file:
    with st.spinner("Processing document..."):
        # Save uploaded file to disk temporarily
        with open("temp_doc.pdf", "wb") as f:
            f.write(uploaded_file.read())
        # Load and split PDF
        loader = PyPDFLoader("temp_doc.pdf")
        docs = loader.load_and_split()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        splits = text_splitter.split_documents(docs)
        # Embed and index
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        vectorstore = FAISS.from_documents(splits, embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

        st.success("Document processed! Ask questions about its content.")

# Chat memory
if "history" not in st.session_state:
    st.session_state["history"] = StreamlitChatMessageHistory()

# Prompt with retrieval (if doc uploaded)
prompt_msgs = [
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
]
if retriever:
    # Add document context placeholder if using retrieval
    from langchain_core.prompts import PromptTemplate
    prompt_msgs.insert(2, ("system", "Context from uploaded document:\n{context}"))

prompt = ChatPromptTemplate.from_messages(prompt_msgs)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5, openai_api_key=openai_api_key)

# Retrieval function for RunnableWithMessageHistory
def get_context(inputs):
    if retriever:
        docs = retriever.get_relevant_documents(inputs["input"])
        context = "\n\n".join([d.page_content for d in docs])
        return {"context": context}
    return {"context": ""}

chain = RunnableWithMessageHistory(
    prompt | llm,
    lambda session_id: st.session_state["history"],
    input_messages_key="input",
    history_messages_key="history",
    partial_variables=get_context if retriever else None
)

# Fancy chat display with avatars
for msg in st.session_state["history"].messages:
    if msg.type == "ai":
        st.chat_message("assistant", avatar="🛒").write(msg.content)
    elif msg.type == "human":
        st.chat_message("user", avatar="🧑").write(msg.content)

user_input = st.chat_input("Ask about procurement or your uploaded document...")

if user_input:
    st.chat_message("user", avatar="🧑").write(user_input)
    with st.chat_message("assistant", avatar="🛒"):
        with st.spinner("Thinking..."):
            result = chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": "session-1"}}
            )
            response = result.content if hasattr(result, "content") else result
            st.write(response)

if st.button("New Conversation"):
    st.session_state["history"].clear()
    st.rerun()

