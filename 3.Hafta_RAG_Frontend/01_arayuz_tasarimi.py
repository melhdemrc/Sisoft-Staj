import streamlit as st
import time

st.set_page_config(
    page_title="FMF Klinik Karar Destek Sistemi",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Ana Arka Planı ve Fontları Düzenle */
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Üst Bilgi Alanı (Header) */
    .main-header {
        font-size: 24px;
        font-weight: 600;
        color: #2c3e50;
        border-bottom: 2px solid #e9ecef;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* Yan Menü (Sidebar) Düzenlemeleri */
    [data-testid="stSidebar"] {
        background-color: #2c3e50;
    }
    [data-testid="stSidebar"] * {
        color: #ecf0f1 !important;
    }
    
    /* Mesaj Kutuları Tasarımı */
    .stChatMessage {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Kullanıcı Mesajı Vurgusu */
    [data-testid="stChatMessageContent"] {
        color: #2c3e50;
    }
    
    /* Streamlit Varsayılanlarını Gizle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### SİSTEM PANELİ")
    st.markdown("---")
    
    st.markdown("**Versiyon:** v2.1.0-Stable")
    st.markdown("**Modül:** FMF & Romatoloji")
    st.markdown("**Bağlantı:** Yerel Veritabanı (Secure)")
    
    st.markdown("---")
    st.markdown("### PARAMETRELER")
    
    sensitivity = st.slider("Hassasiyet Ayarı (Threshold)", 0.0, 1.0, 0.75)
    max_response = st.number_input("Maksimum Cevap Uzunluğu", value=500)
    
    st.markdown("---")
    if st.button("Oturumu Sıfırla", type="primary"):
        st.session_state.messages = []
        st.rerun()

st.markdown('<div class="main-header">FMF KLİNİK YÖNETİM VE KARAR DESTEK SİSTEMİ</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Sistem hazır. Veritabanı bağlantısı kuruldu. Lütfen sorgunuzu giriniz."
    })

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=None):
        st.markdown(msg["content"])

if prompt := st.chat_input("Klinik sorgunuzu buraya yazınız..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=None):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=None):
        message_placeholder = st.empty()
        full_response = ""
        
        simulation_text = "Sorgunuz işleniyor... Veritabanı taranıyor... İlgili protokoller getiriliyor. (NOT: Bu arayüz şu an sadece ön yüz tasarımıdır. Yarın RAG entegrasyonu tamamlandığında gerçek tıbbi veriler buradan akacaktır.)"
        
        for chunk in simulation_text.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})