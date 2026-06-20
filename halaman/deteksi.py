# halaman/deteksi.py - Halaman Deteksi Kemiripan Wajah
# =====================================================
# Fitur: Membandingkan dua wajah menggunakan metode Eigenfaces (PCA)
# =====================================================

import streamlit as st
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity

def tampilkan():
    # ---- 1. JUDUL & PENJELASAN ----
    st.markdown('<h1 class="main-title">🌸 Deteksi Kemiripan Wajah</h1>', unsafe_allow_html=True)
    
    # Penjelasan yang menyambut
    st.markdown("""
    <div class="explanation-box">
        <b>👋 Hai! Selamat datang di halaman Deteksi Kemiripan Wajah.</b><br><br>
        Di sini kamu bisa membandingkan dua foto wajah untuk melihat apakah 
        kedua orang tersebut <b>mirip</b> atau <b>tidak mirip</b>.<br><br>
        
        <b>📋 Cara menggunakan:</b><br>
        1️⃣ <b>Upload data latih</b> – Klik tombol 🌸 <b>"Klik Sakura"</b> di sidebar untuk menampilkan bagian upload. 
        Upload minimal <b>10 foto wajah</b> (dari 2 orang berbeda, masing-masing 5+ foto).<br>
        2️⃣ <b>Upload dua foto uji</b> – Pilih dua foto wajah yang ingin dibandingkan di bagian bawah.<br>
        3️⃣ <b>Atur threshold</b> – Geser slider untuk menentukan batas kemiripan (default 0.70).<br>
        4️⃣ <b>Klik tombol "Proses Deteksi"</b> – Sistem akan memproses dan menampilkan skor kemiripan.<br><br>
        
        <b>💡 Hasil yang muncul:</b><br>
        • Skor kemiripan (0% – 100%)<br>
        • Kesimpulan: <b>MIRIP</b> / <b>CUKUP MIRIP</b> / <b>TIDAK MIRIP</b><br>
        • Grafik akumulasi informasi PCA<br><br>
        
        <i>✨ Pastikan foto wajah terlihat jelas dan tidak menggunakan filter agar hasil lebih akurat.</i>
    </div>
    """, unsafe_allow_html=True)

    # ---- 2. SIDEBAR: UPLOAD DATA LATIH (TOGGLE DENGAN SAKURA) ----
    with st.sidebar:
        st.markdown("---")
        st.markdown('<div class="sakura-btn-container">', unsafe_allow_html=True)
        kol1, kol2, kol3 = st.columns([1, 2, 1])
        with kol2:
            # Tombol sakura untuk toggle upload data latih
            if st.button("🌸", key="toggle_sidebar_deteksi"):
                st.session_state.show_upload = not st.session_state.show_upload
                st.rerun()
            st.caption("Klik Sakura")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Bagian upload data latih (hanya muncul jika show_upload = True)
        if st.session_state.show_upload:
            st.header("📂 Upload Data Latih")
            st.markdown("Upload **minimal 10 foto** wajah (2 orang, masing-masing 5+ foto)")
            
            # Gunakan key unik agar tidak bertabrakan dengan uploader lain
            file_latih = st.file_uploader(
                "Pilih Foto",
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True,
                key="deteksi_train"
            )
            
            if file_latih:
                st.success(f"✅ {len(file_latih)} foto berhasil terupload!")
            else:
                st.warning("⬆️ Upload foto di sini")
        else:
            st.info("🌸 Upload data latih disembunyikan. Klik sakura di atas untuk menampilkan.")
        
        st.divider()
        
        # ---- 3. SLIDER THRESHOLD ----
        ambang = st.slider("🎯 Ambang Batas Kemiripan", 0.0, 1.0, 0.70, 0.05, key="threshold_deteksi")
        st.caption(f"Threshold saat ini: **{ambang:.2f}**")
        
        st.divider()
        
        # ---- 4. ANGGOTA KELOMPOK ----
        st.markdown("""
            <b>🌸 Kelompok 2</b><br>
            1. Gea Destadia Al-Zahra<br>
            2. Luna Amilia<br>
            3. Dalilah Arifah Ariandi DJR<br>
            4. Nadia Azzizah
        """, unsafe_allow_html=True)

    # ---- 5. AREA UTAMA: UPLOAD 2 FOTO UJI ----
    st.markdown("## 🔍 Upload Dua Wajah untuk Dibandingkan")
    
    kolom1, kolom2 = st.columns(2)
    with kolom1:
        st.markdown("### 📸 Foto Pertama")
        file1 = st.file_uploader("Upload Foto 1", type=["jpg","jpeg","png"], key="f1_deteksi", label_visibility="collapsed")
    with kolom2:
        st.markdown("### 📸 Foto Kedua")
        file2 = st.file_uploader("Upload Foto 2", type=["jpg","jpeg","png"], key="f2_deteksi", label_visibility="collapsed")

    # ---- 6. TOMBOL PROSES ----
    if st.button("🚀 Proses Deteksi Sekarang", use_container_width=True):
        # Ambil file_latih dari session state (dari sidebar)
        try:
            train_files = file_latih
        except NameError:
            train_files = None
        
        # Validasi
        if not train_files or len(train_files) < 10:
            st.error("⚠️ **Data Latih Kurang!** Upload minimal 10 foto wajah terlebih dahulu.")
            st.info("💡 Klik tombol 🌸 di sidebar untuk menampilkan bagian upload data latih.")
        elif not file1 or not file2:
            st.error("⚠️ Upload kedua foto uji!")
        else:
            with st.spinner("⏳ Sedang memproses... Mohon tunggu."):
                time.sleep(0.5)
                
                # ===== FUNGSI PREPROCESSING =====
                # Deteksi wajah menggunakan Haar Cascade
                def deteksi_dan_potong_wajah(byte_gambar):
                    arr_np = np.frombuffer(byte_gambar, np.uint8)
                    img = cv2.imdecode(arr_np, cv2.IMREAD_COLOR)
                    abu = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    cascade = cv2.CascadeClassifier(
                        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
                    )
                    wajah = cascade.detectMultiScale(abu, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
                    if len(wajah) > 0:
                        x, y, w, h = max(wajah, key=lambda rect: rect[2] * rect[3])
                        return abu[y:y+h, x:x+w], True
                    return abu, False
                
                # Preprocessing: crop wajah → resize → normalisasi → flatten
                def praproses(byte_gambar, ukuran=(100, 100)):
                    potongan, _ = deteksi_dan_potong_wajah(byte_gambar)
                    resize = cv2.resize(potongan, ukuran)
                    normal = resize / 255.0
                    return normal.flatten(), resize
                
                # Muat gambar berwarna untuk ditampilkan di hasil
                def muat_warna(byte_gambar, ukuran=(100, 100)):
                    arr_np = np.frombuffer(byte_gambar, np.uint8)
                    img = cv2.imdecode(arr_np, cv2.IMREAD_COLOR)
                    abu = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    cascade = cv2.CascadeClassifier(
                        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
                    )
                    wajah = cascade.detectMultiScale(abu, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
                    if len(wajah) > 0:
                        x, y, w, h = max(wajah, key=lambda rect: rect[2] * rect[3])
                        potongan = img[y:y+h, x:x+w]
                        resize = cv2.resize(potongan, ukuran)
                        return cv2.cvtColor(resize, cv2.COLOR_BGR2RGB)
                    else:
                        resize = cv2.resize(img, ukuran)
                        return cv2.cvtColor(resize, cv2.COLOR_BGR2RGB)
                
                # ===== PROSES DATA =====
                UKURAN = (100, 100)
                X_latih = []
                progress = st.progress(0, text="Mengolah data latih...")
                for i, file in enumerate(train_files):
                    vektor, _ = praproses(file.getvalue(), UKURAN)
                    X_latih.append(vektor)
                    progress.progress((i+1)/len(train_files))
                X_latih = np.array(X_latih)
                
                # ===== JALANKAN PCA =====
                progress.progress(50, text="Menjalankan PCA & mencari Eigenfaces...")
                k = min(50, len(X_latih)-1) if len(X_latih)>1 else 1
                pca = PCA(n_components=k)
                pca.fit(X_latih)
                
                # ===== PROSES FOTO UJI =====
                progress.progress(70, text="Memproses foto uji...")
                v1, _ = praproses(file1.getvalue(), UKURAN)
                v2, _ = praproses(file2.getvalue(), UKURAN)
                img1_warna = muat_warna(file1.getvalue(), UKURAN)
                img2_warna = muat_warna(file2.getvalue(), UKURAN)
                
                # Proyeksi ke ruang PCA
                proj1 = pca.transform([v1])
                proj2 = pca.transform([v2])
                
                # Hitung Cosine Similarity
                kemiripan = cosine_similarity(proj1, proj2)[0][0]
                
                progress.progress(100, text="Selesai!")
                time.sleep(0.3)
                progress.empty()
                
                # ===== TAMPILKAN HASIL =====
                st.markdown("---")
                st.subheader("📊 Hasil Deteksi")
                
                # 3 kolom: Foto 1, Foto 2, Skor
                kolom_r1, kolom_r2, kolom_r3 = st.columns([2, 2, 1.5])
                
                with kolom_r1:
                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    st.markdown('<div class="pink-badge">📸 Foto Pertama</div>', unsafe_allow_html=True)
                    st.image(img1_warna, caption=f"Resize {UKURAN[0]}x{UKURAN[1]}", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with kolom_r2:
                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    st.markdown('<div class="pink-badge">📸 Foto Kedua</div>', unsafe_allow_html=True)
                    st.image(img2_warna, caption=f"Resize {UKURAN[0]}x{UKURAN[1]}", use_container_width=True)
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
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # ===== GRAFIK AKUMULASI INFORMASI =====
                st.subheader("📈 Grafik Akumulasi Informasi")
                varians = np.cumsum(pca.explained_variance_ratio_)
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(range(1, len(varians)+1), varians, 'bo-', linewidth=2)
                ax.axhline(y=0.95, color='r', linestyle='--', label='95% Varians')
                ax.axhline(y=ambang, color='g', linestyle=':', label=f'Threshold {ambang:.2f}')
                ax.set_xlabel('Jumlah Komponen (k)')
                ax.set_ylabel('Akumulasi Varians')
                ax.set_title('Kurva Akumulasi Informasi PCA')
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
