PROJE: FMF KLİNİK KARAR DESTEK SİSTEMİ
GELİŞTİRİCİ: Melih Demirci
TARİH: 05.02.2026

[PROJE HAKKINDA]
Bu proje, Ailevi Akdeniz Ateşi (FMF) hastalığı için geliştirilmiş, 
yapay zeka destekli bir klinik rehber asistanıdır.
RAG (Retrieval-Augmented Generation) mimarisi kullanılarak, 
tıbbi veriler vektör veritabanında saklanmakta ve anlık sorgulanmaktadır.

[KURULUM]
1. Gerekli kütüphaneleri yükleyin:
   pip install -r requirements.txt

2. Veritabanını oluşturun (Eğer yoksa):
   python fix_and_update.py

3. Arayüzü başlatın:
   streamlit run 03_hafiza_entegrasyonu.py

[ÖZELLİKLER]
- Güvenli Yerel Veritabanı (ChromaDB)
- Hibrit Güvenlik Filtresi (Konu dışı soruları engeller)
- Sohbet Hafızası (Session State)
- Profesyonel CSS Arayüzü