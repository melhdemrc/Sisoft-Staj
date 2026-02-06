"""
DOSYA: 02_rag_entegrasyonu.py
TARİH: 04.02.2026 (Çarşamba)
KONU: RAG Back-End Entegrasyonu ve Canlı Veri Akışı
"""

import streamlit as st
import time
import os

try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_PATH = "../2.Hafta_RAG_Uygulamalari/chroma_db_storage" 
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

st.set_page_config(
    page_title="FMF Klinik Karar Destek Sistemi",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {background-color: #f8f9fa; font-family: 'Segoe UI', sans-serif;}
    .main-header {font-size: 24px; font-weight: 600; color: #2c3e50; border-bottom: 2px solid #e9ecef; padding-bottom: 10px; margin-bottom: 20px;}
    [data-testid="stSidebar"] {background-color: #2c3e50;}
    [data-testid="stSidebar"] * {color: #ecf0f1 !important;}
    .stChatMessage {background-color: #ffffff; border: 1px solid #e9ecef; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    [data-testid="stChatMessageContent"] {color: #2c3e50;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_rag_system():
    if not os.path.exists(DB_PATH):
        return None, "VERİTABANI BULUNAMADI"
    
    embedding_function = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    db = Chroma(persist_directory=DB_PATH, embedding_function=embedding_function)
    return db, "BAĞLANDI"

db, status_msg = load_rag_system()

with st.sidebar:
    st.markdown("### SİSTEM PANELİ")
    st.markdown("---")
    st.markdown(f"**Durum:** {status_msg}")
    st.markdown("**Veri Kaynağı:** Yerel ChromaDB")
    
    if status_msg == "VERİTABANI BULUNAMADI":
        st.error("Lütfen 2. Hafta klasörünün yolunu kontrol edin!")
    
    st.markdown("---")
    if st.button("Sohbeti Temizle", type="primary"):
        st.session_state.messages = []
        st.rerun()

st.markdown('<div class="main-header">FMF KLİNİK YÖNETİM VE KARAR DESTEK SİSTEMİ</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Sistem çevrimiçi. Tıbbi rehber üzerinden sorgulama yapabilirsiniz."
    })

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=None):
        st.markdown(msg["content"])
if prompt := st.chat_input("Klinik sorgunuzu giriniz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=None):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=None):
        message_placeholder = st.empty()
        
        if db is None:
            full_response = "HATA: Veritabanı bağlantısı kurulamadı."
            message_placeholder.error(full_response)
        else:
            results = db.similarity_search(prompt, k=3)
            
            context_text = ""
            for i, doc in enumerate(results):
                context_text += f"**[KAYNAK {i+1}]:** {doc.page_content}\n\n"
            
            full_response = "Sorgunuzla eşleşen klinik rehber kayıtları aşağıdadır:\n\n" + context_text
            
            display_text = ""
            for chunk in full_response.split():
                display_text += chunk + " "
                time.sleep(0.02)
                message_placeholder.markdown(display_text + "▌")
            
            message_placeholder.markdown(full_response)
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})