import os
import tempfile
import time
import shutil
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from translations import TRANSLATIONS

os.environ["ANONYMIZED_TELEMETRY"] = "False"

load_dotenv()

# Initialize language in session state
if "lang" not in st.session_state:
    st.session_state.lang = "vi"

t = TRANSLATIONS[st.session_state.lang]

st.set_page_config(page_title=t["page_title"], page_icon="⚖️", layout="wide")

# Language selector in sidebar
with st.sidebar:
    st.header("🌐 Language / Ngôn ngữ")
    lang_choice = st.selectbox(
        "Select Language / Chọn Ngôn ngữ",
        options=["Tiếng Việt", "English"],
        index=0 if st.session_state.lang == "vi" else 1
    )
    new_lang = "vi" if lang_choice == "Tiếng Việt" else "en"
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.rerun()

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

st.title(t["title"])
st.markdown(t["description"])

# Sidebar for configuration and uploads
with st.sidebar:
    st.header(t["config_header"])
    api_key = st.text_input(t["api_key_label"], type="password", placeholder=t["api_key_placeholder"])
    if not api_key and not os.environ.get("GOOGLE_API_KEY"):
        st.info(t["api_key_info"])
    
    st.markdown("---")
    st.header(t["admin_header"])
    admin_password = st.text_input(t["admin_password_label"], type="password")
    is_admin = (admin_password == os.environ.get("ADMIN_PASSWORD", "admin123"))
    
    if is_admin:
        st.success(t["admin_success"])
        st.header(t["upload_header"])
        uploaded_files = st.file_uploader(t["upload_label"], type=["pdf", "docx", "doc"], accept_multiple_files=True)
        web_urls = st.text_area(t["urls_label"], placeholder=t["urls_placeholder"])
        process_btn = st.button(t["process_btn"])
    else:
        st.info(t["admin_info"])
        process_btn = False
        uploaded_files = []
        web_urls = ""
    
    st.markdown("---")
    st.markdown(t["how_to_use_header"])
    st.markdown(t["how_to_use_steps"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
CHROMA_DIR = "./chroma_db"

def process_documents(uploaded_files, web_urls, api_key):
    active_key = api_key or os.environ.get("GOOGLE_API_KEY")
    if not active_key:
        st.error(t["error_api_key"])
        return False
        
    documents = []
    
    with st.spinner(t["spinner_loading"]):
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
                    st.error(t["error_doc_format"].format(file_name=uploaded_file.name))
            except Exception as e:
                st.error(t["error_loading"].format(file_name=uploaded_file.name, error=e))
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
                    st.error(t["error_loading"].format(file_name=url, error=e))
                    
    if not documents:
        st.warning(t["warning_no_docs"])
        return None
        
    with st.spinner(t["spinner_indexing"]):
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_documents(documents)
            
            embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=active_key)
            
            # Process in small batches with long delays to respect the very tight 30K TPM limit
            batch_size = 10
            
            # Initialize Chroma (will connect to existing data if it exists)
            vectorstore = Chroma(
                persist_directory=CHROMA_DIR,
                embedding_function=embeddings
            )
            
            # Optimized for efficiency: larger batches to conserve RPD (Limit 1K), 
            # but longer delays to respect TPM (Limit 30K).
            # 40 chunks * ~250 tokens = ~10,000 tokens per request.
            # 1.5 requests per minute (40s delay) = ~15,000 TPM (Safe under 30K).
            batch_size = 40
            progress_bar = st.progress(0)
            for i in range(0, len(splits), batch_size):
                if i > 0:
                    # Wait 40 seconds between batches to stay under 30K TPM
                    time.sleep(40)
                
                batch = splits[i:i + batch_size]
                vectorstore.add_documents(batch)
                
                # Update progress
                progress = min((i + batch_size) / len(splits), 1.0)
                progress_bar.progress(progress)
            
            st.success(t["success_processed"])
            return True
        except Exception as e:
            st.error(t["error_processing"].format(error=e))
            return False

if process_btn:
    success = process_documents(uploaded_files, web_urls, api_key)
    if success:
        st.session_state.chat_history = [] 

# Chat interface
st.markdown(t["chat_header"])
chat_container = st.container()

with chat_container:
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "sources" in msg:
                with st.expander(t["view_sources"]):
                    for i, doc in enumerate(msg["sources"]):
                        st.markdown(t["source_label"].format(index=i+1))
                        st.info(f"{doc.page_content[:300]}...")
                        st.caption(f"Metadata: {doc.metadata}")

if prompt := st.chat_input(t["chat_placeholder"]):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    active_key = api_key or os.environ.get("GOOGLE_API_KEY")
    
    if not os.path.exists(CHROMA_DIR):
        st.warning(t["warning_no_docs_uploaded"])
    elif not active_key:
        st.error(t["error_api_key_sidebar"])
    else:
        with st.chat_message("assistant"):
            with st.spinner(t["thinking"]):
                try:
                    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=active_key)
                    vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
                    
                    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0.2, google_api_key=active_key)
                    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
                    
                    # Delay 12 seconds to stay within the 5 RPM limit shown in your screenshot
                    time.sleep(12)
                    
                    system_prompt = t["system_prompt"]
                    
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
                    with st.expander(t["view_sources"]):
                        for i, doc in enumerate(sources):
                            st.markdown(t["source_label"].format(index=i+1))
                            st.info(f"{doc.page_content[:300]}...")
                            st.caption(f"Metadata: {doc.metadata}")
                    
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": answer,
                        "sources": sources
                    })
                except Exception as e:
                    st.error(t["error_general"].format(error=e))
