# 🌸 ANGEL – Aplikasi PCA untuk Grayscale, Kompresi, & Deteksi Kemiripan Wajah

Aplikasi berbasis web untuk mengolah gambar menggunakan **Principal Component Analysis (PCA)**.  
Dibangun dengan **Streamlit** dan dikembangkan oleh **Kelompok 2 – Mahasiswa Sarjana Teknik Informatika Universitas Negeri Semarang**.

---

## ✨ Fitur Unggulan

- **🌫️ Grayscale** – Mengubah gambar berwarna menjadi hitam-putih (grayscale) untuk efek artistik dan penghematan ukuran file.

- **🗜️ Kompresi PCA** – Mereduksi dimensi gambar menggunakan PCA pada setiap kanal warna (R, G, B) secara terpisah. Menampilkan metrik kualitas seperti SSIM, PSNR, rasio kompresi, serta kurva akumulasi informasi PCA.

- **🔍 Deteksi Kemiripan Wajah** – Membandingkan dua gambar wajah menggunakan metode Eigenfaces (PCA) dan Cosine Similarity. Menampilkan skor kemiripan dalam persen, kesimpulan (Mirip / Cukup Mirip / Tidak Mirip), dan grafik akumulasi informasi.

---

## 🛠️ Teknologi yang Digunakan

- **Python 3.8+** – Bahasa pemrograman utama.
- **Streamlit 1.28+** – Framework untuk membangun antarmuka web secara cepat.
- **OpenCV 4.8+** – Digunakan untuk pemrosesan gambar dan deteksi wajah (Haar Cascade).
- **Scikit-learn 1.3+** – Implementasi PCA dan Cosine Similarity.
- **Scikit-image 0.21+** – Menghitung metrik kualitas SSIM dan PSNR.
- **Matplotlib 3.7+** – Membuat grafik akumulasi informasi PCA.
- **Pillow 10.0+** – Manipulasi gambar dasar (membuka, menyimpan, resize).

---

## 📁 Struktur File
project:  
├── app.py # File utama aplikasi (semua fitur dalam satu file)  
├── requirements.txt # Daftar library yang dibutuhkan  
├── README.md # Dokumentasi proyek (file ini)  
└── logo-kelompok.PNG # Logo kelompok (ditampilkan di sidebar)

---

## 🚀 Cara Menjalankan di Lokal

1. **Clone repositori** ini ke komputer kamu: git clone https://github.com/luunaamiiii/FACE-SIMILARITY-PCA.git
cd FACE-SIMILARITY-PCA
2. **Install semua library** yang dibutuhkan: pip install -r requirements.txt
3. **Jalankan aplikasi Streamlit**: streamlit run app.py
4. Buka browser dan akses `http://localhost:8501`.

---

## 👥 Anggota Kelompok

- **Gea Destadia Al-Zahra**
- **Luna Amilia**
- **Dalilah Arifah Ariandi DJR**
- **Nadia Azzizah**

**Universitas Negeri Semarang** – Teknik Informatika

---

## 📌 Catatan Penting

- **Koneksi internet** diperlukan saat pertama kali membuka halaman Deteksi untuk mengunduh dataset LFW (Labeled Faces in the Wild) sebagai data latih default. Proses ini hanya terjadi sekali.
- Pastikan file **`logo-kelompok.PNG`** berada di folder yang sama dengan `app.py`, karena digunakan sebagai logo di sidebar.
- Untuk hasil terbaik di halaman Deteksi Kemiripan, gunakan foto wajah yang **jelas, tidak menggunakan filter, dan tidak berekspresi berlebihan**.

---

## 🔗 Link Aplikasi

- **Streamlit Cloud**: [https://face-similarity-pca-xxxxxx.streamlit.app](https://face-similarity-pca-xxxxxx.streamlit.app)
- **GitHub**: [https://github.com/luunaamiiii/FACE-SIMILARITY-PCA](https://github.com/luunaamiiii/FACE-SIMILARITY-PCA)

---

## 📞 Kontak
**Gea Destadia Al-Zahra**  
IG = @gea_destadia_10  
WA = 0831-5068-7481

**Luna Amilia**  
IG = @luunaaamiiii  
Email = lunaamilia0@gmail.com

**Nadia Azizah**  
IG = @ndyyzh  
WA = 0858-4631-3309

**Dalilah Arifah Ariandi DJR**  
IG = @adellianav  
WA = 0813-1211-6787

---

**🌸 Made with Love by Team ANGEL**  
*Teknologi untuk kreativitas tanpa batas.*
