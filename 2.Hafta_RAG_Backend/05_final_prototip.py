import os
import warnings
warnings.filterwarnings("ignore")
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_PATH = "chroma_db_storage"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def main():
    print("=== RAG SAĞLIK ASİSTANI PROTOTİPİ ===")
    print("Sistem yükleniyor, lütfen bekleyin...\n")

    if not os.path.exists(DB_PATH):
        print("HATA: Veritabanı bulunamadı! Önce 02_embedding_ve_db.py çalıştırılmalı.")
        return

    embedding_function = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    db = Chroma(persist_directory=DB_PATH, embedding_function=embedding_function)
    print(">> Veritabanı Bağlantısı: BAŞARILI")
    print(">> Çıkış yapmak için 'q' tuşuna basın.\n")

    while True:
        user_input = input("SORUNUZU YAZIN: ")
        
        if user_input.lower() == 'q':
            print("Sistem kapatılıyor...")
            break
        
        if not user_input:
            continue

        print("\n... Veritabanı Taranıyor ...")

        results = db.similarity_search(user_input, k=3)
        
        context_text = ""
        for i, doc in enumerate(results):
            context_text += f"KAYNAK {i+1}: {doc.page_content}\n"

        final_prompt = f"""
        Rol: Sen uzman bir doktorsun.
        Görev: Aşağıdaki kaynakları kullanarak hastanın sorusunu yanıtla.
        Kural: Kaynakta bilgi yoksa "Bilmiyorum" de.
        
        --- KAYNAKLAR ---
        {context_text}
        -----------------
        
        SORU: {user_input}
        CEVAP: [Buraya LLM cevabı gelecek]
        """

        print("-" * 40)
        print("SİSTEMİN ÜRETTİĞİ BAĞLAM VE ŞABLON:")
        print(final_prompt)
        print("-" * 40)
        print(">> (Bu şablon LLM'e gönderilmeye hazırdır.)\n")

if __name__ == "__main__":
    main()