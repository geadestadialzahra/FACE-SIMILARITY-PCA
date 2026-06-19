# app.py - VERSI FINAL DENGAN TEMA PINK & TOMBOL SAKURA
# =====================================================
# APLIKASI DETEKSI KEMIRIPAN WAJAH DENGAN PCA (EIGENFACES)
# =====================================================

import streamlit as st
import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import time

# ==========================================
# 1. PENGATURAN HALAMAN & CSS (TEMA PINK SOFT)
# ==========================================
st.set_page_config(
    page_title="PCA Face Similarity",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS KUSTOM (PINK SOFT) ---
st.markdown("""
    <style>
        /* Warna utama pink soft */
        .main-title {
            text-align: center;
            color: #AD1457;
            font-size: 42px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .sub-title {
            text-align: center;
            color: #D81B60;
            font-size: 18px;
            margin-bottom: 30px;
        }
        .result-card {
            background-color: #FCE4EC;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            text-align: center;
            border: 1px solid #F8BBD0;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Tombol pink */
        .stButton button {
            background-color: #EC407A;
            color: white;
            font-size: 18px;
            border-radius: 12px;
            padding: 10px 30px;
            width: 100%;
            border: none;
            transition: 0.3s;
        }
        .stButton button:hover {
            background-color: #D81B60;
            color: white;
            transform: scale(1.02);
        }
        
        /* Sidebar background pink soft */
        .css-1d391kg, .css-12w0qpk {
            background-color: #FCE4EC;
        }
        
        /* Judul di sidebar */
        h1, h2, h3 {
            color: #AD1457;
        }
        
        /* Bikin gambar logo bulat */
        .rounded-logo {
            border-radius: 50%;
            border: 3px solid #EC407A;
            box-shadow: 0 4px 8px rgba(233, 30, 99, 0.3);
        }
        
        /* Teks anggota */
        .member-list {
            color: #6A1B4D;
            font-size: 14px;
            line-height: 1.8;
        }
        
        /* Info preprocessing */
        .preprocess-info {
            background-color: #FCE4EC;
            padding: 15px;
            border-radius: 10px;
            font-size: 14px;
            color: #6A1B4D;
            border-left: 4px solid #EC407A;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. FUNGSI DETEKSI WAJAH (Haar Cascade)
# ==========================================
def detect_and_crop_face(image_bytes):
    """
    Deteksi wajah menggunakan Haar Cascade, lalu crop area wajah.
    Kalau gagal deteksi, return gambar asli (biar tetap bisa jalan).
    """
    # Ubah bytes ke numpy array
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Load Haar Cascade
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    
    # Deteksi wajah
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    
    if len(faces) > 0:
        # Ambil wajah pertama (paling besar)
        x, y, w, h = max(faces, key=lambda rect: rect[2] * rect[3])
        # Crop wajah
        face_crop = gray[y:y+h, x:x+w]
        return face_crop, True
    else:
        # Kalau gagal deteksi, pakai gambar asli
        return gray, False

# ==========================================
# 3. FUNGSI PREPROCESSING (DENGAN CROP)
# ==========================================
def preprocess_with_face_detection(file_bytes, img_size=(100, 100)):
    """
    Preprocessing lengkap:
    1. Deteksi & crop wajah
    2. Grayscale (sudah dari crop)
    3. Resize ke ukuran target
    4. Flatten & normalisasi
    """
    # Deteksi wajah
    face_crop, detected = detect_and_crop_face(file_bytes)
    
    # Resize
    resized = cv2.resize(face_crop, img_size)
    
    # Normalisasi (0-1)
    normalized = resized / 255.0
    
    # Flatten
    vector = normalized.flatten()
    
    return vector, resized, detected

# ==========================================
# 4. JUDUL
# ==========================================
st.markdown('<p class="main-title">🌸 Deteksi Kemiripan Wajah</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Menggunakan Metode PCA (Eigenfaces) & Cosine Similarity</p>', unsafe_allow_html=True)

# ==========================================
# 5. SIDEBAR: UPLOAD DATA LATIH (DENGAN TOMBOL SAKURA)
# ==========================================
with st.sidebar:
    # Logo bulat
    st.markdown(
        '<img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="80" class="rounded-logo">',
        unsafe_allow_html=True
    )

    # --- INISIALISASI SESSION STATE UNTUK TOGGLE ---
    if "show_upload" not in st.session_state:
        st.session_state.show_upload = True   # default: muncul

    # --- TOMBOL SAKURA UNTUK TOGGLE ---
    if st.button("🌸 Sembunyikan Data Latih" if st.session_state.show_upload else "🌸 Tampilkan Data Latih", use_container_width=True):
        st.session_state.show_upload = not st.session_state.show_upload
        st.rerun()

    # --- BAGIAN UPLOAD DATA LATIH (Muncul sesuai status) ---
    if st.session_state.show_upload:
        st.header("Upload Data Latih")
        st.markdown("Upload **minimal 10 foto** wajah. <br> (Usahakan 2 orang berbeda, masing-masing 5+ foto) <br> Pastikan Mukanya Terlihat yaa <br> Dan No Filter yaa ^^", unsafe_allow_html=True)
        
        uploaded_train_files = st.file_uploader(
            "Pilih Foto Buat Latih ^^",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="train"
        )
        
        if uploaded_train_files:
            st.success(f"{len(uploaded_train_files)} yey foto sudah terupload!")
        else:
            st.warning("⬆️ Upload foto di sini")
    else:
        st.caption("🌸 Bagian upload data latih sedang disembunyikan. Klik tombol di atas untuk menampilkan.")

    st.divider()
    
    # --- SLIDER THRESHOLD (tetap muncul) ---
    threshold = st.slider("Atur Ambang Batas Kemiripan", 0.0, 1.0, 0.70, 0.05)
    st.caption(f"Threshold saat ini: {threshold:.2f}")
    
    st.divider()
    
    # --- DAFTAR ANGGOTA (tetap muncul) ---
    st.markdown(
        """
        <div class="member-list">
            <b>🌸 Dibuat oleh Kelompok 2</b><br>
            Anggota:<br>
            1. Gea Destadia Al-Zahra<br>
            2. Luna Amilia<br>
            3. Dalilah Arifah Ariandi DJR<br>
            4. Nadia Azzizah
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# 6. AREA UTAMA: UPLOAD 2 FOTO UJI
# ==========================================
st.header("Upload Dua Wajah yang Mau Kamu Bandingkan ^^")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("#### 📸 Foto Pertama")
    face1_file = st.file_uploader("Upload Foto 1", type=["jpg", "jpeg", "png"], key="face1", label_visibility="collapsed")

with col2:
    st.markdown("#### 📸 Foto Kedua")
    face2_file = st.file_uploader("Upload Foto 2", type=["jpg", "jpeg", "png"], key="face2", label_visibility="collapsed")

# ==========================================
# 7. TOMBOL PROSES
# ==========================================
st.markdown("---")
col_button, _ = st.columns([1, 3])
with col_button:
    proses_button = st.button("🚀 Proses Deteksi Sekarang", use_container_width=True)

# ==========================================
# 8. LOGIKA PEMROSESAN
# ==========================================
if proses_button:
    if not uploaded_train_files or len(uploaded_train_files) < 10:
        st.error("**Data Latih Kurang Nih...** Upload minimal 10 gambar wajah (2 orang, masing-masing 5 foto).")
    elif not face1_file or not face2_file:
        st.error("**Foto Uji Kurang Nih...** Upload kedua foto yang akan dibandingkan.")
    else:
        with st.spinner("Lagi memproses nih... tunggu yaa"):
            time.sleep(0.5)
            
            # --- A. Preprocessing Data Latih (dengan deteksi wajah) ---
            IMG_SIZE = (100, 100)
            X_train = []
            train_detected_status = []
            
            progress_bar = st.progress(0, text="Mengolah data latih...")
            for i, file in enumerate(uploaded_train_files):
                file_bytes = file.getvalue()
                vector, _, detected = preprocess_with_face_detection(file_bytes, IMG_SIZE)
                X_train.append(vector)
                train_detected_status.append(detected)
                progress_bar.progress((i + 1) / len(uploaded_train_files))
            
            X_train = np.array(X_train)
            
            # --- B. Preprocessing Foto Uji ---
            progress_bar.progress(50, text="Memproses foto uji...")
            
            # Foto 1
            face1_bytes = face1_file.getvalue()
            vec1, img1_resized, detected1 = preprocess_with_face_detection(face1_bytes, IMG_SIZE)
            
            # Foto 2
            face2_bytes = face2_file.getvalue()
            vec2, img2_resized, detected2 = preprocess_with_face_detection(face2_bytes, IMG_SIZE)
            
            # --- C. Jalankan PCA ---
            progress_bar.progress(70, text="Menjalankan PCA & mencari Eigenfaces...")
            k = min(50, len(X_train) - 1) if len(X_train) > 1 else 1
            pca = PCA(n_components=k)
            X_pca = pca.fit_transform(X_train)
            
            # Proyeksikan foto uji
            proj1 = pca.transform([vec1])
            proj2 = pca.transform([vec2])
            
            # Hitung Cosine Similarity
            similarity = cosine_similarity(proj1, proj2)[0][0]
            
            progress_bar.progress(100, text="Selesai!")
            time.sleep(0.3)
            progress_bar.empty()
            
            # ==========================================
            # 9. TAMPILKAN HASIL
            # ==========================================
            st.markdown("---")
            st.subheader("Hasil Deteksi Foto Kamu ^^")
            
            # Tampilkan info preprocessing
            st.markdown(f"""
            <div class="preprocess-info">
                <b>Proses Preprocessing Tunggu yaaa ^^:</b><br>
                • Gambar diubah ke Grayscale ✓<br>
                • Resize ke {IMG_SIZE[0]}x{IMG_SIZE[1]} pixel ✓<br>
                • Normalisasi pixel (0-1) ✓<br>
                • Flatten ke 1 vektor ✓<br>
                • Deteksi wajah: Foto 1 {'Berhasil!!' if detected1 else 'Yah Gagal.. Up lagi yaa ^^'} | Foto 2 {'Berhasil!!' if detected2 else 'Yah Gagal.. Up lagi yaa ^^'}
            </div>
            """, unsafe_allow_html=True)
            
            col_res1, col_res2, col_res3 = st.columns(3, gap="medium")
            
            with col_res1:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.image(img1_resized, width=180, caption="Foto 1 (Setelah Resize)", use_container_width=False)
                st.caption(f"Ukuran: {IMG_SIZE[0]}x{IMG_SIZE[1]}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_res2:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.image(img2_resized, width=180, caption="Foto 2 (Setelah Resize)", use_container_width=False)
                st.caption(f"Ukuran: {IMG_SIZE[0]}x{IMG_SIZE[1]}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_res3:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.metric(label="Skor Kemiripan", value=f"{similarity:.2%}", delta=None)
                
                if similarity >= threshold:
                    st.success("**Kesimpulan: MIRIP**")
                    st.markdown("*(Kemungkinan besar orang yang sama)*")
                    st.balloons()
                elif similarity >= 0.50:
                    st.warning("**Kesimpulan: CUKUP MIRIP**")
                    st.markdown("*(Perlu verifikasi tambahan)*")
                else:
                    st.error("**Kesimpulan: TIDAK MIRIP**")
                    st.markdown("*(Kemungkinan besar orang berbeda)*")
                
                st.caption(f"Jumlah Komponen PCA: {k}")
                st.caption(f"Varians data: {np.sum(pca.explained_variance_ratio_)*100:.1f}%")
                st.caption(f"Threshold yang digunakan: {threshold:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # --- Grafik PCA ---
            st.subheader("Grafik Akumulasi Informasi PCA")
            explained_variance = np.cumsum(pca.explained_variance_ratio_)
            
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(range(1, len(explained_variance)+1), explained_variance, 'bo-', linewidth=2, markersize=6)
            ax.axhline(y=0.95, color='red', linestyle='--', linewidth=2, label='95% Varians')
            ax.axhline(y=threshold, color='green', linestyle=':', linewidth=2, label=f'Threshold: {threshold:.2f}')
            ax.set_xlabel('Jumlah Komponen PCA (k)', fontsize=12)
            ax.set_ylabel('Akumulasi Informasi', fontsize=12)
            ax.set_title('Kurva Akumulasi Informasi PCA', fontsize=14)
            ax.grid(True, alpha=0.3)
            ax.legend(loc='lower right')
            ax.set_ylim(0, 1.05)
            st.pyplot(fig)