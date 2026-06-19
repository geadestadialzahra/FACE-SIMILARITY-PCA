[README.md](https://github.com/user-attachments/files/29121497/README.md)
# Deteksi Kemiripan Wajah dengan PCA (Eigenfaces)

Aplikasi berbasis web untuk mendeteksi kemiripan antara dua wajah menggunakan metode Principal Component Analysis (PCA) atau yang lebih dikenal sebagai **Eigenfaces**.

---

## 📖 Deskripsi Proyek

Proyek ini dibuat untuk memenuhi tugas mata kuliah [Aljabar_Linear]. Aplikasi ini memungkinkan pengguna untuk:

1. Mengunggah **dataset wajah** (minimal 5 gambar) sebagai data latih.
2. Mengunggah **dua gambar wajah** yang akan dibandingkan.
3. Mendapatkan **skor kemiripan** (Cosine Similarity) antara 0% – 100%.
4. Mengetahui **kesimpulan otomatis** (Mirip / Cukup Mirip / Tidak Mirip).
5. Melihat **Kurva Akumulasi Informasi PCA** (grafik varians).

---

## ✨ Fitur Unggulan

- Upload data latih langsung di sidebar.
- Tampilan modern dengan **card** dan **warna profesional**.
- Grafik interaktif menggunakan **Matplotlib**.
- **Animasi loading** dan progress bar.
- **Responsif** (bisa diakses dari HP, tablet, atau laptop).
- Kesimpulan dilengkapi dengan **balon animasi** jika wajah mirip.

---

## 🛠️ Teknologi yang Digunakan

| Teknologi | Kegunaan |
|-----------|----------|
| **Python 3.8+** | Bahasa pemrograman utama |
| **Streamlit** | Membangun antarmuka web |
| **OpenCV & PIL** | Membaca, mengubah grayscale, dan resize gambar |
| **Scikit-learn** | Implementasi PCA dan Cosine Similarity |
| **Matplotlib** | Membuat grafik akumulasi varians |
| **GitHub** | Menyimpan kode secara online |
| **Streamlit Cloud** | Men-deploy aplikasi ke internet |

---

## 🚀 Cara Menjalankan di Lokal (Localhost)

Ikuti langkah-langkah berikut jika ingin menjalankan aplikasi di komputer sendiri:

1. **Clone repositori** ini ke laptop:
   ```bash
   git clone https://github.com/luunaaamiiii/FACE-SIMILARITY-PCA
