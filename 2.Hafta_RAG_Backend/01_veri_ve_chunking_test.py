import os
from datetime import datetime
from langchain_text_splitters import RecursiveCharacterTextSplitter

CONFIG = {
    "data_folder": "data_source",
    "output_folder": "test_results",
    "filename": "fmf_tedavi_rehberi.txt",
    "report_name": "chunking_analiz_raporu.txt",
    "experiments": [
        {"name": "SENARYO_A_MICRO", "chunk_size": 50, "chunk_overlap": 10},
        {"name": "SENARYO_B_OPTIMAL", "chunk_size": 250, "chunk_overlap": 50},
        {"name": "SENARYO_C_MACRO", "chunk_size": 1000, "chunk_overlap": 200}
    ]
}

class RAGPipelineTest:
    def __init__(self):
        self.raw_text = ""
        self.file_path = os.path.join(CONFIG["data_folder"], CONFIG["filename"])
        self.report_path = os.path.join(CONFIG["output_folder"], CONFIG["report_name"])

        os.makedirs(CONFIG["data_folder"], exist_ok=True)
        os.makedirs(CONFIG["output_folder"], exist_ok=True)

    def generate_synthetic_data(self):
        print("[1/3] Veri Seti Oluşturuluyor...")
        self.raw_text = """
AİLEVİ AKDENİZ ATEŞİ (FMF) KLİNİK YÖNETİM REHBERİ - v2026.1

1. KLİNİK TANIMLAMA
Ailevi Akdeniz Ateşi (FMF); tekrarlayan ateş, peritonit, plörit ve artrit ataklarıyla karakterize,
genellikle 12 ile 72 saat süren, otozomal resesif geçişli bir hastalıktır. 
Ülkemizde prevalansı (görülme sıklığı) 1/1000 oranındadır.

2. GENETİK ETİYOLOJİ
Hastalık 16. kromozomdaki MEFV gen mutasyonlarına bağlı gelişir.
En sık saptanan mutasyonlar:
- M694V (En şiddetli seyir ve amiloidoz riski)
- M680I
- V726A

3. TEDAVİ STRATEJİSİ VE İLAÇLAR
Tedavinin altın standardı Kolşisin (Colchicine) molekülüdür.
Kullanım Amacı: Atak sıklığını azaltmak ve sekonder amiloidoz (böbrek yetmezliği) gelişimini önlemektir.

Dozaj Protokolü:
- Yetişkin: Günde 1.5 - 2 mg (İdame doz)
- Çocuk (<5 yaş): Günde 0.5 mg
- Dirençli Vaka: Kolşisin'e yanıt vermeyen hastalarda IL-1 inhibitörleri (Anakinra) başlanmalıdır.

4. ACİL DURUM VE ATAK YÖNETİMİ
Atak başlangıcında Kolşisin dozu ARTIRILMAMALIDIR. Bu yaygın bir yanlıştır.
Ağrı yönetimi için NSAİİ (Non-steroid antiinflamatuar) grubu ilaçlar kullanılabilir.
"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(self.raw_text)
        print(f"   -> Kaydedildi: {self.file_path} ({len(self.raw_text)} karakter)")

    def run_chunking_tests(self):
        print("[2/3] Chunking Testleri Başlatılıyor...")
        results_log = f"=== CHUNKING ANALİZ RAPORU ===\nTarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        for exp in CONFIG["experiments"]:
            print(f"   -> Test Ediliyor: {exp['name']} (Size: {exp['chunk_size']})")
            
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=exp['chunk_size'],
                chunk_overlap=exp['chunk_overlap'],
                separators=["\n\n", "\n", " ", ""]
            )
            chunks = splitter.create_documents([self.raw_text])
            
            results_log += f"--- DENEY: {exp['name']} ---\n"
            results_log += f"Parametreler: Size={exp['chunk_size']} | Overlap={exp['chunk_overlap']}\n"
            results_log += f"Oluşan Parça Sayısı: {len(chunks)}\n"
            
            if len(chunks) > 1:
                sample = chunks[1].page_content.replace("\n", " ")
                results_log += f"Örnek Parça (Index 1): \"{sample[:100]}...\"\n"
            else:
                results_log += "Örnek Parça: Tek parça oluştu.\n"
            results_log += "-"*40 + "\n"

        print("[3/3] Rapor Oluşturuluyor...")
        with open(self.report_path, "w", encoding="utf-8") as f:
            f.write(results_log)
        print(f"   -> Rapor Hazır: {self.report_path}")

if __name__ == "__main__":
    print("--- RAG PAZARTESİ GÖREVİ BAŞLADI ---")
    pipeline = RAGPipelineTest()
    pipeline.generate_synthetic_data()
    pipeline.run_chunking_tests()
    print("--- İŞLEM BAŞARIYLA TAMAMLANDI ---")