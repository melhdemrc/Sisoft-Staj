import os
import shutil
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma

DATA_PATH = "data_source/fmf_tedavi_rehberi.txt"
DB_PATH = "chroma_db_storage"

def main():
    print("=== VERİTABANI GÜNCELLEME BAŞLATILDI ===")

    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)
        print(">> Eski veritabanı silindi.")

    print(">> Yeni metin dosyası okunuyor...")
    loader = TextLoader(DATA_PATH, encoding="utf-8")
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400, 
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    splits = text_splitter.split_documents(docs)
    print(f">> Metin {len(splits)} parçaya bölündü.")

    print(">> Vektör veritabanı oluşturuluyor (Bu işlem birkaç saniye sürebilir)...")
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    Chroma.from_documents(
        documents=splits,
        embedding=embedding_function,
        persist_directory=DB_PATH
    )
    print(">> BAŞARILI! Veritabanı güncellendi.")

if __name__ == "__main__":
    main()