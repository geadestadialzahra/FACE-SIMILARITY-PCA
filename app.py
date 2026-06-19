# =====================================================
# APLIKASI DETEKSI KEMIRIPAN WAJAH DENGAN PCA
# =====================================================
# Dibuat oleh: Kelompok 2
# Mata Kuliah: Aljabar Linier / Computer Vision
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
# 1. PENGATURAN HALAMAN
# ==========================================
st.set_page_config(
    page_title="PCA Face Similarity",
    page_icon="🌸",
    layout="wide"
)

# ==========================================
# 2. CSS - TEMA PINK SOFT
# ==========================================
st.markdown("""
    <style>
        /* ===== BACKGROUND UTAMA ===== */
        .stApp, .main, .block-container, section.main, div[data-testid="stSidebar"] {
            background-color: #FFF0F5 !important;
            background-image: none !important;
        }
        
        /* ===== SEMUA TEKS ===== */
        body, p, div, span, label, h1, h2, h3, h4, h5, h6, .stMarkdown, .stText, .stCaption {
            color: #6A1B4D !important;
        }
        
        /* ===== HEADER (BAR ATAS) ===== */
        header {
            background: linear-gradient(135deg, #880E4F, #AD1457) !important;
            border-bottom: 2px solid #F8BBD0 !important;
        }
        
        /* ===== SEMUA ELEMEN DI HEADER JADI PUTIH ===== */
        header * {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }
        header button, header svg, header span, header div {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }
        header .st-emotion-cache-1v0mbdj, header .st-emotion-cache-1r6slb0 {
            color: #FFFFFF !important;
        }
        header button:hover {
            transform: scale(1.05) !important;
            transition: 0.3s !important;
        }
        
        /* ===== SIDEBAR ===== */
        .css-1d391kg, .css-12w0qpk, [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FCE4EC, #FFF0F5) !important;
            border-right: 2px solid #F8BBD0 !important;
        }
        
        /* ===== JUDUL UTAMA (DI TENGAH) ===== */
        .main-title {
            text-align: center !important;
            color: #AD1457 !important;
            font-size: 42px !important;
            font-weight: bold !important;
            text-shadow: 0 2px 15px rgba(173, 20, 87, 0.2) !important;
            display: block !important;
            width: 100% !important;
        }
        .sub-title {
            text-align: center !important;
            color: #D81B60 !important;
            font-size: 18px !important;
            text-shadow: 0 1px 10px rgba(216, 27, 96, 0.15) !important;
            display: block !important;
            width: 100% !important;
        }
        
        /* ===== SEMUA HEADING ===== */
        h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
            color: #AD1457 !important;
            font-weight: bold !important;
        }
        
        /* =========================================================
           ===== FILE UPLOADER =====
           ========================================================= */
        div[data-testid="stFileUploader"],
        .stFileUploader,
        .st-emotion-cache-1v0mbdj,
        .st-emotion-cache-1r6slb0,
        .st-emotion-cache-1wmy9hl {
            background: linear-gradient(135deg, #FCE4EC, #FFF0F5) !important;
            border: 2px dashed #EC407A !important;
            border-radius: 12px !important;
            padding: 10px !important;
        }
        div[data-testid="stFileUploader"] > div,
        .stFileUploader > div {
            background: rgba(255, 255, 255, 0.6) !important;
            border-radius: 8px !important;
            padding: 20px !important;
        }
        
        /* === TEKS UPLOADER DIKEMBALIKAN KE ITEM === */
        div[data-testid="stFileUploader"] *,
        .stFileUploader * {
            color: #6A1B4D !important;  /* warna item/pink gelap */
            background: transparent !important;
        }
        
        div[data-testid="stFileUploader"] button,
        .stFileUploader button {
            background: linear-gradient(135deg, #EC407A, #D81B60) !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
            padding: 5px 20px !important;
            transition: 0.3s !important;
        }
        div[data-testid="stFileUploader"] button:hover,
        .stFileUploader button:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 4px 15px rgba(233, 30, 99, 0.3) !important;
        }
        div[data-testid="stFileUploader"]:hover,
        .stFileUploader:hover {
            border-color: #D81B60 !important;
            background: linear-gradient(135deg, #F8BBD0, #FCE4EC) !important;
        }
        div[data-testid="stFileUploader"]:hover > div,
        .stFileUploader:hover > div {
            background: rgba(255, 255, 255, 0.8) !important;
        }
        
        /* =========================================================
           ===== TOMBOL =====
           ========================================================= */
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
            background: rgba(236, 64, 122, 0.2) !important;
            box-shadow: 0 0 20px rgba(236, 64, 122, 0.3) !important;
        }
        
        .stButton button {
            background: linear-gradient(135deg, #EC407A, #D81B60) !important;
            color: white !important;
            font-size: 18px !important;
            border-radius: 50px !important;
            padding: 10px 30px !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(233, 30, 99, 0.3) !important;
            transition: 0.3s !important;
        }
        .stButton button:hover {
            transform: scale(1.03) translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(233, 30, 99, 0.4) !important;
        }
        
        /* =========================================================
           ===== METRIC & SLIDER =====
           ========================================================= */
        .stMetric {
            background: rgba(255, 255, 255, 0.3) !important;
            border-radius: 12px !important;
            padding: 10px !important;
        }
        .stMetric label, .stMetric div, .stMetric span {
            color: #6A1B4D !important;
        }
        .stSlider > div {
            background: rgba(255, 255, 255, 0.4) !important;
            border-radius: 10px !important;
        }
        
        /* =========================================================
           ===== ALERT =====
           ========================================================= */
        .stAlert p, .stSuccess p, .stError p, .stWarning p {
            color: #6A1B4D !important;
            font-weight: bold !important;
            font-size: 20px !important;
        }
        .stWarning {
            background-color: rgba(255, 193, 7, 0.15) !important;
            border-radius: 12px !important;
            padding: 5px !important;
        }
        .stWarning p {
            color: #AD1457 !important;
        }
        
        /* =========================================================
           ===== BADGE PINK (LABEL FOTO) =====
           ========================================================= */
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
            box-shadow: 0 2px 10px rgba(233, 30, 99, 0.12) !important;
            text-align: center !important;
            margin-bottom: 12px !important;
        }
        .result-container {
            text-align: center !important;
        }
        
        /* =========================================================
           ===== PENJELASAN GRAFIK =====
           ========================================================= */
        .explanation-box {
            background: rgba(255, 255, 255, 0.5) !important;
            padding: 15px !important;
            border-radius: 12px !important;
            border-left: 4px solid #EC407A !important;
            box-shadow: 0 2px 10px rgba(233, 30, 99, 0.08) !important;
            color: #6A1B4D !important;
        }
        .explanation-box b {
            color: #AD1457 !important;
        }
        .explanation-box ul {
            padding-left: 20px !important;
        }
        .explanation-box li {
            margin-bottom: 6px !important;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SESSION STATE
# ==========================================
if "show_upload" not in st.session_state:
    st.session_state.show_upload = True

# ==========================================
# 4. FUNGSI DETEKSI WAJAH & PREPROCESSING
# ==========================================

def deteksi_dan_potong_wajah(byte_gambar):
    arr_np = np.frombuffer(byte_gambar, np.uint8)
    img = cv2.imdecode(arr_np, cv2.IMREAD_COLOR)
    abu = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade_wajah = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    wajah = cascade_wajah.detectMultiScale(abu, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    if len(wajah) > 0:
        x, y, w, h = max(wajah, key=lambda rect: rect[2] * rect[3])
        potongan = abu[y:y+h, x:x+w]
        return potongan, True
    else:
        return abu, False

def praproses_dengan_deteksi_wajah(byte_gambar, ukuran=(100, 100)):
    potongan, terdeteksi = deteksi_dan_potong_wajah(byte_gambar)
    resize = cv2.resize(potongan, ukuran)
    normal = resize / 255.0
    vektor = normal.flatten()
    return vektor, resize, terdeteksi

def muat_gambar_berwarna(byte_gambar, ukuran=(100, 100)):
    arr_np = np.frombuffer(byte_gambar, np.uint8)
    img = cv2.imdecode(arr_np, cv2.IMREAD_COLOR)
    abu = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade_wajah = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    wajah = cascade_wajah.detectMultiScale(abu, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    if len(wajah) > 0:
        x, y, w, h = max(wajah, key=lambda rect: rect[2] * rect[3])
        potongan = img[y:y+h, x:x+w]
        resize = cv2.resize(potongan, ukuran)
        return cv2.cvtColor(resize, cv2.COLOR_BGR2RGB)
    else:
        resize = cv2.resize(img, ukuran)
        return cv2.cvtColor(resize, cv2.COLOR_BGR2RGB)

# ==========================================
# 5. JUDUL (DI TENGAH)
# ==========================================
st.markdown('<h1 class="main-title">🌸 Deteksi Kemiripan Wajah</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Menggunakan PCA (Eigenfaces) & Cosine Similarity</p>', unsafe_allow_html=True)

# ==========================================
# 6. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("---")
    st.markdown('<div class="sakura-btn-container">', unsafe_allow_html=True)
    kol1, kol2, kol3 = st.columns([1, 2, 1])
    with kol2:
        if st.button("🌸", key="toggle_sidebar"):
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
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="train"
        )
        
        if file_latih:
            st.success(f"✅ {len(file_latih)} foto berhasil terupload!")
        else:
            st.warning("⬆️ Upload foto di sini")
    else:
        st.info("🌸 Upload disembunyikan. Klik sakura di atas.")
    
    st.divider()
    
    ambang = st.slider("🎯 Ambang Batas Kemiripan", 0.0, 1.0, 0.70, 0.05)
    st.caption(f"Threshold: {ambang:.2f}")
    
    st.divider()
    
    st.markdown("""
        <b>🌸 Kelompok 2</b><br>
        1. Gea Destadia Al-Zahra<br>
        2. Luna Amilia<br>
        3. Dalilah Arifah Ariandi DJR<br>
        4. Nadia Azzizah
    """, unsafe_allow_html=True)

# ==========================================
# 7. AREA UTAMA: UPLOAD 2 FOTO UJI
# ==========================================
st.markdown("## 🔍 Upload Dua Wajah untuk Dibandingkan")

kolom1, kolom2 = st.columns(2)

with kolom1:
    st.markdown("### 📸 Foto Pertama")
    file1 = st.file_uploader("Upload Foto 1", type=["jpg","jpeg","png"], key="f1", label_visibility="collapsed")

with kolom2:
    st.markdown("### 📸 Foto Kedua")
    file2 = st.file_uploader("Upload Foto 2", type=["jpg","jpeg","png"], key="f2", label_visibility="collapsed")

# ==========================================
# 8. TOMBOL PROSES & LOGIKA DETEKSI
# ==========================================
if st.button("🚀 Proses Deteksi Sekarang", use_container_width=True):
    if 'file_latih' not in locals() or not file_latih or len(file_latih) < 10:
        st.error("⚠️ **Data Latih Kurang!** Upload minimal 10 foto.")
        st.info("💡 Klik tombol 🌸 di sidebar untuk menampilkan bagian upload.")
    elif not file1 or not file2:
        st.error("⚠️ Upload kedua foto uji!")
    else:
        with st.spinner("⏳ Sedang memproses... Mohon tunggu."):
            time.sleep(0.5)
            
            UKURAN = (100, 100)
            X_latih = []
            
            progress = st.progress(0, text="Mengolah data latih...")
            for i, file in enumerate(file_latih):
                vektor, _, _ = praproses_dengan_deteksi_wajah(file.getvalue(), UKURAN)
                X_latih.append(vektor)
                progress.progress((i+1)/len(file_latih))
            
            X_latih = np.array(X_latih)
            
            progress.progress(50, text="Menjalankan PCA & mencari Eigenfaces...")
            k = min(50, len(X_latih)-1) if len(X_latih)>1 else 1
            pca = PCA(n_components=k)
            X_pca = pca.fit_transform(X_latih)
            
            progress.progress(70, text="Memproses foto uji...")
            
            vektor1, _, _ = praproses_dengan_deteksi_wajah(file1.getvalue(), UKURAN)
            vektor2, _, _ = praproses_dengan_deteksi_wajah(file2.getvalue(), UKURAN)
            
            gambar1 = muat_gambar_berwarna(file1.getvalue(), UKURAN)
            gambar2 = muat_gambar_berwarna(file2.getvalue(), UKURAN)
            
            proyeksi1 = pca.transform([vektor1])
            proyeksi2 = pca.transform([vektor2])
            
            kemiripan = cosine_similarity(proyeksi1, proyeksi2)[0][0]
            
            progress.progress(100, text="Selesai!")
            time.sleep(0.3)
            progress.empty()
            
            # ==========================================
            # 9. TAMPILKAN HASIL
            # ==========================================
            st.markdown("---")
            st.subheader("📊 Hasil Deteksi")
            
            kolom_r1, kolom_r2, kolom_r3 = st.columns([2, 2, 1.5])
            
            with kolom_r1:
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.markdown('<div class="pink-badge">📸 Foto Pertama</div>', unsafe_allow_html=True)
                st.image(gambar1, caption=f"Resize {UKURAN[0]}x{UKURAN[1]}", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with kolom_r2:
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.markdown('<div class="pink-badge">📸 Foto Kedua</div>', unsafe_allow_html=True)
                st.image(gambar2, caption=f"Resize {UKURAN[0]}x{UKURAN[1]}", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with kolom_r3:
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.markdown('<div class="pink-badge">🎯 Skor Kemiripan</div>', unsafe_allow_html=True)
                st.markdown(f"<h1 style='color:#AD1457;font-size:42px;'>{kemiripan:.2%}</h1>", unsafe_allow_html=True)
                
                if kemiripan >= ambang:
                    st.success("✅ **MIRIP**")
                    st.balloons()
                elif kemiripan >= 0.50:
                    st.warning("⚠️ **CUKUP MIRIP**")
                else:
                    st.error("❌ **TIDAK MIRIP**")
                
                st.caption(f"Komponen PCA: {k}")
                st.caption(f"Varians: {np.sum(pca.explained_variance_ratio_)*100:.1f}%")
                st.caption(f"Threshold: {ambang:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # ==========================================
            # 10. GRAFIK + PENJELASAN
            # ==========================================
            st.markdown("---")
            kolom_graf, kolom_exp = st.columns([1, 1])
            
            with kolom_graf:
                st.subheader("📈 Grafik Akumulasi Informasi")
                varians = np.cumsum(pca.explained_variance_ratio_)
                fig, ax = plt.subplots(figsize=(5, 3.5))
                ax.plot(range(1, len(varians)+1), varians, 'bo-', linewidth=2, markersize=5)
                ax.axhline(y=0.95, color='red', linestyle='--', linewidth=2, label='95% Varians')
                ax.axhline(y=ambang, color='green', linestyle=':', linewidth=2, label=f'Threshold {ambang:.2f}')
                ax.set_xlabel('Jumlah Komponen PCA (k)', fontsize=10)
                ax.set_ylabel('Akumulasi Informasi', fontsize=10)
                ax.set_title('Kurva Akumulasi Informasi PCA', fontsize=11)
                ax.grid(True, alpha=0.3)
                ax.legend(loc='lower right', fontsize=8)
                ax.set_ylim(0, 1.05)
                st.pyplot(fig)
            
            with kolom_exp:
                st.subheader("📖 Penjelasan Grafik")
                st.markdown("""
                <div class="explanation-box">
                Grafik ini menunjukkan seberapa banyak <b>informasi wajah</b> yang bisa dipertahankan jika kita menggunakan sejumlah komponen PCA (k).
                
                <br><br>
                
                <b>🔵 Garis biru</b> → kurva akumulasi varians. Semakin tinggi, semakin baik.<br>
                <b>🔴 Garis merah putus-putus</b> → 95% varians data sudah terwakili.<br>
                <b>🟢 Garis hijau titik-titik</b> → <b>Threshold</b> (batas kemiripan) yang kamu atur di sidebar.
                
                <br><br>
                
                <b>💡 Cara baca:</b><br>
                Dari 10.000 pixel wajah, PCA bisa meringkasnya menjadi 50 angka saja tanpa kehilangan banyak informasi. Semakin tinggi garis biru, semakin baik representasi wajahnya.
                </div>
                """, unsafe_allow_html=True)
