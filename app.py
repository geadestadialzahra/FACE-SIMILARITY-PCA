# ==========================================
# 5. NAVIGASI SIDEBAR (TOMBOL BLOK WARNA - DIPERBESAR)
# ==========================================
st.sidebar.markdown("🌸 **Haloo!!**")

# Daftar menu
menus = [
    ("🏠", "🏠 Home"),
    ("🌫️", "🌫️ Grayscale"),
    ("🗜️", "🗜️ Kompresi"),
    ("🔍", "🔍 Deteksi Kemiripan")
]

# Buat 4 kolom untuk tombol
cols = st.sidebar.columns(4)

for col, (emoji, page_name) in zip(cols, menus):
    with col:
        is_active = (st.session_state.page == page_name)
        
        # Tombol aktif: background pink + sedikit membesar
        if is_active:
            st.markdown(f"""
                <style>
                    .stSidebar .stButton button[data-testid="baseButton-secondary"]:has(> div:contains("{emoji}")) {{
                        background: #F8BBD0 !important;
                        box-shadow: 0 0 15px rgba(236, 64, 122, 0.15) !important;
                        border: none !important;
                        transform: scale(1.12) !important;
                        transition: all 0.3s ease !important;
                    }}
                </style>
            """, unsafe_allow_html=True)
        
        if st.button(emoji, key=f"nav_{emoji}", use_container_width=True):
            st.session_state.page = page_name
            st.rerun()

st.sidebar.markdown("---")
if st.session_state.page == "🏠 Home":
    st.sidebar.markdown('<p class="sidebar-caption">📌 Beranda & Profil</p>', unsafe_allow_html=True)
elif st.session_state.page == "🌫️ Grayscale":
    st.sidebar.markdown('<p class="sidebar-caption">🌫️ Ubah ke hitam-putih</p>', unsafe_allow_html=True)
elif st.session_state.page == "🗜️ Kompresi":
    st.sidebar.markdown('<p class="sidebar-caption">🗜️ Kompresi dengan PCA</p>', unsafe_allow_html=True)
elif st.session_state.page == "🔍 Deteksi Kemiripan":
    st.sidebar.markdown('<p class="sidebar-caption">🔍 Bandingkan dua wajah</p>', unsafe_allow_html=True)
