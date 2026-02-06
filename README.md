# RAG Uygulamaları - Hafta 2

Bu proje, Sisoft staj programının ikinci haftası kapsamında geliştirilen, doküman tabanlı bir soru-cevap (RAG - Retrieval-Augmented Generation) sistemidir. Proje, yerel veri kaynaklarını kullanarak anlamlı metin parçalama, vektör veri tabanı oluşturma ve bağlama dayalı yanıt üretme süreçlerini kapsamaktadır.

## Proje Yapısı

Proje, iş akışına göre sıralanmış beş ana modülden oluşmaktadır:

1. **01_veri_ve_chunking_test.py**: Veri kaynaklarının okunması ve metinlerin işlenebilir parçalara (chunking) ayrılması.
2. **02_embedding_ve_db.py**: Metin parçalarının vektörlere dönüştürülmesi ve ChromaDB üzerine kaydedilmesi.
3. **03_sorgulama_testi.py**: Vektör veri tabanı üzerinde semantik arama testlerinin yapılması.
4. **04_prompt_tasarimi.py**: LLM için bağlam (context) içeren dinamik prompt yapısının oluşturulması.
5. **05_final_prototip.py**: Tüm sürecin birleştirildiği interaktif sağlık asistanı simülasyonu.

## Kurulum

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları takip edebilirsiniz:

1. Python ortamını hazırlayın ve bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

2. Vektör veri tabanını oluşturun:
   ```bash
   python 02_embedding_ve_db.py
   ```

3. Final prototipini başlatın:
   ```bash
   python 05_final_prototip.py
   ```

## Kullanılan Teknolojiler

* **LangChain**: RAG iş akışının yönetimi ve doküman işleme.
* **ChromaDB**: Vektör verilerinin depolanması ve hızlı erişim.
* **HuggingFace**: Cümlelerin vektör temsillerine dönüştürülmesi (sentence-transformers/all-MiniLM-L6-v2).

## Notlar

* Verilerin saklandığı yerel dizin: `chroma_db_storage`
* Test sonuçları ve loglar: `test_results`