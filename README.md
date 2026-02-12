# Ailevi Akdeniz Ateşi (FMF) Klinik Karar Destek Sistemi

**Geliştirici:** Melih Demirci

**Tarih:** Şubat 2026

**Konsept:** Sisoft Staj Programı Projesi

Bu proje, Ailevi Akdeniz Ateşi (FMF) hastalığına özel klinik rehber verilerini kullanarak, sağlık profesyonelleri ve hastalar için geliştirilmiş yapay zeka destekli bir Klinik Karar Destek Sistemidir.

Proje, RAG (Retrieval-Augmented Generation) mimarisini temel almaktadır. Klasik yapay zeka modellerinin aksine, cevaplar modelin eğitim verisinden değil, yerel bir vektör veritabanında tutulan güncel tıbbi rehberlerden referans alınarak üretilir. "Local-First" (Önce Yerel) prensibiyle çalıştığı için veri gizliliğini esas alır ve internet bağlantısına ihtiyaç duymadan çalışabilir.

## Proje Klasör Yapısı

Proje, geliştirme sürecine göre modüler bir yapıda organize edilmiştir:

```text
Melih_Demirci_Staj_Projesi/
│
├── 2.Hafta_RAG_Backend/          # ARKA PLAN (RAG Motoru ve Veri İşleme)
│   ├── 01_veri_ve_chunking_test.py
│   ├── 02_embedding_ve_db.py
│   ├── 03_sorgulama_testi.py
│   ├── 04_prompt_tasarimi.py
│   ├── 05_final_prototip.py
│   └── data_source/              # Genişletilmiş Tıbbi ve Yaşam Rehberleri
│
├── 3.Hafta_RAG_Frontend/         # ARAYÜZ (Streamlit, Hafıza ve Güvenlik)
│   ├── 01_arayuz_tasarimi.py     # ANA UYGULAMA (Giriş)
│   ├── 02_rag_entegrasyonu.py    # ANA UYGULAMA (Geliştirme)
│   ├── 03_hafiza_entegrasyonu.py # ANA UYGULAMA (v3.0 Final Kod)
│   ├── fix_and_update.py         # Veritabanı Onarım ve Güncelleme Scripti
│   └── requirements.txt          # Gerekli Kütüphaneler
│
└── README.md                     # Proje Dokümantasyonu

```

## Kurulum ve Çalıştırma

### 1. Gereksinimlerin Yüklenmesi

```bash
pip install -r 3.Hafta_RAG_Frontend/requirements.txt

```

### 2. Veritabanının Oluşturulması

```bash
python 3.Hafta_RAG_Frontend/fix_and_update.py

```

*(Bu işlem data_source içindeki metinleri okur, parçalar ve ChromaDB'ye kaydeder.)*

### 3. Uygulamanın Başlatılması

```bash
streamlit run 3.Hafta_RAG_Frontend/03_hafiza_entegrasyonu.py

```

## Geliştirme Süreci ve Modüller

### Hafta 2: RAG Mimarisi ve Backend (Arka Plan)

Bu aşamada doküman tabanlı soru-cevap sisteminin mantıksal motoru inşa edilmiştir.

* **01_veri_ve_chunking_test.py:** Ham metinlerin okunması ve anlamlı parçalara ayrılması.
* **02_embedding_ve_db.py:** Metinlerin sayısal vektörlere dönüştürülüp ChromaDB'ye kaydedilmesi.
* **03_sorgulama_testi.py:** Veritabanı üzerinde semantik (anlamsal) arama testleri.
* **04_prompt_tasarimi.py:** LLM için bağlam içeren dinamik prompt yapılarının kurgulanması.
* **05_final_prototip.py:** Terminal tabanlı çalışan ilk fonksiyonel prototip.

### Hafta 3: Frontend, Güvenlik ve Yaşam Rehberi Entegrasyonu

Arka plan motoru, kullanıcı dostu bir arayüze ve genişletilmiş veri setine entegre edilmiştir.

* **Modern Web Arayüzü:** Streamlit ve profesyonel CSS tasarımı ile kullanıcı paneli geliştirilmiştir.
* **Sohbet Hafızası (Session Memory):** Asistanın geçmiş konuşmaları hatırlaması sağlanmıştır.
* **Hibrit Güvenlik (Guardrails):** **Keyword Filter** ve **Fuzzy Matching** ile konu dışı sorular engellenmiş, yazım hataları tolere edilmiştir.
* **Veri Mühendisliği ve Optimizasyon:** * **Genişletilmiş Kapsam:** Klinik verilere ek olarak; Beslenme (Diyet), Spor, Psikolojik Stres Yönetimi, Eğitim ve Askerlik Mevzuatı modülleri entegre edilmiştir.
* **Semantik İzolasyon (Chunk Isolation):** Farklı konuların anlamsal olarak karışmaması için optimize edilmiş parça boyutu (Chunk Size: 400-600) ve özel paragraf ayrıştırma teknikleri uygulanmıştır.



## Kullanılan Teknolojiler

| Teknoloji | Amaç |
| --- | --- |
| **Python** | Ana programlama dili |
| **Streamlit** | Web arayüzü ve ön yüz geliştirme |
| **LangChain** | RAG akış yönetimi ve doküman işleme |
| **ChromaDB** | Vektör verilerinin yerel olarak saklanması |
| **HuggingFace** | `all-MiniLM-L6-v2` embedding modeli |
| **Difflib** | Yazım hataları için bulanık eşleşme algoritması |
| **Metadata Atıf Sistemi** | Yanıtların hangi dökümandan alındığını gösteren referans mekanizması |
| **RecursiveCharacterTextSplitter** | Konu bütünlüğünü koruyan akıllı metin parçalama stratejisi |

## Notlar

* **Veri Gizliliği:** Tüm veriler `chroma_db_storage` klasöründe yerel olarak tutulur, dış servislerle veri paylaşımı yapılmaz.
* **Kaynak Atıf Sistemi:** Sistem, her bilginin kaynağını (dosya adı ve bölüm) yanıt içerisinde kullanıcıya raporlayarak şeffaflık sunar.
* **Sorumluluk Reddi:** Sistem bir klinik karar destek aracıdır. Üretilen yanıtlar tıbbi tavsiye niteliğinde olmayıp, profesyonel hekim görüşünün yerine geçemez.
