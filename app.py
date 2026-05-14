import os
import tempfile
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

os.environ["ANONYMIZED_TELEMETRY"] = "False"

load_dotenv()

st.set_page_config(page_title="Legal Document Chatbot", page_icon="⚖️", layout="wide")

# CSS to make the UI look more premium and dynamic
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background: #ffffff;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s ease 0s;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0px 15px 20px rgba(46, 229, 157, 0.4);
        transform: translateY(-2px);
    }
    .css-1d391kg {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.title("⚖️ Legal Document Q&A Chatbot")
st.markdown("Upload your PDFs, Word documents, or provide web URLs to start asking questions!")

# Sidebar for configuration and uploads
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Google Gemini API Key", type="password", placeholder="Paste your API key here")
    if not api_key and not os.environ.get("GOOGLE_API_KEY"):
        st.info("💡 To use this app, please enter your own Google Gemini API Key. You can get a free one from [Google AI Studio](https://aistudio.google.com/app/apikey).")
    
    st.markdown("---")
    st.header("🔒 Admin Access")
    admin_password = st.text_input("Admin Password", type="password")
    is_admin = (admin_password == os.environ.get("ADMIN_PASSWORD", "admin123"))
    
    if is_admin:
        st.success("✅ Admin Access Granted")
        st.header("📄 Upload Data Sources")
        uploaded_files = st.file_uploader("Upload Documents (PDF, DOCX)", type=["pdf", "docx", "doc"], accept_multiple_files=True)
        web_urls = st.text_area("Web URLs (one per line)", placeholder="https://example.com/legal-document")
        process_btn = st.button("🚀 Process Documents")
    else:
        st.info("Log in as Admin to upload new documents.")
        process_btn = False
        uploaded_files = []
        web_urls = ""
    
    st.markdown("---")
    st.markdown("### How to use:")
    st.markdown("1. Enter your Google Gemini API Key.")
    st.markdown("2. Upload your documents or enter URLs.")
    st.markdown("3. Click 'Process Documents'.")
    st.markdown("4. Ask questions in the chat!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
CHROMA_DIR = "./chroma_db"

def process_documents(uploaded_files, web_urls, api_key):
    active_key = api_key or os.environ.get("GOOGLE_API_KEY")
    if not active_key:
        st.error("⚠️ Please provide a Google API Key.")
        return False
        
    documents = []
    
    with st.spinner("⏳ Loading documents..."):
        # Process uploaded files
        for uploaded_file in uploaded_files:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_filepath = temp_file.name
                
            try:
                if file_extension == ".pdf":
                    loader = PyPDFLoader(temp_filepath)
                    documents.extend(loader.load())
                elif file_extension == ".docx":
                    loader = Docx2txtLoader(temp_filepath)
                    documents.extend(loader.load())
                elif file_extension == ".doc":
                    st.error(f"❌ '{uploaded_file.name}' is a .doc file. Please convert it to .docx first.")
            except Exception as e:
                st.error(f"❌ Error loading {uploaded_file.name}: {e}")
            finally:
                os.remove(temp_filepath)
                
        # Process web URLs
        if web_urls.strip():
            urls = [url.strip() for url in web_urls.split('\n') if url.strip()]
            for url in urls:
                try:
                    loader = WebBaseLoader(url)
                    documents.extend(loader.load())
                except Exception as e:
                    st.error(f"❌ Error loading {url}: {e}")
                    
    if not documents:
        st.warning("⚠️ No documents loaded. Please upload files or provide valid URLs.")
        return None
        
    with st.spinner("🧠 Processing and indexing documents..."):
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_documents(documents)
            
            embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=active_key)
            
            # Using Chroma vector store with persistent directory
            vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=CHROMA_DIR)
            st.success("✅ Documents processed successfully!")
            return True
        except Exception as e:
            st.error(f"❌ Error during processing: {e}")
            return False

if process_btn:
    success = process_documents(uploaded_files, web_urls, api_key)
    if success:
        st.session_state.chat_history = [] 

# Chat interface
st.markdown("### 💬 Chat")
chat_container = st.container()

with chat_container:
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "sources" in msg:
                with st.expander("📚 View Sources"):
                    for i, doc in enumerate(msg["sources"]):
                        st.markdown(f"**Source {i+1}:**")
                        st.info(f"{doc.page_content[:300]}...")
                        st.caption(f"Metadata: {doc.metadata}")

if prompt := st.chat_input("Ask a question about the provided documents..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    active_key = api_key or os.environ.get("GOOGLE_API_KEY")
    
    if not os.path.exists(CHROMA_DIR):
        st.warning("⚠️ No documents have been uploaded yet. An admin must upload documents first.")
    elif not active_key:
        st.error("⚠️ Please provide a Google API Key in the sidebar.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=active_key)
                    vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
                    
                    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2, google_api_key=active_key)
                    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
                    
                    system_prompt = (
                        "You are an expert legal assistant specialized in analyzing documents and answering questions based on them. "
                        "Use the following pieces of retrieved context to answer the user's question accurately. "
                        "If the answer cannot be found in the provided context, state clearly that you don't know based on the provided documents. "
                        "Do not make up information. Provide a clear and well-structured answer."
                        "\n\n"
                        "Context:\n{context}"
                    )
                    
                    prompt_template = ChatPromptTemplate.from_messages([
                        ("system", system_prompt),
                        ("human", "{input}"),
                    ])
                    
                    question_answer_chain = create_stuff_documents_chain(llm, prompt_template)
                    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
                    
                    response = rag_chain.invoke({"input": prompt})
                    answer = response["answer"]
                    sources = response["context"]
                    
                    st.write(answer)
                    with st.expander("📚 View Sources"):
                        for i, doc in enumerate(sources):
                            st.markdown(f"**Source {i+1}:**")
                            st.info(f"{doc.page_content[:300]}...")
                            st.caption(f"Metadata: {doc.metadata}")
                    
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": answer,
                        "sources": sources
                    })
                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")
