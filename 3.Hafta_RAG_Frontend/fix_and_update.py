import os
import shutil
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
DATA_FOLDER = os.path.join(parent_dir, "2.Hafta_RAG_Backend", "data_source")
DB_PATH = os.path.join(parent_dir, "2.Hafta_RAG_Backend", "chroma_db_storage")

def main():
    print("=== KAPSAMLI VERİTABANI GÜNCELLEMESİ ===")
    
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)
        print(">> Eski veritabanı temizlendi.")
    all_documents = []
    if not os.path.exists(DATA_FOLDER):
        print("HATA: Veri klasörü bulunamadı.")
        return

    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith(".txt"):
            file_path = os.path.join(DATA_FOLDER, filename)
            print(f">> Okunuyor: {filename}")
            loader = TextLoader(file_path, encoding="utf-8")
            all_documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,  
        chunk_overlap=100,
        separators=["\n\n", "\n", "BÖLÜM", ". "] 
    )
    splits = text_splitter.split_documents(all_documents)
    print(f">> Toplam {len(splits)} bilgi parçacığı oluşturuldu.")

    print(">> Yapay zeka öğreniyor (Embedding)...")
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    Chroma.from_documents(
        documents=splits,
        embedding=embedding_function,
        persist_directory=DB_PATH
    )
    print(">>SİSTEM HAZIR! Artık çok daha fazla soruya cevap verebilir.")

if __name__ == "__main__":
    main()