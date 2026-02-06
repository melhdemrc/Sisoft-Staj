import streamlit as st
import os
from difflib import get_close_matches

try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_PATH = "../2.Hafta_RAG_Uygulamalari/chroma_db_storage"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

WHITELIST_KEYWORDS = [
    "fmf", "ailevi", "akdeniz", "ateş", "tedavi", "ilaç", "kolşisin", "colchicine",
    "ağrı", "karın", "göğüs", "eklem", "şişlik", "nöbet", "atak", "genetik", "gen",
    "mutasyon", "m694v", "m680i", "v726a", "amiloidoz", "böbrek", "yetmezlik",
    "tanı", "belirti", "semptom", "doktor", "hastane", "klinik", "romatoloji",
    "gebelik", "hamile", "emzirme", "cerrahi", "ameliyat", "yan", "etki", "etkiler",
    "doz", "prevalans", "sıklık", "türkiye", "çocuk", "yetişkin", "direnç", "anakinra",
    "iltihap", "peritonit", "plörit", "artrit", "eritem", "kızarıklık", "kusma",
    "ishal", "kabızlık", "protein", "idrar", "taşıyıcı", "hasta", "hastalık"
]

st.set_page_config(
    page_title="FMF Klinik Karar Destek Sistemi",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css():
    """Özel CSS stillerini yükler."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
        
        .stApp { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
        section[data-testid="stSidebar"] { background-color: #0F172A; width: 320px !important; padding-top: 2rem; }
        section[data-testid="stSidebar"] * { color: #E2E8F0 !important; }
        
        /* Header Tasarımı */
        .header-container {
            background-color: #FFFFFF; padding: 1.5rem 2rem; border-bottom: 1px solid #E2E8F0;
            margin: -6rem -4rem 2rem -4rem; display: flex; align-items: center;
            position: sticky; top: 0; z-index: 50; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        .header-title { font-size: 1.5rem; font-weight: 700; color: #1E293B; letter-spacing: -0.025em; }

        /* Mesaj Balonları */
        .stChatMessage { background-color: transparent; border: none; padding: 0; margin-bottom: 1.5rem; }
        .stChatMessage [data-testid="stChatMessageContent"] {
            padding: 1.25rem 1.75rem; border-radius: 1rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            font-size: 1rem; line-height: 1.6;
        }
        [data-testid="chatAvatarIcon-user"], [data-testid="chatAvatarIcon-assistant"] { display: None; }
        
        /* Kullanıcı Mesajı (Mavi) */
        .stChatMessage[data-testid="stChatMessage"]:nth-of-type(odd) { flex-direction: row-reverse; }
        .stChatMessage[data-testid="stChatMessage"]:nth-of-type(odd) [data-testid="stChatMessageContent"] {
            background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
            color: #FFFFFF; margin-left: 20%; border-bottom-right-radius: 0.25rem;
        }
        
        /* Asistan Mesajı (Beyaz) */
        .stChatMessage[data-testid="stChatMessage"]:nth-of-type(even) [data-testid="stChatMessageContent"] {
            background-color: #FFFFFF; color: #1E293B; border: 1px solid #E2E8F0;
            margin-right: 20%; border-bottom-left-radius: 0.25rem;
        }
        
        /* Input Alanı */
        div[data-testid="stChatInput"] {
            position: fixed; bottom: 0px; left: 0; right: 0;
            padding: 2rem 5rem 2rem 24rem; background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px); border-top: 1px solid #E2E8F0; z-index: 100;
        }
        .stTextInput input { border-radius: 0.75rem; border: 1px solid #CBD5E1; padding: 1rem 1.25rem; }
        .stTextInput input:focus { border-color: #3B82F6; box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15); outline: none; }
        
        /* Gizleme Kuralları */
        #MainMenu, footer, header {visibility: hidden;}
        
        /* Durum Rozeti */
        .status-badge {
            display: inline-flex; align-items: center; padding: 0.375rem 0.75rem;
            border-radius: 9999px; background-color: rgba(16, 185, 129, 0.1);
            color: #10B981; font-size: 0.875rem; font-weight: 600;
            border: 1px solid rgba(16, 185, 129, 0.2); margin-bottom: 2rem;
        }
        .status-dot { width: 8px; height: 8px; background-color: #10B981; border-radius: 50%; margin-right: 0.5rem; }
        
        /* Temizle Butonu */
        div.stButton > button {
            width: 100%; border-radius: 0.5rem; background-color: #EF4444; color: white;
            border: none; font-weight: 600; margin-top: 1rem;
        }
        div.stButton > button:hover { background-color: #DC2626; color: white; }
    </style>
    """, unsafe_allow_html=True)

load_css()

@st.cache_resource
def load_rag_system():
    """
    Embedding modelini ve ChromaDB veritabanını önbelleğe alır.
    Bu sayede her sorguda model tekrar yüklenmez.
    """
    if not os.path.exists(DB_PATH):
        return None
    embedding_function = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    db = Chroma(persist_directory=DB_PATH, embedding_function=embedding_function)
    return db

db = load_rag_system()

def is_medically_relevant(query):
    """
    Kullanıcı sorgusunun tıbbi bağlamda olup olmadığını kontrol eder.
    Hibrit Yöntem: Kelime kökü eşleşmesi + Bulanık (Fuzzy) eşleşme.
    """
    query_words = query.lower().split()
    
    for word in query_words:
        for keyword in WHITELIST_KEYWORDS:
            if keyword in word: 
                return True
        
        matches = get_close_matches(word, WHITELIST_KEYWORDS, n=1, cutoff=0.85)
        if matches:
            return True
            
    return False

with st.sidebar:
    st.markdown("### KONTROL PANELİ")
    st.markdown("""
        <div class="status-badge">
            <div class="status-dot"></div>
            Sistem Çevrimiçi
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
        <div style='color: #94A3B8; font-size: 0.875rem; margin-bottom: 0.5rem;'>MODÜL</div>
        <div style='font-weight: 500; margin-bottom: 1.5rem;'>FMF Klinik Rehberi</div>
        
        <div style='color: #94A3B8; font-size: 0.875rem; margin-bottom: 0.5rem;'>VERSİYON</div>
        <div style='font-weight: 500; margin-bottom: 1.5rem;'>2.4.0 (Stable)</div>
        
        <div style='color: #94A3B8; font-size: 0.875rem; margin-bottom: 0.5rem;'>BAĞLANTI</div>
        <div style='font-weight: 500;'>Güvenli Yerel DB</div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = [] 
        st.rerun()

st.markdown("""
    <div class="header-container">
        <div class="header-title">FMF Klinik Karar Destek Sistemi</div>
    </div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Sistem hazır. Tıbbi rehber üzerinden sorgulama yapabilirsiniz."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Klinik sorgunuzu buraya yazınız..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if db is None:
            full_response = "Sistem Hatası: Veritabanı bağlantısı kurulamadı."
            message_placeholder.error(full_response)
        else:
            is_relevant = is_medically_relevant(prompt)
            
            if not is_relevant:
                full_response = "🛡️ **Güvenlik Uyarısı:** Girilen sorgu sistemin tıbbi kapsamı dışındadır. Lütfen hastalık, ilaç veya tedavi süreçleri hakkında bir soru sorunuz."
            else:
                results = db.similarity_search(prompt, k=3)
                
                if not results:
                     full_response = "Sistem Mesajı: İlgili kayıt bulunamadı."
                else:
                    context_text = ""
                    for i, doc in enumerate(results):
                        context_text += f"\n\n> **REFERANS {i+1}**\n{doc.page_content}"
                    full_response = "Rehberden derlenen sonuçlar:" + context_text
            
            message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})