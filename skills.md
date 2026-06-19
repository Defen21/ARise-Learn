# 🧬 Panduan Kompetensi (Skills) & Validasi Output Materi — ARise Learn

Dokumen ini berfungsi sebagai panduan standar (*standard operating procedure* / guidelines) untuk memastikan bahwa materi pembelajaran, model 3D, penjelasan AI, dan rekomendasi topik berikutnya yang dihasilkan oleh platform **ARise Learn** memenuhi dua kriteria utama:
1. **Mudah Dipahami (Accessible & Clear)**: Menggunakan bahasa yang ramah siswa, analogi yang relevan, dan struktur yang teratur.
2. **Pasti Valid (Accurate & Grounded)**: Terikat langsung pada kurikulum resmi dan divalidasi dengan basis data RAG (*Retrieval-Augmented Generation*) untuk menghindari halusinasi AI.

---

## 🎯 1. Prinsip Penyederhanaan Materi (Easy to Understand)

Untuk memastikan materi sains yang kompleks (seperti mekanika kuantum, genetika, kardiologi) dapat dipahami dengan mudah oleh siswa sekolah menengah, setiap output penjelasan AI wajib mengikuti prinsip berikut:

### 💡 A. Penggunaan Analogi Kehidupan Sehari-hari
LLM harus memetakan konsep abstrak ke objek konkret yang sudah dikenal siswa:
* **Sel/Atom**: Seperti pabrik atau sistem tata surya mini.
* **DNA**: Cetak biru (*blueprint*) pembangunan rumah, atau resep memasak raksasa.
* **Jantung**: Pompa air otomatis di rumah yang bekerja tanpa henti.
* **Molekul H2O**: Magnet kecil yang saling tarik-menarik (kutub positif & negatif).

### 📐 B. Struktur Penjelasan Berjenjang (Hierarchy)
Jangan menyajikan teks dalam satu blok paragraf besar. Gunakan pemformatan Markdown berikut:
* **Gunakan Bullet Points & Bold Text** untuk menonjolkan kata kunci penting.
* **Pemisah Bagian**: Gunakan sub-header (`###`) untuk membagi anatomi atau sub-topik.
* **Urutan Logis**: Mulai dari definisi umum → cara kerja/fungsi → mengapa hal ini penting dalam kehidupan nyata.

---

## 🛡️ 2. Protokol Validasi Materi (Ensuring Absolute Validity)

Materi yang diajarkan harus bebas dari halusinasi ilmiah. Validasi dilakukan melalui integrasi **RAG (Retrieval-Augmented Generation)** dengan langkah-langkah berikut:

| Tahap Validasi | Mekanisme Teknis | Hasil yang Diharapkan |
| :--- | :--- | :--- |
| **1. Ingesti Data Terpercaya** | Dokumen kurikulum nasional dan buku teks resmi disimpan di **Qdrant Vector Database** dalam bentuk embeddings. | Sumber referensi berakar pada buku teks yang terverifikasi. |
| **2. Semantic Search Query** | AI Service melakukan pencarian vektor berdasarkan input gambar & konteks untuk mengambil kutipan teks asli dari basis data. | Mendapatkan teks referensi kurikulum yang memiliki kemiripan semantik tertinggi. |
| **3. Grounded Generation** | Prompt LLM diinstruksikan untuk *hanya* menjelaskan topik berdasarkan konteks referensi yang diberikan. | Mencegah AI mengarang istilah atau fakta baru di luar buku teks resmi. |
| **4. Confidence & RAG Score** | Sistem menghitung skor kecocokan (*match rate*) antara hasil analisis dan teks dasar kurikulum. | Tampilan indikator persentase validasi (misal: "94% Match") di UI. |

> [!IMPORTANT]
> Jika database RAG sedang offline, sistem memiliki mekanisme *Strict Fallback System* yang mengunci prompt LLM agar hanya menggunakan konsep sains mendasar yang diakui secara global (seperti standar IUPAC untuk kimia, atau model standar atom Bohr).

---

## 🗺️ 3. Pemetaan Kompetensi (Skills) & Peta Jalur Belajar (Learning Paths)

Berikut adalah standar pemetaan kompetensi yang diperoleh siswa dari setiap topik di katalog ARise Learn, serta rekomendasi materi berikutnya yang paling efektif:

### 1. ❤️ Anatomi Jantung Manusia (Human Heart)
* **Kompetensi Utama yang Diperoleh (Skills)**:
  * Mengidentifikasi struktur ruang jantung (atrium, ventrikel) dan pembuluh darah utama (aorta).
  * Memahami perbedaan antara sirkulasi darah besar (sistemik) dan sirkulasi darah kecil (pulmonal).
  * Menjelaskan kerja katup jantung dalam mencegah arus balik darah (*regurgitasi*).
* **Rekomendasi Jalur Belajar Terkait**:
  1. **Sistem Transportasi Darah (Sangat Relevan)**: Mempelajari sel darah merah, sel darah putih, plasma, dan fungsinya dalam pertukaran oksigen.
  2. **Tekanan Darah & Jantung (Relevan)**: Memahami konsep sistol, diastol, dan faktor yang memengaruhi tekanan darah manusia.
  3. **Penyakit Sistem Kardiovaskular (Relevan)**: Mempelajari gangguan seperti hipertensi, serangan jantung, dan aterosklerosis.

### 2. 🧬 Struktur Heliks Ganda DNA (DNA Double Helix)
* **Kompetensi Utama yang Diperoleh (Skills)**:
  * Memahami struktur nukleotida (gula deoksiribosa, gugus fosfat, basa nitrogen).
  * Menerapkan aturan pasangan basa nitrogen komplementer Chargaff (Adenin-Timin, Sitosin-Guanin).
  * Menjelaskan ikatan hidrogen yang menstabilkan rantai ganda DNA.
* **Rekomendasi Jalur Belajar Terkait**:
  1. **Replikasi DNA (Sangat Relevan)**: Bagaimana sel menduplikasi informasi genetiknya sebelum membelah.
  2. **Sintesis Protein / Transkripsi (Relevan)**: Langkah menerjemahkan kode DNA menjadi rantai RNA dan protein.
  3. **Mutasi Genetik (Relevan)**: Memahami bagaimana kesalahan pembacaan basa nitrogen memicu variasi genetik atau penyakit bawaan.

### 3. 💧 Geometri Molekul H₂O (Water Molecule)
* **Kompetensi Utama yang Diperoleh (Skills)**:
  * Memahami geometri molekul bentuk V (sudut ikatan 104.5°) akibat adanya pasangan elektron bebas (PEB).
  * Mengidentifikasi polaritas molekul air yang disebabkan oleh perbedaan elektronegativitas antara Oksigen dan Hidrogen.
  * Menjelaskan pembentukan ikatan hidrogen antarmolekul air.
* **Rekomendasi Jalur Belajar Terkait**:
  1. **Gaya Antarmolekul (Sangat Relevan)**: Mengapa air memiliki titik didih yang tinggi dibandingkan molekul sejenis (seperti H2S).
  2. **Sifat Koligatif Larutan (Relevan)**: Bagaimana zat terlarut memengaruhi titik beku dan titik didih pelarut air.
  3. **Ikatan Kimia Dasar (Relevan)**: Membandingkan ikatan kovalen polar pada H2O dengan ikatan ionik atau kovalen nonpolar.

### 4. ⚛️ Model Atom Bohr (Bohr Model)
* **Kompetensi Utama yang Diperoleh (Skills)**:
  * Menjelaskan struktur dasar atom (proton dan neutron di inti, elektron di kulit atom).
  * Memahami kuantisasi energi elektron pada lintasan orbit stasioner tertentu.
  * Menjelaskan fenomena absorbsi dan emisi energi saat elektron berpindah kulit (transisi elektron).
* **Rekomendasi Jalur Belajar Terkait**:
  1. **Konfigurasi Elektron (Sangat Relevan)**: Aturan pengisian elektron pada kulit dan sub-kulit atom (prinsip Aufbau, larangan Pauli).
  2. **Tabel Periodik Unsur (Relevan)**: Bagaimana nomor atom dan konfigurasi elektron menentukan posisi unsur dalam sistem periodik.
  3. **Teori Mekanika Kuantum Modern (Relevan)**: Mengenal konsep orbital elektron (awan probabilitas) yang menyempurnakan model Bohr.

---

## 🛠️ 4. Templat JSON Respons AI untuk Rekomendasi Terstruktur
Untuk menjaga keajekan format rekomendasi materi di tingkat API, LLM harus menghasilkan data rekomendasi yang sesuai dengan skema JSON berikut:

```json
[
  {
    "title": "Nama Materi Rekomendasi",
    "description": "Deskripsi singkat mengenai apa yang akan dipelajari di materi ini dan mengapa ini relevan setelah mempelajari topik saat ini.",
    "relevance": "Sangat Relevan / Relevan",
    "icon_hint": "biology / biotech / chemistry / physics / medical / calculate"
  }
]
```

---
*Dokumen ini merupakan bagian dari standar kualitas akademik sistem pembelajaran interaktif **ARise Learn**.*
