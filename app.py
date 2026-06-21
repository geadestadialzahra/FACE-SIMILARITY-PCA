import streamlit as st
from PIL import Image, ImageDraw
import io
import base64

st.set_page_config(
    page_title="LANG APP",
    page_icon="🌸",
    layout="wide"
)

# ======================== CSS GLOBAL ========================
st.markdown("""
    <style>
        /* ----- BACKGROUND UTAMA ----- */
        .stApp, .main, .block-container, section.main, div[data-testid="stSidebar"] {
            background-color: #FFF0F5 !important;
            background-image: none !important;
        }
        body, p, div, span, label, h1, h2, h3, h4, h5, h6, .stMarkdown, .stText, .stCaption {
            color: #6A1B4D !important;
        }
        header {
            background: linear-gradient(135deg, #880E4F, #AD1457) !important;
            border-bottom: 2px solid #F8BBD0 !important;
        }
        header * {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }
        .css-1d391kg, .css-12w0qpk, [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FCE4EC, #FFF0F5) !important;
            border-right: 2px solid #F8BBD0 !important;
        }
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
        h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
            color: #AD1457 !important;
            font-weight: bold !important;
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
        div[data-testid="stFileUploader"] {
            background: linear-gradient(135deg, #FCE4EC, #FFF0F5) !important;
            border: 2px dashed #EC407A !important;
            border-radius: 12px !important;
            padding: 10px !important;
        }
        div[data-testid="stFileUploader"] > div {
            background: rgba(255, 255, 255, 0.6) !important;
            border-radius: 8px !important;
            padding: 20px !important;
        }
        div[data-testid="stFileUploader"] * {
            color: #6A1B4D !important;
            background: transparent !important;
        }
        div[data-testid="stFileUploader"] button {
            background: linear-gradient(135deg, #EC407A, #D81B60) !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
            padding: 5px 20px !important;
        }
        div[data-testid="stFileUploader"] button:hover {
            transform: scale(1.05) !important;
        }
        div[data-testid="stFileUploader"]:hover {
            border-color: #D81B60 !important;
        }
        .stSlider > div {
            background: rgba(255, 255, 255, 0.4) !important;
            border-radius: 10px !important;
        }
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
        .result-card {
            background: linear-gradient(135deg, #FCE4EC, #FFF0F5) !important;
            padding: 20px !important;
            border-radius: 15px !important;
            text-align: center !important;
            border: 1px solid #F8BBD0 !important;
            box-shadow: 0 4px 15px rgba(233, 30, 99, 0.1) !important;
            height: 100% !important;
        }
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
            font-size: 60px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 !important;
            margin: 0 auto !important;
            box-shadow: none !important;
            transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
            line-height: 1 !important;
        }
        .stSidebar .stButton button:hover {
            transform: scale(1.06) !important;
            background: rgba(236, 64, 122, 0.06) !important;
            box-shadow: 0 0 12px rgba(236, 64, 122, 0.08) !important;
        }
        .sidebar-caption {
            text-align: center;
            color: #AD1457;
            font-weight: bold;
            font-size: 15px;
            padding-top: 5px;
        }

        /* ----- PROFIL TIM ----- */
        .profile-card {
            background: white;
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(173,20,87,0.1);
            border: 1px solid #F8BBD0;
        }
        .profile-card h3 {
            color: #AD1457;
            text-align: center;
            margin-bottom: 1rem;
        }
        .profile-item {
            display: flex;
            align-items: center;
            margin-bottom: 0.8rem;
            padding: 0.5rem;
            border-radius: 12px;
            background: #FFF5F8;
        }
        .profile-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(135deg, #EC407A, #D81B60);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 20px;
            margin-right: 15px;
            flex-shrink: 0;
        }
        .profile-info {
            flex: 1;
        }
        .profile-info .name {
            font-weight: bold;
            color: #6A1B4D;
        }
        .profile-info .detail {
            font-size: 0.85rem;
            color: #880E4F;
        }

        /* ----- GAYA KHUSUS GRAYSCALE (bunga & header) ----- */
        .grayscale-header {
            text-align: center;
            padding: 1.5rem 0 0.5rem 0;
            background: linear-gradient(135deg, #FCE4EC, #FFF0F5);
            border-radius: 20px;
            margin-bottom: 2rem;
            border: 1px solid #F8BBD0;
        }
        .grayscale-header h1 {
            font-size: 2.8rem;
            color: #AD1457;
            margin: 0;
            font-weight: 800;
            text-shadow: 2px 2px 10px rgba(173,20,87,0.2);
        }
        .grayscale-header p {
            font-size: 1.1rem;
            color: #6A1B4D;
            margin: 0.3rem 0 1rem 0;
        }
        .flower-shower {
            font-size: 2rem;
            letter-spacing: 6px;
            color: #EC407A;
            animation: twinkle 2s infinite alternate;
        }
        @keyframes twinkle {
            0% { opacity: 0.6; transform: scale(1); }
            100% { opacity: 1; transform: scale(1.05); }
        }

        /* ----- GAYA UMUM KONTEN ----- */
        .content-card {
            background: white;
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(173,20,87,0.08);
            border: 1px solid #F8BBD0;
        }
        .content-card h2 {
            color: #AD1457;
            margin-top: 0;
        }
        .image-card {
            background: white;
            border-radius: 16px;
            padding: 1rem;
            box-shadow: 0 4px 12px rgba(173,20,87,0.1);
            border: 1px solid #F8BBD0;
            margin: 0.5rem 0;
        }
        .image-card img {
            border-radius: 12px;
            border: 2px solid #F8BBD0;
            width: 100%;
        }
        .download-btn {
            background: linear-gradient(135deg, #EC407A, #D81B60);
            color: white;
            border: none;
            border-radius: 50px;
            padding: 0.6rem 2rem;
            font-weight: bold;
            transition: 0.3s;
            box-shadow: 0 4px 15px rgba(233,30,99,0.3);
            cursor: pointer;
        }
        .download-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 25px rgba(233,30,99,0.4);
        }
        .info-box {
            background: rgba(255,255,255,0.7);
            border-left: 5px solid #EC407A;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin-top: 1.5rem;
            box-shadow: 0 2px 10px rgba(233,30,99,0.08);
        }
        .info-box b {
            color: #AD1457;
        }
        .university {
            text-align: center;
            padding: 1rem 0;
            color: #AD1457;
            font-weight: bold;
            font-size: 1.2rem;
            border-top: 2px solid #F8BBD0;
            margin-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ======================== SESSION STATE ========================
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"
if "grayscale_visited" not in st.session_state:
    st.session_state.grayscale_visited = False
if "download_done" not in st.session_state:
    st.session_state.download_done = False

# ======================== SIDEBAR NAVIGASI ========================
st.sidebar.markdown("🌸 **Haloo!!**")
menus = [
    ("🏠", "🏠 Home"),
    ("🌫️", "🌫️ Grayscale"),
    ("🗜️", "🗜️ Kompresi"),
    ("🔍", "🔍 Deteksi Kemiripan")
]

cols = st.sidebar.columns(4)
for col, (emoji, page_name) in zip(cols, menus):
    with col:
        is_active = (st.session_state.page == page_name)
        if is_active:
            st.markdown(f"""
                <style>
                    .stSidebar .stButton button[data-testid="baseButton-secondary"]:has(> div:contains("{emoji}")) {{
                        background: #F8BBD0 !important;
                        transform: translateY(2px) scale(1.03) !important;
                        box-shadow: 0 4px 14px rgba(236,64,122,0.25) !important;
                        border: none !important;
                    }}
                </style>
            """, unsafe_allow_html=True)
        if st.button(emoji, key=f"nav_{emoji}", use_container_width=True):
            st.session_state.page = page_name
            if page_name == "🌫️ Grayscale":
                st.session_state.grayscale_visited = False
            st.rerun()

st.sidebar.markdown("---")
if st.session_state.page == "🏠 Home":
    st.sidebar.markdown('<p class="sidebar-caption">📌 Beranda & Profil</p>', unsafe_allow_html=True)
elif st.session_state.page == "🌫️ Grayscale":
    st.sidebar.markdown('<p class="sidebar-caption">🌫️ Ubah ke hitam-putih</p>', unsafe_allow_html=True)
elif st.session_state.page == "🗜️ Kompresi":
    st.sidebar.markdown('<p class="sidebar-caption">🗜️ Kompresi dengan PCA</p>', unsafe_allow_html=True)
elif st.session_state.page == "🔍 Deteksi Kemiripan":
    st.sidebar.markdown('<p class="sidebar-caption">🔍 Cari kemiripan</p>', unsafe_allow_html=True)

# ======================== FUNGSI PROFIL TIM ========================
def tampilkan_profil():
    """Menampilkan kartu profil tim di kolom kiri."""
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    st.markdown("### 👥 Tim Pengembang")
    st.markdown("**Teknik Informatika**")

    # Data anggota (ganti dengan data asli kalian)
    anggota = [
        {"nama": "Andi Pratama", "ig": "@andi_p", "telp": "0812-3456-7890"},
        {"nama": "Budi Santoso", "ig": "@budi_s", "telp": "0813-4567-8901"},
        {"nama": "Citra Dewi", "ig": "@citra_d", "telp": "0814-5678-9012"},
        {"nama": "Dian Sastro", "ig": "@dian_s", "telp": "0815-6789-0123"},
    ]

    for member in anggota:
        inisial = ''.join([kata[0] for kata in member["nama"].split()])
        st.markdown(f"""
        <div class="profile-item">
            <div class="profile-avatar">{inisial}</div>
            <div class="profile-info">
                <div class="name">{member['nama']}</div>
                <div class="detail">📸 {member['ig']}</div>
                <div class="detail">📞 {member['telp']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Universitas selalu di bawah profil
    st.markdown('<div class="university">🎓 Universitas Negeri Semarang</div>', unsafe_allow_html=True)


# ======================== HALAMAN ========================
page = st.session_state.page

# Layout dua kolom: kiri (profil) 1/4, kanan (konten) 3/4
col_left, col_right = st.columns([1, 3], gap="large")

with col_left:
    tampilkan_profil()

with col_right:
    if page == "🏠 Home":
        # ---------- HOME ----------
        st.markdown("""
        <div class="content-card">
            <h2>🌸 Selamat Datang di Aplikasi LANG</h2>
            <p style="font-size:1.1rem;">
                Aplikasi ini dirancang untuk membantu Anda mengolah gambar dengan mudah dan cepat.
            </p>
            <p>
                <b>Fitur unggulan:</b><br>
                • <b>🌫️ Grayscale</b> – Ubah gambar menjadi hitam-putih untuk efek artistik dan penghematan ukuran.<br>
                • <b>🗜️ Kompresi PCA</b> – Reduksi dimensi gambar menggunakan Principal Component Analysis, menjaga kualitas visual dengan ukuran lebih kecil.<br>
                • <b>🔍 Deteksi Kemiripan</b> – Bandingkan dua gambar dan dapatkan skor kemiripan secara otomatis.
            </p>
            <p>
                <b>Manfaat:</b><br>
                ✅ Menghemat ruang penyimpanan.<br>
                ✅ Mempermudah analisis visual.<br>
                ✅ Hasil cepat dan akurat.
            </p>
            <p style="color:#880E4F; font-style:italic;">
                "Teknologi untuk kreativitas tanpa batas."
            </p>
        </div>
        """, unsafe_allow_html=True)

    elif page == "🌫️ Grayscale":
        # ---------- GRAYSCALE ----------
        # Efek bunga + balloons saat pertama kali masuk
        if not st.session_state.grayscale_visited:
            st.balloons()
            st.session_state.grayscale_visited = True

        # Header dengan semburan bunga
        st.markdown("""
        <div class="grayscale-header">
            <div class="flower-shower">🌸 🌺 🌷 🌹 🌻 🌼 🌸 🌺 🌷 🌹 🌻 🌼</div>
            <h1>🌫️ Konversi ke Grayscale</h1>
            <p>Ubah warna menjadi cerita hitam-putih yang abadi.</p>
            <div class="flower-shower">🌸 🌺 🌷 🌹 🌻 🌼 🌸 🌺 🌷 🌹 🌻 🌼</div>
        </div>
        """, unsafe_allow_html=True)

        # Deskripsi keren di tengah
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FCE4EC, #FFF0F5); 
                    padding: 1.5rem; border-radius: 16px; border: 1px solid #F8BBD0; 
                    margin-bottom: 2rem; text-align: center;">
            <p style="font-size:1.2rem; color:#6A1B4D;">
                🌟 <b>Grayscale</b> adalah seni mengubah spektrum warna menjadi gradasi abu-abu yang elegan. 
                Setiap piksel bercerita tentang kontras, tekstur, dan emosi – tanpa gangguan warna.
            </p>
            <p style="color:#880E4F; font-style:italic;">
                "Terkadang, hitam-putih justru lebih hidup."
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Uploader
        uploaded_file = st.file_uploader(
            "📤 Unggah gambar (JPG, PNG, WEBP)",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=False
        )

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            col_img1, col_img2 = st.columns(2, gap="medium")

            with col_img1:
                st.markdown('<div class="image-card">', unsafe_allow_html=True)
                st.markdown("### 🖼️ Gambar Asli")
                st.image(image, use_container_width=True)
                st.markdown(f"*Ukuran: {image.width} x {image.height} px*")
                st.markdown('</div>', unsafe_allow_html=True)

            with col_img2:
                if st.button("🔄 Konversi ke Grayscale", use_container_width=True):
                    gray_image = image.convert("L")
                    gray_rgb = gray_image.convert("RGB")

                    st.markdown('<div class="image-card">', unsafe_allow_html=True)
                    st.markdown("### ⚫ Hasil Grayscale")
                    st.image(gray_rgb, use_container_width=True)
                    st.markdown(f"*Ukuran: {gray_rgb.width} x {gray_rgb.height} px*")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Tombol download
                    buf = io.BytesIO()
                    gray_rgb.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    b64 = base64.b64encode(byte_im).decode()
                    href = f'<a href="data:image/png;base64,{b64}" download="grayscale.png" style="text-decoration:none;">'
                    href += '<button class="download-btn">⬇️ Download Hasil</button></a>'
                    st.markdown(href, unsafe_allow_html=True)

                    # Pesan sukses + balloons
                    st.success("🌸 Semoga membantu, terima kasih banyak telah menggunakan jasa layanan kami, salam cinta ❤️")
                    st.balloons()

                    # Manfaat
                    st.markdown("""
                    <div class="info-box">
                        <b>💡 Manfaat Grayscale:</b><br>
                        • Mengurangi kompleksitas warna, fokus pada bentuk dan tekstur.<br>
                        • Menghemat ruang penyimpanan (ukuran file lebih kecil).<br>
                        • Memberikan nuansa artistik dan klasik pada foto.
                    </div>
                    """, unsafe_allow_html=True)

        else:
            # Placeholder jika belum upload
            st.markdown("""
            <div style="text-align:center; padding:2rem 0;">
                <p style="font-size:1.2rem; color:#6A1B4D;">👆 Unggah gambar untuk mulai mengubahnya menjadi hitam-putih</p>
                <p style="color:#AD1457; opacity:0.7;">Atau lihat contoh di bawah ini:</p>
            </div>
            """, unsafe_allow_html=True)

            # Contoh gambar kotak warna-warni
            example_img = Image.new('RGB', (400, 300), color='#FCE4EC')
            draw = ImageDraw.Draw(example_img)
            draw.rectangle([50, 50, 150, 150], fill='#EC407A')
            draw.rectangle([200, 50, 300, 150], fill='#42A5F5')
            draw.rectangle([50, 180, 150, 280], fill='#66BB6A')
            draw.rectangle([200, 180, 300, 280], fill='#FFA726')
            st.image(example_img, caption="Contoh gambar (unggah gambar Anda sendiri untuk hasil nyata)", use_container_width=True)

    elif page == "🗜️ Kompresi":
        # ---------- KOMPRESI (PCA) ----------
        st.markdown("""
        <div class="content-card">
            <h2>🗜️ Kompresi Gambar dengan PCA</h2>
            <p>
                <b>Principal Component Analysis (PCA)</b> adalah teknik reduksi dimensi yang dapat 
                mengecilkan ukuran gambar dengan tetap mempertahankan informasi penting. 
                Semakin rendah komponen yang digunakan, semakin besar kompresi, namun kualitas visual 
                akan menurun secara bertahap.
            </p>
            <p style="color:#880E4F; font-style:italic;">
                "Kecilkan ukuran, pertahankan esensi."
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Upload gambar
        uploaded_file = st.file_uploader(
            "📤 Unggah gambar untuk dikompresi",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=False
        )

        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert("RGB")
            # Konversi ke array numpy (sederhana)
            import numpy as np
            img_array = np.array(image)
            h, w, c = img_array.shape

            # Slider untuk jumlah komponen PCA
            n_components = st.slider(
                "Jumlah komponen PCA (semakin kecil, semakin besar kompresi)",
                min_value=10,
                max_value=min(h, w, 200),
                value=min(h, w, 100),
                step=10
            )

            if st.button("🚀 Kompresi dengan PCA", use_container_width=True):
                # Proses PCA sederhana (ambil rata-rata channel atau gunakan SVD)
                # Untuk demo, kita lakukan PCA pada setiap channel
                from sklearn.decomposition import PCA
                pca = PCA(n_components=n_components)
                
                # Reshape agar setiap piksel menjadi vektor fitur
                flat_img = img_array.reshape(-1, c)
                # Terapkan PCA
                reduced = pca.fit_transform(flat_img)
                # Rekonstruksi
                reconstructed = pca.inverse_transform(reduced)
                # Kembalikan ke bentuk gambar
                compressed_img = reconstructed.reshape(h, w, c).astype(np.uint8)
                compressed_pil = Image.fromarray(compressed_img)

                # Tampilkan hasil
                col_ori, col_comp = st.columns(2)
                with col_ori:
                    st.markdown('<div class="image-card">', unsafe_allow_html=True)
                    st.markdown("### 🖼️ Gambar Asli")
                    st.image(image, use_container_width=True)
                    st.markdown(f"*Ukuran: {w} x {h} px*")
                    st.markdown('</div>', unsafe_allow_html=True)

                with col_comp:
                    st.markdown('<div class="image-card">', unsafe_allow_html=True)
                    st.markdown(f"### 🗜️ Hasil Kompresi (n={n_components})")
                    st.image(compressed_pil, use_container_width=True)
                    st.markdown(f"*Ukuran: {w} x {h} px*")
                    st.markdown('</div>', unsafe_allow_html=True)

                # Tombol download hasil kompresi
                buf = io.BytesIO()
                compressed_pil.save(buf, format="PNG")
                byte_im = buf.getvalue()
                b64 = base64.b64encode(byte_im).decode()
                href = f'<a href="data:image/png;base64,{b64}" download="compressed_pca.png" style="text-decoration:none;">'
                href += '<button class="download-btn">⬇️ Download Hasil Kompresi</button></a>'
                st.markdown(href, unsafe_allow_html=True)

                # Info manfaat kompresi
                st.markdown("""
                <div class="info-box">
                    <b>💡 Manfaat Kompresi PCA:</b><br>
                    • Mengurangi ukuran file secara signifikan.<br>
                    • Mempercepat transfer dan penyimpanan data.<br>
                    • Tetap mempertahankan fitur utama gambar.
                </div>
                """, unsafe_allow_html=True)

        else:
            st.info("👆 Unggah gambar untuk memulai kompresi.")

    elif page == "🔍 Deteksi Kemiripan":
        # ---------- DETEKSI KEMIRIPAN ----------
        st.markdown("""
        <div class="content-card">
            <h2>🔍 Deteksi Kemiripan Gambar</h2>
            <p>
                Bandingkan dua gambar dan dapatkan skor kemiripan berdasarkan 
                <b>Structural Similarity Index (SSIM)</b> atau <b>Mean Squared Error (MSE)</b>.
                Semakin tinggi skor SSIM (mendekati 1), semakin mirip kedua gambar.
            </p>
            <p style="color:#880E4F; font-style:italic;">
                "Temukan koneksi visual di antara dua gambar."
            </p>
        </div>
        """, unsafe_allow_html=True)

        col_upload1, col_upload2 = st.columns(2)
        with col_upload1:
            img1 = st.file_uploader("📤 Gambar pertama", type=["jpg", "jpeg", "png"], key="img1")
        with col_upload2:
            img2 = st.file_uploader("📤 Gambar kedua", type=["jpg", "jpeg", "png"], key="img2")

        if img1 is not None and img2 is not None:
            image1 = Image.open(img1).convert("RGB")
            image2 = Image.open(img2).convert("RGB")

            # Resize ke ukuran yang sama untuk perbandingan
            size = (300, 300)
            im1 = image1.resize(size)
            im2 = image2.resize(size)

            col_show1, col_show2 = st.columns(2)
            with col_show1:
                st.image(im1, caption="Gambar 1", use_container_width=True)
            with col_show2:
                st.image(im2, caption="Gambar 2", use_container_width=True)

            if st.button("🔎 Hitung Kemiripan", use_container_width=True):
                try:
                    import numpy as np
                    from skimage.metrics import structural_similarity as ssim
                    from skimage.metrics import mean_squared_error

                    arr1 = np.array(im1)
                    arr2 = np.array(im2)

                    # Konversi ke grayscale untuk SSIM
                    gray1 = np.mean(arr1, axis=2).astype(np.float32) / 255.0
                    gray2 = np.mean(arr2, axis=2).astype(np.float32) / 255.0

                    ssim_score = ssim(gray1, gray2, data_range=1.0)
                    mse_score = mean_squared_error(gray1, gray2)

                    st.success(f"✅ Skor Kemiripan (SSIM): **{ssim_score:.4f}** (semakin mendekati 1 = semakin mirip)")
                    st.info(f"📊 Mean Squared Error (MSE): **{mse_score:.6f}** (semakin kecil = semakin mirip)")

                    if ssim_score > 0.8:
                        st.balloons()
                        st.markdown("🌸 **Gambar sangat mirip!** Terima kasih telah menggunakan layanan kami. Salam cinta ❤️")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
        else:
            st.info("👆 Unggah dua gambar untuk membandingkannya.")
