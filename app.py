# =====================================================
# APLIKASI PCA UNTUK PENGOLAHAN CITRA WAJAH
# =====================================================
# Kelompok 2 - Aljabar Linier / Computer Vision
# =====================================================
#
# Fitur:
# 1. Home      - Profil kelompok dan deskripsi aplikasi
# 2. Grayscale - Konversi gambar berwarna menjadi hitam-putih
# 3. Kompresi  - Kompresi gambar dengan PCA (SSIM, PSNR, rasio)
# 4. Deteksi   - Membandingkan dua wajah dengan Eigenfaces (PCA)
# =====================================================

import streamlit as st
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
import time

# ==========================================
# 1. IMPOR SKIMAGE (opsional, untuk SSIM & PSNR)
# ==========================================
try:
    from skimage.metrics import structural_similarity as ssim
    from skimage.metrics import peak_signal_noise_ratio as psnr
    SKIMAGE_AVAILABLE = True
except ImportError:
    SKIMAGE_AVAILABLE = False

# ==========================================
# 2. PENGATURAN HALAMAN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="PCA Face App",
    page_icon="🌸",
    layout="wide"
)

# ==========================================
# 3. CSS - TEMA PINK SOFT
# ==========================================
st.markdown("""
    <style>
        /* ----- BACKGROUND ----- */
        .stApp, .main, .block-container, section.main, div[data-testid="stSidebar"] {
            background-color: #FFF0F5 !important;
            background-image: none !important;
        }
        body, p, div, span, label, h1, h2, h3, h4, h5, h6, .stMarkdown, .stText, .stCaption {
            color: #6A1B4D !important;
        }

        /* ----- HEADER (BAR ATAS) ----- */
        header {
            background: linear-gradient(135deg, #880E4F, #AD1457) !important;
            border-bottom: 2px solid #F8BBD0 !important;
        }
        header * {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }

        /* ----- SIDEBAR ----- */
        .css-1d391kg, .css-12w0qpk, [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FCE4EC, #FFF0F5) !important;
            border-right: 2px solid #F8BBD0 !important;
        }

        /* ----- JUDUL ----- */
        .main-title {
            text-align: center !important;
            color: #AD1457 !important;
            font-size: 42px !important;
            font-weight: bold !important;
            text-shadow: 0 2px 15px rgba(173,20,87,0.2) !important;
        }
        .sub-title {
            text-align: center !important;
            color: #D81B60 !important;
            font-size: 18px !important;
            text-shadow: 0 1px 10px rgba(216,27,96,0.15) !important;
        }

        /* ----- TOMBOL UMUM ----- */
        .stButton button {
            background: linear-gradient(135deg, #EC407A, #D81B60) !important;
            color: white !important;
            font-size: 18px !important;
            border-radius: 50px !important;
            padding: 10px 30px !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(233,30,99,0.3) !important;
            transition: 0.3s !important;
        }
        .stButton button:hover {
            transform: scale(1.03) translateY(-2px) !important;
        }

        /* ----- FILE UPLOADER ----- */
        div[data-testid="stFileUploader"] {
            background: linear-gradient(135deg, #FCE4EC, #FFF0F5) !important;
            border: 2px dashed #EC407A !important;
            border-radius: 12px !important;
            padding: 10px !important;
        }
        div[data-testid="stFileUploader"] > div {
            background: rgba(255,255,255,0.6) !important;
            border-radius: 8px !important;
            padding: 20px !important;
        }
        div[data-testid="stFileUploader"] * {
            color: #6A1B4D !important;
        }
        div[data-testid="stFileUploader"] button {
            background: linear-gradient(135deg, #EC407A, #D81B60) !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
            padding: 5px 20px !important;
        }

        /* ----- BADGE PINK ----- */
        .pink-badge {
            display: block !important;
            width: 100% !important;
            background: linear-gradient(135deg, #FCE4EC, #F8BBD0) !important;
            color: #AD1457 !important;
            padding: 10px 18px !important;
            border-radius: 12px !important;
            font-weight: bold !important;
            font-size: 16px !important;
            border: 1px solid #EC407A !important;
            text-align: center !important;
            margin-bottom: 12px !important;
        }

        /* ----- CARD HASIL ----- */
        .result-card {
            background: linear-gradient(135deg, #FCE4EC, #FFF0F5) !important;
            padding: 20px !important;
            border-radius: 15px !important;
            text-align: center !important;
            border: 1px solid #F8BBD0 !important;
            box-shadow: 0 4px 15px rgba(233,30,99,0.1) !important;
            height: 100% !important;
        }

        /* ----- KOTAK PENJELASAN ----- */
        .explanation-box {
            background: rgba(255,255,255,0.5) !important;
            padding: 15px !important;
            border-radius: 12px !important;
            border-left: 4px solid #EC407A !important;
            box-shadow: 0 2px 10px rgba(233,30,99,0.08) !important;
            color: #6A1B4D !important;
        }

        /* ----- TOMBOL NAVIGASI DI SIDEBAR ----- */
        .stSidebar .stButton button {
            width: 48px !important;
            height: 48px !important;
            min-width: 48px !important;
            min-height: 48px !important;
            max-width: 48px !important;
            max-height: 48px !important;
            border-radius: 50% !important;
            border: none !important;
            background: transparent !important;
            font-size: 60px !important;   /* emoji besar */
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 !important;
            margin: 0 auto !important;
            box-shadow: none !important;
            transition: all 0.3s ease !important;
            line-height: 1 !important;
        }
        .stSidebar .stButton button:hover {
            transform: scale(1.05) !important;
            background: rgba(236,64,122,0.1) !important;
        }

        /* ----- CAPTION DI BAWAH NAVIGASI ----- */
        .sidebar-caption {
            text-align: center;
            color: #AD1457;
            font-weight: bold;
            font-size: 15px;
            padding-top: 5px;
        }

        /* ----- TOMBOL SAKURA DI SIDEBAR (untuk toggle upload) ----- */
        .sakura-btn-container .stButton button {
            background: transparent !important;
            border: 2px solid #EC407A !important;
            border-radius: 50% !important;
            font-size: 32px !important;
            padding: 8px 14px !important;
            color: #EC407A !important;
            width: 55px !important;
            height: 55px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            margin: 0 auto !important;
            transition: 0.3s !important;
        }
        .sakura-btn-container .stButton button:hover {
            transform: scale(1.1) rotate(15deg) !important;
            background: rgba(236,64,122,0.2) !important;
            box-shadow: 0 0 20px rgba(236,64,122,0.3) !important;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. SESSION STATE
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"          # halaman aktif
if "show_upload" not in st.session_state:
    st.session_state.show_upload = True        # toggle upload data latih

# ==========================================
# 5. FUNGSI DETEKSI WAJAH (Haar Cascade)
# ==========================================

def deteksi_dan_potong_wajah(byte_gambar):
    """Deteksi wajah dengan Haar Cascade, lalu crop area wajah.
       Jika gagal, return gambar asli."""
    arr_np = np.frombuffer(byte_gambar, np.uint8)
    img = cv2.imdecode(arr_np, cv2.IMREAD_COLOR)
    abu = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    wajah = cascade.detectMultiScale(abu, scaleFactor=1.1, minNeighbors=5, minSize=(50,50))
    if len(wajah) > 0:
        x, y, w, h = max(wajah, key=lambda r: r[2]*r[3])
        return abu[y:y+h, x:x+w], True
    return abu, False

def praproses_wajah(byte_gambar, ukuran=(100,100)):
    """Preprocessing: crop wajah -> resize -> normalisasi -> flatten"""
    potongan, terdeteksi = deteksi_dan_potong_wajah(byte_gambar)
    resize = cv2.resize(potongan, ukuran)
    normal = resize / 255.0
    vektor = normal.flatten()
    return vektor, resize, terdeteksi

def muat_gambar_warna(byte_gambar, ukuran=(100,100)):
    """Muat gambar berwarna (setelah crop wajah) untuk ditampilkan."""
    arr_np = np.frombuffer(byte_gambar, np.uint8)
    img = cv2.imdecode(arr_np, cv2.IMREAD_COLOR)
    abu = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    wajah = cascade.detectMultiScale(abu, scaleFactor=1.1, minNeighbors=5, minSize=(50,50))
    if len(wajah) > 0:
        x, y, w, h = max(wajah, key=lambda r: r[2]*r[3])
        potongan = img[y:y+h, x:x+w]
        resize = cv2.resize(potongan, ukuran)
        return cv2.cvtColor(resize, cv2.COLOR_BGR2RGB)
    else:
        resize = cv2.resize(img, ukuran)
        return cv2.cvtColor(resize, cv2.COLOR_BGR2RGB)

# ==========================================
# 6. HALAMAN-HALAMAN APLIKASI
# ==========================================

# ---------- 6a. HALAMAN HOME ----------
def halaman_home():
    st.markdown('<h1 class="main-title">🌸 Selamat Datang di Aplikasi PCA</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Kelompok 2 – Aljabar Linier / Computer Vision</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="explanation-box">
        <h3>📌 Tentang Aplikasi</h3>
        Aplikasi ini dibuat untuk memenuhi tugas mata kuliah Aljabar Linier / Computer Vision.
        Kami mengimplementasikan metode <b>PCA (Principal Component Analysis)</b> untuk:
        <ul>
            <li><b>🌫️ Grayscale</b> – Mengubah gambar berwarna menjadi hitam-putih</li>
            <li><b>🗜️ Kompresi</b> – Mengompresi gambar dengan PCA, menampilkan SSIM, PSNR, dan rasio kompresi</li>
            <li><b>🔍 Deteksi Kemiripan</b> – Membandingkan dua wajah menggunakan Eigenfaces</li>
        </ul>
        Gunakan menu emoji di samping untuk memilih fitur.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="result-card">
        <h4>👥 Anggota Kelompok</h4>
        <p>1. Gea Destadia Al-Zahra<br>
        2. Luna Amilia<br>
        3. Dalilah Arifah Ariandi DJR<br>
        4. Nadia Azzizah</p>
        <p style="font-size:14px; color:#AD1457;">🌸 Terima kasih telah berkunjung!</p>
        </div>
        """, unsafe_allow_html=True)

# ---------- 6b. HALAMAN GRAYSCALE ----------
def halaman_grayscale():
    st.markdown('<h1 class="main-title">🌫️ Konversi ke Grayscale</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Upload gambar berwarna, lihat hasil hitam-putih</p>', unsafe_allow_html=True)

    file = st.file_uploader("Upload gambar (JPG/PNG)", type=["jpg","jpeg","png"])
    if file is not None:
        img = Image.open(file)
        col1, col2 = st.columns(2)
        with col1:
            st.image(img, caption="Gambar Asli (Berwarna)", use_container_width=True)
        with col2:
            gray = img.convert("L")
            st.image(gray, caption="Hasil Grayscale", use_container_width=True)
        st.markdown(f"""
        <div class="explanation-box">
        <b>Informasi:</b><br>
        • Ukuran gambar: {img.size[0]} x {img.size[1]} pixel<br>
        • Mode warna: {img.mode} → Grayscale (L)
        </div>
        """, unsafe_allow_html=True)

# ---------- 6c. HALAMAN KOMPRESI PCA ----------
def halaman_kompresi():
    st.markdown('<h1 class="main-title">🗜️ Kompresi Gambar dengan PCA</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Upload gambar, atur jumlah komponen, lihat hasil kompresi & metrik kualitas</p>', unsafe_allow_html=True)

    file = st.file_uploader("Upload gambar (JPG/PNG)", type=["jpg","jpeg","png"])
    if file is not None:
        # Baca & resize jika terlalu besar
        img = Image.open(file).convert("L")
        img_np = np.array(img, dtype=np.float64)
        h, w = img_np.shape
        if h > 300 or w > 300:
            st.warning("Gambar terlalu besar, di-resize ke 256x256 agar cepat")
            img = img.resize((256,256))
            img_np = np.array(img, dtype=np.float64)
            h, w = img_np.shape

        k_max = min(h, w)
        k = st.slider("Jumlah komponen PCA (k)", 1, k_max, min(50,k_max), 1)

        # --- PCA untuk kompresi ---
        mean_col = np.mean(img_np, axis=0)
        centered = img_np - mean_col
        cov = np.cov(centered, rowvar=False)
        eigen_vals, eigen_vecs = np.linalg.eigh(cov)
        idx = np.argsort(eigen_vals)[::-1]
        eigen_vals = eigen_vals[idx]
        eigen_vecs = eigen_vecs[:, idx]
        Vk = eigen_vecs[:, :k]
        proj = centered @ Vk
        rekon = proj @ Vk.T + mean_col
        rekon = np.clip(rekon, 0, 255).astype(np.uint8)

        # --- Metrik kualitas ---
        img_uint8 = img_np.astype(np.uint8)
        if SKIMAGE_AVAILABLE:
            ssim_val = ssim(img_uint8, rekon, data_range=255)
            psnr_val = psnr(img_uint8, rekon, data_range=255)
        else:
            ssim_val = "Tidak tersedia"
            psnr_val = "Tidak tersedia"

        original_size = h * w
        compressed_size = h * k + w * k
        compression_ratio = compressed_size / original_size
        saving = (1 - compression_ratio) * 100

        # --- Tampilkan hasil ---
        col1, col2 = st.columns(2)
        with col1:
            st.image(img_uint8, caption="Gambar Asli (Grayscale)", use_container_width=True)
        with col2:
            st.image(rekon, caption=f"Hasil Kompresi (k={k})", use_container_width=True)

        st.markdown("### 📊 Metrik Kualitas")
        c1,c2,c3 = st.columns(3)
        c1.metric("SSIM", f"{ssim_val:.4f}" if isinstance(ssim_val,float) else ssim_val)
        c2.metric("PSNR", f"{psnr_val:.2f} dB" if isinstance(psnr_val,float) else psnr_val)
        c3.metric("Penghematan", f"{saving:.1f}%")

        st.markdown(f"""
        <div class="explanation-box">
        <b>Detail Kompresi:</b><br>
        • Ukuran asli: {original_size} pixel<br>
        • Ukuran setelah PCA: {compressed_size} koefisien<br>
        • Rasio kompresi: {compression_ratio:.4f}<br>
        • Jumlah komponen PCA: {k}
        </div>
        """, unsafe_allow_html=True)

        # --- Grafik akumulasi varians ---
        total_var = np.sum(eigen_vals)
        cum_var = np.cumsum(eigen_vals) / total_var
        fig, ax = plt.subplots(figsize=(8,4))
        ax.plot(range(1,len(cum_var)+1), cum_var, 'bo-', linewidth=2)
        ax.axhline(y=0.95, color='r', linestyle='--', label='95% Varians')
        ax.axvline(x=k, color='g', linestyle=':', label=f'k = {k}')
        ax.set_xlabel('Jumlah Komponen (k)')
        ax.set_ylabel('Akumulasi Varians')
        ax.set_title('Kurva Akumulasi Informasi PCA')
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

# ---------- 6d. HALAMAN DETEKSI KEMIRIPAN ----------
def halaman_deteksi():
    st.markdown('<h1 class="main-title">🔍 Deteksi Kemiripan Wajah</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Bandingkan dua wajah dengan metode Eigenfaces (PCA)</p>', unsafe_allow_html=True)

    # ----- SIDEBAR: Upload data latih -----
    with st.sidebar:
        st.markdown("---")
        st.markdown('<div class="sakura-btn-container">', unsafe_allow_html=True)
        kol1, kol2, kol3 = st.columns([1,2,1])
        with kol2:
            if st.button("🌸", key="toggle_upload"):
                st.session_state.show_upload = not st.session_state.show_upload
                st.rerun()
            st.caption("Klik Sakura")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")

        if st.session_state.show_upload:
            st.header("📂 Upload Data Latih")
            st.markdown("Upload **minimal 10 foto** wajah (2 orang, masing-masing 5+ foto)")
            file_latih = st.file_uploader(
                "Pilih Foto",
                type=["jpg","jpeg","png"],
                accept_multiple_files=True,
                key="train_deteksi"
            )
            if file_latih:
                st.success(f"✅ {len(file_latih)} foto terupload!")
            else:
                st.warning("⬆️ Upload foto di sini")
        else:
            st.info("🌸 Upload disembunyikan. Klik sakura di atas.")

        st.divider()
        ambang = st.slider("🎯 Ambang Batas Kemiripan", 0.0, 1.0, 0.70, 0.05, key="threshold_deteksi")
        st.caption(f"Threshold: {ambang:.2f}")
        st.divider()
        st.markdown("""
            <b>🌸 Kelompok 2</b><br>
            1. Gea Destadia Al-Zahra<br>
            2. Luna Amilia<br>
            3. Dalilah Arifah Ariandi DJR<br>
            4. Nadia Azzizah
        """, unsafe_allow_html=True)

    # ----- AREA UTAMA: Upload 2 foto uji -----
    st.markdown("## 🔍 Upload Dua Wajah untuk Dibandingkan")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📸 Foto Pertama")
        file1 = st.file_uploader("Upload Foto 1", type=["jpg","jpeg","png"], key="f1_deteksi", label_visibility="collapsed")
    with col2:
        st.markdown("### 📸 Foto Kedua")
        file2 = st.file_uploader("Upload Foto 2", type=["jpg","jpeg","png"], key="f2_deteksi", label_visibility="collapsed")

    # ----- Tombol proses -----
    if st.button("🚀 Proses Deteksi Sekarang", use_container_width=True):
        # Validasi
        if 'file_latih' not in locals() or not file_latih or len(file_latih) < 10:
            st.error("⚠️ **Data Latih Kurang!** Upload minimal 10 foto.")
            st.info("💡 Klik tombol 🌸 di sidebar untuk menampilkan upload.")
        elif not file1 or not file2:
            st.error("⚠️ Upload kedua foto uji!")
        else:
            with st.spinner("⏳ Memproses..."):
                time.sleep(0.5)

                UKURAN = (100,100)
                X_latih = []

                # ----- Proses data latih -----
                progress = st.progress(0, text="Mengolah data latih...")
                for i, f in enumerate(file_latih):
                    vektor, _, _ = praproses_wajah(f.getvalue(), UKURAN)
                    X_latih.append(vektor)
                    progress.progress((i+1)/len(file_latih))
                X_latih = np.array(X_latih)

                # ----- PCA -----
                progress.progress(50, text="Menjalankan PCA & mencari Eigenfaces...")
                k = min(50, len(X_latih)-1) if len(X_latih)>1 else 1
                pca = PCA(n_components=k)
                pca.fit(X_latih)

                # ----- Proses foto uji -----
                progress.progress(70, text="Memproses foto uji...")
                v1, _, _ = praproses_wajah(file1.getvalue(), UKURAN)
                v2, _, _ = praproses_wajah(file2.getvalue(), UKURAN)
                img1 = muat_gambar_warna(file1.getvalue(), UKURAN)
                img2 = muat_gambar_warna(file2.getvalue(), UKURAN)

                proj1 = pca.transform([v1])
                proj2 = pca.transform([v2])
                kemiripan = cosine_similarity(proj1, proj2)[0][0]
                progress.empty()

                # ----- Tampilkan hasil -----
                st.markdown("---")
                st.subheader("📊 Hasil Deteksi")

                col_r1, col_r2, col_r3 = st.columns([2,2,1.5])
                with col_r1:
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.markdown('<span class="pink-badge">📸 Foto Pertama</span>', unsafe_allow_html=True)
                    st.image(img1, caption=f"Resize {UKURAN[0]}x{UKURAN[1]}", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                with col_r2:
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.markdown('<span class="pink-badge">📸 Foto Kedua</span>', unsafe_allow_html=True)
                    st.image(img2, caption=f"Resize {UKURAN[0]}x{UKURAN[1]}", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                with col_r3:
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.markdown('<span class="pink-badge">🎯 Skor Kemiripan</span>', unsafe_allow_html=True)
                    st.markdown(f"<h1 style='color:#AD1457;font-size:42px;'>{kemiripan:.2%}</h1>", unsafe_allow_html=True)
                    if kemiripan >= ambang:
                        st.success("✅ MIRIP")
                        st.balloons()
                    elif kemiripan >= 0.50:
                        st.warning("⚠️ CUKUP MIRIP")
                    else:
                        st.error("❌ TIDAK MIRIP")
                    st.caption(f"Komponen PCA: {k}")
                    st.caption(f"Varians: {np.sum(pca.explained_variance_ratio_)*100:.1f}%")
                    st.markdown('</div>', unsafe_allow_html=True)

                # ----- Grafik akumulasi varians -----
                st.subheader("📈 Grafik Akumulasi Informasi")
                varians = np.cumsum(pca.explained_variance_ratio_)
                fig, ax = plt.subplots(figsize=(5,3.5))
                ax.plot(range(1,len(varians)+1), varians, 'bo-', linewidth=2, markersize=5)
                ax.axhline(y=0.95, color='r', linestyle='--', label='95% Varians')
                ax.axhline(y=ambang, color='g', linestyle=':', label=f'Threshold {ambang:.2f}')
                ax.set_xlabel('Jumlah Komponen (k)')
                ax.set_ylabel('Akumulasi Varians')
                ax.set_title('Kurva Akumulasi Informasi PCA')
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

                # ----- Penjelasan grafik -----
                st.markdown("""
                <div class="explanation-box">
                <b>📖 Penjelasan Grafik:</b><br>
                • 🔵 Garis biru → akumulasi varians. Semakin tinggi, semakin baik.<br>
                • 🔴 Garis merah putus-putus → 95% varians data sudah terwakili.<br>
                • 🟢 Garis hijau titik-titik → Threshold (batas kemiripan) yang diatur.
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# 7. NAVIGASI SIDEBAR (4 EMOJI)
# ==========================================
st.sidebar.markdown("🌸 **Haloo!!**")

# Daftar menu: (emoji, nama_halaman)
MENUS = [
    ("🏠", "🏠 Home"),
    ("🌫️", "🌫️ Grayscale"),
    ("🗜️", "🗜️ Kompresi"),
    ("🔍", "🔍 Deteksi Kemiripan")
]

cols = st.sidebar.columns(4)
for col, (emoji, page_name) in zip(cols, MENUS):
    with col:
        is_active = (st.session_state.page == page_name)
        # Tombol aktif: background pink + efek turun
        if is_active:
            st.markdown(f"""
                <style>
                    .stSidebar .stButton button[data-testid="baseButton-secondary"]:has(> div:contains("{emoji}")) {{
                        background: #F8BBD0 !important;
                        transform: translateY(4px) scale(1.02) !important;
                        box-shadow: 0 4px 12px rgba(236,64,122,0.3) !important;
                        border: none !important;
                    }}
                </style>
            """, unsafe_allow_html=True)
        if st.button(emoji, key=f"nav_{emoji}", use_container_width=True):
            st.session_state.page = page_name
            st.rerun()

# Keterangan halaman aktif di bawah emoji
st.sidebar.markdown("---")
caption_map = {
    "🏠 Home": "📌 Beranda & Profil",
    "🌫️ Grayscale": "🌫️ Ubah ke hitam-putih",
    "🗜️ Kompresi": "🗜️ Kompresi dengan PCA",
    "🔍 Deteksi Kemiripan": "🔍 Bandingkan dua wajah"
}
st.sidebar.markdown(f'<p class="sidebar-caption">{caption_map.get(st.session_state.page, "")}</p>', unsafe_allow_html=True)

# ==========================================
# 8. TAMPILKAN HALAMAN SESUAI PILIHAN
# ==========================================
page = st.session_state.page
if page == "🏠 Home":
    halaman_home()
elif page == "🌫️ Grayscale":
    halaman_grayscale()
elif page == "🗜️ Kompresi":
    halaman_kompresi()
elif page == "🔍 Deteksi Kemiripan":
    halaman_deteksi()
