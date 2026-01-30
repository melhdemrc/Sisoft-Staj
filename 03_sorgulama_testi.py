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

def run_retrieval_test():
    print("--- 1. VERİTABANI BAĞLANTISI ---")
    if not os.path.exists(DB_PATH):
        print(f"[HATA] Veritabanı yok!")
        return

    embedding_function = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    db = Chroma(persist_directory=DB_PATH, embedding_function=embedding_function)
    print("   -> Veritabanı yüklendi.")
    
    query = "FMF hastalığının tedavisinde hangi ilaç kullanılır?"
    
    print(f"\n--- 2. SORGU: '{query}' ---")

    results = db.similarity_search(query, k=3)
    
    print(f"   -> Sistem {len(results)} adet alakalı parça buldu.\n")

    found_answer = False

    for i, doc in enumerate(results):
        print(f"--- SONUÇ #{i+1} ---")
        print(f"{doc.page_content[:150]}...")
        
        if "Kolşisin" in doc.page_content:
            print(f"\nDOĞRU CEVAP BURADA BULUNDU! (Sonuç #{i+1})")
            print(f"   -> İçerik: {doc.page_content}")
            found_answer = True
        print("-" * 30)

    if not found_answer:
        print("İstenen bilgi ilk 3 sonuçta bulunamadı.")

if __name__ == "__main__":
    run_retrieval_test()