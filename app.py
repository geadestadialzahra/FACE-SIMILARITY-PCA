# ---------- DETEKSI KEMIRIPAN ----------
def halaman_deteksi():
    st.markdown('<h1 class="main-title">🔍 Deteksi Kemiripan Wajah</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Bandingkan dua wajah dengan metode Eigenfaces (PCA)</p>', unsafe_allow_html=True)

    # --- KOTAK PINK STATIS ---
    st.markdown("""
    <div class="static-upload-box">
        <span class="icon">📂</span>
        <p><b>Upload Data Latih (minimal 10 foto)</b></p>
        <p>Pilih minimal 10 foto wajah (2 orang, masing-masing 5+ foto)</p>
        <p style="font-size:14px; color:#AD1457;">⬆️ Upload foto di sini nanti akan muncul di bawah</p>
    </div>
    """, unsafe_allow_html=True)

    file_latih = st.file_uploader(
        "Pilih minimal 10 foto wajah (2 orang, masing-masing 5+ foto)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="train_deteksi"
    )
    if file_latih:
        st.success(f"✅ {len(file_latih)} foto terupload!")
    else:
        st.warning("⬆️ Upload foto di sini")

    col1, col2 = st.columns(2)
    with col1:
        file1 = st.file_uploader("Foto Pertama", type=["jpg","jpeg","png"], key="f1_deteksi")
    with col2:
        file2 = st.file_uploader("Foto Kedua", type=["jpg","jpeg","png"], key="f2_deteksi")

    ambang = st.slider("🎯 Ambang Batas Kemiripan", 0.0, 1.0, 0.70, 0.05, key="threshold_deteksi")

    if st.button("🚀 Proses Deteksi", use_container_width=True):
        if not file_latih or len(file_latih) < 10:
            st.error("⚠️ **Data Latih Kurang!** Upload minimal 10 foto.")
        elif not file1 or not file2:
            st.error("⚠️ Upload kedua foto uji!")
        else:
            with st.spinner("⏳ Memproses..."):
                time.sleep(0.5)

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

                def praproses(byte_gambar, ukuran=(100, 100)):
                    potongan, _ = deteksi_dan_potong_wajah(byte_gambar)
                    resize = cv2.resize(potongan, ukuran)
                    normal = resize / 255.0
                    return normal.flatten(), resize

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

                UKURAN = (100, 100)
                X_latih = []
                progress = st.progress(0)
                for i, f in enumerate(file_latih):
                    vektor, _ = praproses(f.getvalue(), UKURAN)
                    X_latih.append(vektor)
                    progress.progress((i+1)/len(file_latih))
                X_latih = np.array(X_latih)

                k = min(50, len(X_latih)-1) if len(X_latih)>1 else 1
                pca = PCA(n_components=k)
                pca.fit(X_latih)

                v1, _ = praproses(file1.getvalue(), UKURAN)
                v2, _ = praproses(file2.getvalue(), UKURAN)
                img1_warna = muat_warna(file1.getvalue(), UKURAN)
                img2_warna = muat_warna(file2.getvalue(), UKURAN)

                proj1 = pca.transform([v1])
                proj2 = pca.transform([v2])
                kemiripan = cosine_similarity(proj1, proj2)[0][0]
                progress.empty()

                # --- TAMPILKAN HASIL DETEKSI (3 KOLOM RAPI) ---
                st.markdown("---")
                st.subheader("📊 Hasil Deteksi")

                col_r1, col_r2, col_r3 = st.columns([2, 2, 1.5])

                with col_r1:
                    st.markdown(
                        f"""
                        <div style="background: linear-gradient(135deg, #FCE4EC, #FFF0F5); 
                                    border: 1px solid #F8BBD0; 
                                    border-radius: 15px; 
                                    padding: 20px; 
                                    text-align: center; 
                                    height: 100%; 
                                    box-shadow: 0 4px 15px rgba(233,30,99,0.1);">
                            <span style="display: inline-block; 
                                         background: linear-gradient(135deg, #FCE4EC, #F8BBD0); 
                                         color: #AD1457; 
                                         padding: 6px 18px; 
                                         border-radius: 20px; 
                                         font-weight: bold; 
                                         font-size: 14px; 
                                         border: 1px solid #EC407A; 
                                         margin-bottom: 10px;">📸 Foto Pertama</span>
                            <div style="display: flex; justify-content: center;">
                                <img src="data:image/png;base64,{img1_warna.tobytes().hex()}" 
                                     style="max-width:100%; border-radius:8px;" 
                                     onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22200%22 height=%22200%22%3E%3Crect width=%22200%22 height=%22200%22 fill=%22%23FCE4EC%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 text-anchor=%22middle%22 dy=%22.3em%22 fill=%22%23AD1457%22 font-size=%2216%22%3EFoto%3C/text%3E%3C/svg%3E'"/>
                            </div>
                            <p style="font-size:12px; color:#AD1457; margin-top:5px;">Resize 100x100</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col_r2:
                    st.markdown(
                        f"""
                        <div style="background: linear-gradient(135deg, #FCE4EC, #FFF0F5); 
                                    border: 1px solid #F8BBD0; 
                                    border-radius: 15px; 
                                    padding: 20px; 
                                    text-align: center; 
                                    height: 100%; 
                                    box-shadow: 0 4px 15px rgba(233,30,99,0.1);">
                            <span style="display: inline-block; 
                                         background: linear-gradient(135deg, #FCE4EC, #F8BBD0); 
                                         color: #AD1457; 
                                         padding: 6px 18px; 
                                         border-radius: 20px; 
                                         font-weight: bold; 
                                         font-size: 14px; 
                                         border: 1px solid #EC407A; 
                                         margin-bottom: 10px;">📸 Foto Kedua</span>
                            <div style="display: flex; justify-content: center;">
                                <img src="data:image/png;base64,{img2_warna.tobytes().hex()}" 
                                     style="max-width:100%; border-radius:8px;" 
                                     onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22200%22 height=%22200%22%3E%3Crect width=%22200%22 height=%22200%22 fill=%22%23FCE4EC%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 text-anchor=%22middle%22 dy=%22.3em%22 fill=%22%23AD1457%22 font-size=%2216%22%3EFoto%3C/text%3E%3C/svg%3E'"/>
                            </div>
                            <p style="font-size:12px; color:#AD1457; margin-top:5px;">Resize 100x100</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col_r3:
                    st.markdown(
                        f"""
                        <div style="background: linear-gradient(135deg, #FCE4EC, #FFF0F5); 
                                    border: 1px solid #F8BBD0; 
                                    border-radius: 15px; 
                                    padding: 20px; 
                                    text-align: center; 
                                    height: 100%; 
                                    box-shadow: 0 4px 15px rgba(233,30,99,0.1);">
                            <span style="display: inline-block; 
                                         background: linear-gradient(135deg, #FCE4EC, #F8BBD0); 
                                         color: #AD1457; 
                                         padding: 6px 18px; 
                                         border-radius: 20px; 
                                         font-weight: bold; 
                                         font-size: 14px; 
                                         border: 1px solid #EC407A; 
                                         margin-bottom: 10px;">🎯 Skor Kemiripan</span>
                            <h1 style="color:#AD1457; font-size:42px; margin:5px 0;">{kemiripan:.2%}</h1>
                            <div style="margin:10px 0;">
                                {"✅ **MIRIP**" if kemiripan >= ambang else "⚠️ **CUKUP MIRIP**" if kemiripan >= 0.50 else "❌ **TIDAK MIRIP**"}
                            </div>
                            <p style="font-size:12px; color:#6A1B4D; margin:2px 0;">Komponen PCA: {k}</p>
                            <p style="font-size:12px; color:#6A1B4D; margin:2px 0;">Varians: {np.sum(pca.explained_variance_ratio_)*100:.1f}%</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # --- GRAFIK AKUMULASI INFORMASI ---
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
