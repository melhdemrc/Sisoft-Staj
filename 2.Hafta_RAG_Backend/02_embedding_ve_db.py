import os
import shutil
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DATA_PATH = "data_source/fmf_tedavi_rehberi.txt"
DB_PATH = "chroma_db_storage"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def create_vector_db():
    print("--- 1. VERİ YÜKLENİYOR ---")
    if not os.path.exists(DATA_PATH):
        print(f"[HATA] Veri dosyası bulunamadı: {DATA_PATH}")
        print("Lütfen önce 01_veri_ve_chunking_test.py dosyasını çalıştırın.")
        return

    loader = TextLoader(DATA_PATH, encoding="utf-8")
    documents = loader.load()
    print(f"   -> Dosya yüklendi. Karakter sayısı: {len(documents[0].page_content)}")

    print("\n--- 2. PARÇALAMA (CHUNKING) ---")
    splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    print(f"   -> Metin {len(chunks)} parçaya ayrıldı.")
    print(f"   -> Örnek Parça: {chunks[1].page_content}")

    print("\n--- 3. VEKTÖRLEŞTİRME VE KAYIT (EMBEDDING) ---")
    print(f"   -> Model yükleniyor: {MODEL_NAME} (İlk seferde indirmesi zaman alabilir...)")
    
    embedding_function = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)
        print("   -> Eski veritabanı temizlendi.")

    print("   -> Veriler vektörlere dönüştürülüp ChromaDB'ye yazılıyor...")
    db = Chroma.from_documents(
        documents=chunks, 
        embedding=embedding_function, 
        persist_directory=DB_PATH
    )
    
    print(f"BAŞARILI! Veritabanı '{DB_PATH}' klasörüne kaydedildi.")

if __name__ == "__main__":
    create_vector_db()