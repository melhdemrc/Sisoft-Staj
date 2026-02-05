
# Ailevi Akdeniz Ateşi (FMF) Klinik Karar Destek Sistemi

**Geliştirici:** Melih Demirci  
**Tarih:** Şubat 2026  
**Konsept:** Sisoft Staj Programı Projesi

Bu proje, Ailevi Akdeniz Ateşi (FMF) hastalığına özel klinik rehber verilerini kullanarak, sağlık profesyonelleri ve hastalar için geliştirilmiş yapay zeka destekli bir Klinik Karar Destek Sistemidir.

Proje, RAG (Retrieval-Augmented Generation) mimarisini temel almaktadır. Klasik yapay zeka modellerinin aksine, cevaplar modelin eğitim verisinden değil, yerel bir vektör veritabanında tutulan güncel tıbbi rehberlerden referans alınarak üretilir. "Local-First" (Önce Yerel) prensibiyle çalıştığı için veri gizliliğini esas alır ve internet bağlantısına ihtiyaç duymadan çalışabilir.

## Proje Klasör Yapısı

Proje, geliştirme sürecine göre modüler bir yapıda organize edilmiştir:

Melih_Demirci_Staj_Projesi/
│
├── 2.Hafta_RAG_Backend/          # ARKA PLAN (RAG Motoru ve Veri İşleme)
│   ├── 01_veri_ve_chunking_test.py
│   ├── 02_embedding_ve_db.py
│   ├── 03_sorgulama_testi.py
│   ├── 04_prompt_tasarimi.py
│   ├── 05_final_prototip.py
│   └── data_source/              # Ham tıbbi metinler
│
├── 3.Hafta_RAG_Frontend/         # ARAYÜZ (Streamlit, Hafıza ve Güvenlik)
│   ├── 03_hafiza_entegrasyonu.py # ANA UYGULAMA (Final Kod)
│   ├── fix_and_update.py         # Veritabanı Onarım Aracı
│   └── requirements.txt          # Gerekli Kütüphaneler
│
└── README.md                     # Proje Dokümantasyonu


## Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

### 1. Gereksinimlerin Yüklenmesi

Projenin çalışması için gerekli Python kütüphanelerini yükleyin:

```bash
pip install -r 3.Hafta_RAG_Frontend/requirements.txt

```

### 2. Veritabanının Oluşturulması

Vektör veritabanını sıfırdan kurmak veya güncellemek için onarım scriptini çalıştırın:

```bash
cd 3.Hafta_RAG_Frontend
python fix_and_update.py

```

*(Bu işlem data_source içindeki metinleri okur, parçalar ve ChromaDB'ye kaydeder.)*

### 3. Uygulamanın Başlatılması

Arayüzü çalıştırmak için Streamlit komutunu kullanın:

```bash
streamlit run 03_hafiza_entegrasyonu.py

```

## Geliştirme Süreci ve Modüller

Proje iki ana fazda geliştirilmiştir:

### Hafta 2: RAG Mimarisi ve Backend (Arka Plan)

Bu aşamada doküman tabanlı soru-cevap sisteminin mantıksal motoru inşa edilmiştir.

* **01_veri_ve_chunking_test.py:** Ham tıbbi metinlerin okunması ve yapay zeka için anlamlı küçük parçalara (chunking) ayrılması.
* **02_embedding_ve_db.py:** Metin parçalarının sayısal vektörlere (embedding) dönüştürülmesi ve ChromaDB vektör veritabanına kaydedilmesi.
* **03_sorgulama_testi.py:** Veritabanı üzerinde semantik (anlamsal) arama testlerinin yapılması.
* **04_prompt_tasarimi.py:** LLM (Büyük Dil Modeli) için bağlam (context) içeren dinamik prompt yapılarının kurgulanması.
* **05_final_prototip.py:** Terminal tabanlı çalışan ilk prototip.

### Hafta 3: Frontend, Güvenlik ve Hafıza (Arayüz)

Arka planda çalışan motor, kullanıcı dostu bir web arayüzüne entegre edilmiş ve akıllı özelliklerle donatılmıştır.

* **Modern Web Arayüzü:** Streamlit kullanılarak geliştirilen, profesyonel CSS tasarımına sahip kullanıcı paneli.
* **Sohbet Hafızası (Session Memory):** Asistanın geçmiş konuşmaları hatırlamasını sağlayan durum yönetimi.
* **Hibrit Güvenlik (Guardrails):**
* **Keyword Filter:** Tıbbi olmayan soruları (Örn: "Araba fiyatları") kelime köküne bakarak engeller.
* **Fuzzy Matching:** Kullanıcı yazım hatalarını (Örn: "Kolsisin") tolere eder ve düzeltir.


* **Performans Optimizasyonu:** `@st.cache_resource` ile modelin sadece bir kez yüklenmesi sağlanarak sorgu hızı artırılmıştır.

## Kullanılan Teknolojiler

| Teknoloji | Amaç |
| --- | --- |
| **Python** | Ana programlama dili |
| **Streamlit** | Web arayüzü ve ön yüz geliştirme |
| **LangChain** | RAG akış yönetimi ve doküman işleme |
| **ChromaDB** | Vektör verilerinin yerel olarak saklanması |
| **HuggingFace** | `sentence-transformers/all-MiniLM-L6-v2` embedding modeli |
| **Difflib** | Yazım hataları için bulanık eşleşme algoritması |

## Notlar

* **Veri Gizliliği:** Tüm veriler `chroma_db_storage` klasöründe yerel olarak tutulur, buluta veri gönderilmez.
* **Kapsam:** Sistem sadece yüklenen FMF Klinik Rehberi kapsamındaki sorulara yanıt verir. Kapsam dışı sorular güvenlik duvarına takılır.

```

```
