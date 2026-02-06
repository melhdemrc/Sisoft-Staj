import os
import warnings
warnings.filterwarnings("ignore")

try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_PATH = "chroma_db_storage"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def simulate_llm_generation():
    print("--- 1. RETRIEVAL (BAĞLAM TOPLAMA) ---")
    
    if not os.path.exists(DB_PATH):
        print("HATA: Veritabanı bulunamadı.")
        return

    embedding_function = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    db = Chroma(persist_directory=DB_PATH, embedding_function=embedding_function)

    user_question = "FMF ataklarında ne yapmalıyım, ilaç dozu değişir mi?"
    print(f"Kullanıcı Sorusu: {user_question}\n")
    
    results = db.similarity_search(user_question, k=3)
    
    context_text = ""
    for doc in results:
        context_text += f"- {doc.page_content}\n"
    
    print(f"   -> Sistem {len(results)} adet destekleyici doküman buldu.")

    print("\n--- 2. DİNAMİK PROMPT OLUŞTURMA ---")
    
    final_prompt = f"""
SEN UZMAN BİR ROMATOLOJİ DOKTORUSUN.
Aşağıdaki "Tıbbi Bağlam" içerisinde yer alan bilgileri kullanarak hastanın sorusunu cevapla.
Eğer bilgi bağlamda yoksa "Bilmiyorum" de, asla kendi tahmininle cevap uydurma.

--- TIBBİ BAĞLAM (GÜVENİLİR KAYNAK) ---
{context_text}
---------------------------------------

HASTA SORUSU: {user_question}

DOKTOR CEVABI:
"""
    
    print("-" * 50)
    print(final_prompt)
    print("-" * 50)
    
    print("\n[SİMÜLASYON SONUCU]")
    print("Bu şablon ChatGPT veya Llama modeline gönderildiğinde şu cevabı üretecektir:")
    print(">> 'Atak başlangıcında Kolşisin dozu ARTIRILMAMALIDIR. Ağrı yönetimi için NSAİİ grubu ilaçlar kullanabilirsiniz.'")

if __name__ == "__main__":
    simulate_llm_generation()