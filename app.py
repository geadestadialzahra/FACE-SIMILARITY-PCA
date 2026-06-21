elif page == "🔍 Deteksi":
    # ==================== DETEKSI KEMIRIPAN DENGAN PCA (EIGENFACES) + COSINE SIMILARITY ====================
    if not st.session_state.deteksi_visited:
        st.balloons()
        st.session_state.deteksi_visited = True

    st.markdown("""
    <div class="deteksi-header">
        <div class="love-shower">❤️ 💖 ❤️ 💖 ❤️ 💖 ❤️ 💖 ❤️ 💖 ❤️ 💖</div>
        <h1>🔍 Deteksi Kemiripan Wajah</h1>
        <p>Bandingkan dua wajah dengan metode PCA (Eigenfaces) dan Cosine Similarity.</p>
        <div class="love-shower">❤️ 💖 ❤️ 💖 ❤️ 💖 ❤️ 💖 ❤️ 💖 ❤️ 💖</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: linear-gradient(135deg, #FCE4EC, #FFF0F5); 
                padding: 1.5rem; border-radius: 16px; border: 1px solid #F8BBD0; 
                margin-bottom: 2rem; text-align: center;">
        <p style="font-size:1.2rem; color:#6A1B4D;">
            ❤️ <b>Cara kerja:</b> PCA mengekstrak fitur utama (eigenfaces) dari data latih (wajah). 
            Dua wajah yang dibandingkan diproyeksikan ke ruang PCA, lalu dihitung kemiripannya dengan <b>Cosine Similarity</b>.
            Semakin tinggi skor, semakin mirip kedua wajah.
        </p>
        <p style="color:#880E4F; font-style:italic;">
            "Setiap wajah unik, tapi kecocokan bisa ditemukan."
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Upload dua gambar
    col_upload1, col_upload2 = st.columns(2)
    with col_upload1:
        img1 = st.file_uploader("📤 Foto Pertama", type=["jpg", "jpeg", "png"], key="img1")
    with col_upload2:
        img2 = st.file_uploader("📤 Foto Kedua", type=["jpg", "jpeg", "png"], key="img2")

    # Upload data latih (opsional)
    st.markdown("---")
    st.markdown("#### 📂 Data Latih (Opsional)")
    st.markdown("Upload folder berisi gambar wajah untuk melatih PCA. Jika tidak diisi, akan digunakan dua gambar yang dibandingkan (dengan PCA 1 komponen).")
    uploaded_zip = st.file_uploader("Unggah file ZIP berisi gambar wajah", type=["zip"], key="train_zip")

    # Parameter
    col_param1, col_param2 = st.columns(2)
    with col_param1:
        n_components = st.slider(
            "Jumlah komponen PCA (k)",
            min_value=1,
            max_value=50,
            value=9,
            step=1,
            help="Semakin banyak komponen, semakin detail fitur wajah yang digunakan. (Jika tanpa data latih, k=1)"
        )
    with col_param2:
        threshold = st.slider(
            "Threshold (batas kemiripan %)",
            min_value=0,
            max_value=100,
            value=70,
            step=5,
            help="Jika skor kemiripan ≥ threshold, dianggap mirip."
        ) / 100.0

    if img1 is not None and img2 is not None:
        # Tampilkan dua gambar
        col_show1, col_show2 = st.columns(2)
        with col_show1:
            st.image(img1, caption="Foto Pertama", use_container_width=True)
        with col_show2:
            st.image(img2, caption="Foto Kedua", use_container_width=True)

        if st.button("🔎 Hitung Kemiripan", use_container_width=True):
            try:
                # Baca dan resize gambar ke ukuran yang sama (misal 100x100)
                size = (100, 100)
                im1 = Image.open(img1).convert("L").resize(size)
                im2 = Image.open(img2).convert("L").resize(size)
                arr1 = np.array(im1, dtype=np.float32).flatten() / 255.0
                arr2 = np.array(im2, dtype=np.float32).flatten() / 255.0

                # Siapkan data latih
                train_vectors = []
                use_zip = False

                if uploaded_zip is not None:
                    # Ekstrak zip
                    with tempfile.TemporaryDirectory() as tmpdir:
                        with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
                            zip_ref.extractall(tmpdir)
                        # Baca semua gambar di folder
                        for root, _, files in os.walk(tmpdir):
                            for file in files:
                                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                                    try:
                                        img_path = os.path.join(root, file)
                                        img = Image.open(img_path).convert("L").resize(size)
                                        vec = np.array(img, dtype=np.float32).flatten() / 255.0
                                        train_vectors.append(vec)
                                    except:
                                        continue
                    if len(train_vectors) >= 2:
                        use_zip = True
                        st.success(f"✅ Data latih berhasil dimuat! Jumlah gambar: {len(train_vectors)}")
                    else:
                        st.warning("Data latih kurang dari 2 gambar. Gunakan data latih default.")
                
                # Jika tidak ada data latih atau kurang, gunakan dua gambar sebagai data latih
                if not use_zip:
                    # Data latih hanya dua gambar, maka PCA hanya bisa 1 komponen
                    n_components_actual = 1
                    train_vectors = np.array([arr1, arr2])
                    st.info(f"ℹ️ Tidak ada data latih yang cukup. Gunakan 2 gambar sebagai data latih dengan k=1.")
                else:
                    # Gunakan data latih dari zip, batasi n_components sesuai jumlah sampel
                    n_components_actual = min(n_components, len(train_vectors)-1, len(train_vectors[0]))
                    train_vectors = np.array(train_vectors)
                    if n_components_actual < n_components:
                        st.warning(f"Jumlah komponen dibatasi menjadi {n_components_actual} karena data latih hanya {len(train_vectors)} gambar.")

                # PCA
                pca = PCA(n_components=n_components_actual)
                pca.fit(train_vectors)
                # Proyeksikan dua gambar
                vec1_pca = pca.transform([arr1])[0]
                vec2_pca = pca.transform([arr2])[0]
                # Cosine similarity
                sim = cosine_similarity([vec1_pca], [vec2_pca])[0][0]
                persentase = sim * 100
                var_ratio = pca.explained_variance_ratio_.sum() * 100

                # Tampilkan hasil
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="score">{persentase:.2f}%</div>', unsafe_allow_html=True)
                if persentase >= threshold * 100:
                    st.markdown(f'<div class="label">✅ MIRIP! (≥ {threshold*100:.0f}%)</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="label">❌ TIDAK MIRIP (< {threshold*100:.0f}%)</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="detail">Komponen PCA: {pca.n_components}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="detail">Varians: {var_ratio:.1f}%</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Grafik akumulasi informasi PCA (hanya jika data latih > 2)
                if len(train_vectors) > 2:
                    st.markdown("### 📈 Grafik Akumulasi Informasi PCA")
                    cumsum_var = np.cumsum(pca.explained_variance_ratio_)
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.plot(range(1, len(cumsum_var)+1), cumsum_var, 'b-', linewidth=2, label='Kurva Akumulasi')
                    ax.axhline(y=0.95, color='r', linestyle='--', alpha=0.7, label='95% Varians')
                    ax.axhline(y=threshold, color='g', linestyle='--', alpha=0.7, label=f'Threshold {threshold*100:.0f}%')
                    ax.axvline(x=pca.n_components, color='orange', linestyle=':', alpha=0.7, label=f'k = {pca.n_components}')
                    ax.set_xlabel('Jumlah Komponen (k)')
                    ax.set_ylabel('Akumulasi Varians')
                    ax.set_title('Kurva Akumulasi Informasi PCA')
                    ax.grid(True, alpha=0.3)
                    ax.legend()
                    st.pyplot(fig)
                    plt.close(fig)

                    # Penjelasan grafik
                    st.markdown("""
                    <div style="background: #FCE4EC; padding: 1rem; border-radius: 12px; margin-top: 1rem; border: 1px solid #EC407A;">
                        <p style="margin:0;"><b>💡 Cara baca grafik:</b><br>
                        • <b>Garis biru</b> → akumulasi varians. Semakin tinggi, semakin banyak informasi yang dipertahankan.<br>
                        • <b>Garis merah putus-putus</b> → 95% varians data sudah terwakili.<br>
                        • <b>Garis hijau putus-putus</b> → threshold kemiripan yang Anda atur.<br>
                        • <b>Garis oranye</b> → jumlah komponen PCA yang digunakan (k).<br>
                        Dengan k yang cukup, kita bisa meringkas wajah menjadi beberapa angka tanpa kehilangan banyak informasi.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                st.balloons()

            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
    else:
        st.info("👆 Upload dua foto wajah untuk membandingkan.")

    # --- KETERANGAN TAMBAHAN DI BAWAH DETEKSI ---
    st.markdown("""
    <div class="footer-note">
        <p>📌 <b>Keterangan:</b> Deteksi kemiripan menggunakan PCA (Eigenfaces) dan Cosine Similarity. 
        Upload data latih (ZIP) untuk hasil lebih akurat. Jika tidak ada, sistem menggunakan 2 gambar dengan k=1 (hasil 100% untuk gambar identik).</p>
    </div>
    """, unsafe_allow_html=True)
