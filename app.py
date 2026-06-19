# app.py
# =====================================================
# APLIKASI DETEKSI KEMIRIPAN WAJAH DENGAN PCA (EIGENFACES)
# =====================================================

import streamlit as st
import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from PIL import Image
import time

# ==========================================
# 1. PENGATURAN HALAMAN & CSS (Biar Cantik)
# ==========================================
st.set_page_config(
    page_title="PCA Face Similarity",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS KUSTOM ---
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #1E3A8A;
            font-size: 42px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .sub-title {
            text-align: center;
            color: #6B7280;
            font-size: 18px;
            margin-bottom: 30px;
        }
        .result-card {
            background-color: #F3F4F6;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            text-align: center;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stButton button {
            background-color: #1E3A8A;
            color: white;
            font-size: 18px;
            border-radius: 12px;
            padding: 10px 30px;
            width: 100%;
        }
        .stButton button:hover {
            background-color: #2563EB;
            color: white;
        }
        h1, h2, h3 {
            color: #1E3A8A;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. JUDUL
# ==========================================
st.markdown('<p class="main-title">🧠 Deteksi Kemiripan Wajah</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Menggunakan Metode PCA (Eigenfaces) & Cosine Similarity</p>', unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR: UPLOAD DATA LATIH
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.header("📂 Step 1: Data Latih")
    st.markdown("Upload **minimal 5 foto** wajah. <br> (Usahakan 2 orang berbeda, masing-masing 3+ foto)", unsafe_allow_html=True)

    uploaded_train_files = st.file_uploader(
        "Pilih Foto Latih",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="train"
    )

    if uploaded_train_files:
        st.success(f"✅ {len(uploaded_train_files)} foto berhasil diupload!")
    else:
        st.warning("⬆️ Upload foto di sini")

    st.divider()
    st.caption("📌 Dibuat dengan ❤️ oleh Kelompok PCA")

# ==========================================
# 4. AREA UTAMA: UPLOAD 2 FOTO UJI
# ==========================================
st.header("🔍 Step 2: Upload Dua Wajah yang Ingin Dibandingkan")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("#### 📸 Foto Pertama")
    face1_file = st.file_uploader("Upload Foto 1", type=["jpg", "jpeg", "png"], key="face1", label_visibility="collapsed")

with col2:
    st.markdown("#### 📸 Foto Kedua")
    face2_file = st.file_uploader("Upload Foto 2", type=["jpg", "jpeg", "png"], key="face2", label_visibility="collapsed")

# ==========================================
# 5. TOMBOL PROSES
# ==========================================
st.markdown("---")
col_button, _ = st.columns([1, 3])
with col_button:
    proses_button = st.button("🚀 Proses Deteksi Sekarang", use_container_width=True)

# ==========================================
# 6. LOGIKA PEMROSESAN
# ==========================================
if proses_button:
    if not uploaded_train_files or len(uploaded_train_files) < 5:
        st.error("⚠️ **Data Latih Kurang!** Upload minimal 5 gambar wajah terlebih dahulu di sidebar.")
    elif not face1_file or not face2_file:
        st.error("⚠️ **Foto Uji Kurang!** Upload kedua foto yang akan dibandingkan.")
    else:
        with st.spinner("⏳ Sedang memproses... Mohon tunggu, ini butuh beberapa detik."):
            time.sleep(0.5)

            # --- A. Preprocessing Data Latih ---
            IMG_SIZE = (100, 100)
            X_train = []

            progress_bar = st.progress(0, text="Mengolah data latih...")
            for i, file in enumerate(uploaded_train_files):
                img = Image.open(file).convert('L')
                img = img.resize(IMG_SIZE)
                vector = np.array(img).flatten() / 255.0
                X_train.append(vector)
                progress_bar.progress((i + 1) / len(uploaded_train_files))

            X_train = np.array(X_train)

            # --- B. Jalankan PCA ---
            progress_bar.progress(50, text="Menjalankan PCA & mencari Eigenfaces...")
            k = min(50, len(X_train) - 1) if len(X_train) > 1 else 1
            pca = PCA(n_components=k)
            X_pca = pca.fit_transform(X_train)

            # --- C. Proses Foto Uji ---
            progress_bar.progress(70, text="Memproses foto uji...")

            def load_and_process(uploaded_file):
                img = Image.open(uploaded_file).convert('L')
                img = img.resize(IMG_SIZE)
                return np.array(img).flatten() / 255.0

            vec1 = load_and_process(face1_file)
            vec2 = load_and_process(face2_file)

            proj1 = pca.transform([vec1])
            proj2 = pca.transform([vec2])

            similarity = cosine_similarity(proj1, proj2)[0][0]

            progress_bar.progress(100, text="Selesai!")
            time.sleep(0.3)
            progress_bar.empty()

            # ==========================================
            # 7. TAMPILKAN HASIL
            # ==========================================
            st.markdown("---")
            st.subheader("📊 Hasil Deteksi")

            col_res1, col_res2, col_res3 = st.columns(3, gap="medium")

            with col_res1:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.image(face1_file, width=180, caption="Foto 1")
                st.markdown('</div>', unsafe_allow_html=True)

            with col_res2:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.image(face2_file, width=180, caption="Foto 2")
                st.markdown('</div>', unsafe_allow_html=True)

            with col_res3:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.metric(label="Skor Kemiripan", value=f"{similarity:.2%}", delta=None)

                if similarity >= 0.70:
                    st.success(" **Kesimpulan: MIRIP**")
                    st.markdown("*(Kemungkinan besar orang yang sama)*")
                    st.balloons()
                elif similarity >= 0.50:
                    st.warning(" **Kesimpulan: CUKUP MIRIP**")
                    st.markdown("*(Perlu verifikasi tambahan)*")
                else:
                    st.error(" **Kesimpulan: TIDAK MIRIP**")
                    st.markdown("*(Kemungkinan besar orang berbeda)*")

                st.caption(f"Jumlah Komponen PCA: {k}")
                st.caption(f"Varians data: {np.sum(pca.explained_variance_ratio_)*100:.1f}%")
                st.markdown('</div>', unsafe_allow_html=True)

            # --- Grafik PCA ---
            st.subheader(" Grafik Akumulasi Informasi PCA")
            explained_variance = np.cumsum(pca.explained_variance_ratio_)

            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(range(1, len(explained_variance)+1), explained_variance, 'bo-', linewidth=2, markersize=6)
            ax.axhline(y=0.95, color='red', linestyle='--', linewidth=2, label='95% Varians')
            ax.set_xlabel('Jumlah Komponen PCA (k)', fontsize=12)
            ax.set_ylabel('Akumulasi Informasi', fontsize=12)
            ax.set_title('Kurva Akumulasi Informasi PCA', fontsize=14)
            ax.grid(True, alpha=0.3)
            ax.legend(loc='lower right')
            ax.set_ylim(0, 1.05)
            st.pyplot(fig)