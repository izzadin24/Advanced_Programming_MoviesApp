import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==========================================
# 1. SETUP HALAMAN & CSS KEREN
# ==========================================
st.set_page_config(page_title="Movie Analytics Pro", layout="wide", page_icon="🍿")

# CSS Custom untuk UI "Mahal" (Dark Mode Friendly)
st.markdown("""
<style>
    /* Mengubah Card Metric jadi kotak elegan */
    div[data-testid="stMetric"] {
        background-color: #262730;
        border: 1px solid #464b5c;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }
    div[data-testid="stMetricLabel"] { font-size: 14px; color: #b0b0b0; }
    div[data-testid="stMetricValue"] { font-size: 28px; font-weight: bold; color: #ffffff; }
    .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOAD DATA (ROBUST / ANTI ERROR)
# ==========================================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data', 'raw', 'Top_Rated_Movies.csv')
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # Bersihkan tanggal agar bisa jadi grafik waktu
        if 'release_date' in df.columns:
            df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
            df['year'] = df['release_date'].dt.year
        return df
    return None

df = load_data()

if df is None:
    st.error("❌ Data tidak ditemukan. Cek folder data/raw!")
    st.stop()

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.header("🍿 Movie Dashboard")
st.sidebar.write("Pilih modul analisis:")

menu = st.sidebar.radio(
    "",
    [
        "🏠 Home Dashboard",
        "🏆 Top Charts (Leaderboard)", 
        "📈 Tren & Statistik", 
        "🔍 Movie Search Engine"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Aplikasi Visualisasi Data Film TMDB.")

# ==========================================
# SECTION 1: HOME (BRIEF DATA)
# ==========================================
if menu == "🏠 Home Dashboard":
    st.title("Executive Summary")
    st.markdown("Ringkasan performa database film saat ini.")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Film", f"{len(df):,}")
    with col2:
        col_vote = 'vote_count' if 'vote_count' in df.columns else df.columns[3]
        total_votes = df[col_vote].sum()
        st.metric("Total User Votes", f"{total_votes/1000000:.1f} M+")
    with col3:
        col_rating = 'vote_average' if 'vote_average' in df.columns else df.columns[2]
        avg_rt = df[col_rating].mean()
        st.metric("Avg Quality Rating", f"{avg_rt:.1f} / 10")
    with col4:
        st.metric("Data Update", "Dec 2025")

    st.markdown("---")
    st.subheader("💡 Quick Insights")
    st.info("Gunakan menu di samping untuk melihat grafik tren dan pencarian detail.")

# ==========================================
# SECTION 2: TOP CHARTS (LEADERBOARD) - SUDAH DIPERBAIKI
# ==========================================
elif menu == "🏆 Top Charts (Leaderboard)":
    st.title("🏆 Hall of Fame")
    st.write("Daftar film terbaik berdasarkan kategori.")
    
    tab1, tab2 = st.tabs(["⭐ Top Rated (Kualitas)", "🔥 Most Popular (Viral)"])
    
    # === TAB 1: TOP RATED ===
    with tab1:
        st.subheader("100 Film dengan Rating Tertinggi")
        col_rating = 'vote_average' if 'vote_average' in df.columns else df.columns[2]
        
        min_vote = st.slider("Minimal Jumlah Vote:", 0, 5000, 1000)
        # Filter data
        top_rated = df[df['vote_count'] >= min_vote].sort_values(by=col_rating, ascending=False).head(100)
        
        # Tentukan kolom apa saja yang mau ditampilkan (Cek dulu kolomnya ada gak)
        cols_to_show = ['title', 'vote_average', 'vote_count']
        if 'release_date' in df.columns: cols_to_show.append('release_date')
        
        st.dataframe(
            top_rated[cols_to_show],
            use_container_width=True,
            hide_index=True
        )

    # === TAB 2: POPULARITY (INI YANG TADI ERROR) ===
    with tab2:
        st.subheader("100 Film Paling Populer")
        col_pop = 'popularity' if 'popularity' in df.columns else df.columns[-1]
        
        top_pop = df.sort_values(by=col_pop, ascending=False).head(100)
        
        # FIX: Kita cek dulu kolom apa aja yang tersedia
        # Jangan paksa panggil 'original_language' kalau gak ada
        cols_pop_show = ['title', 'popularity']
        if 'release_date' in df.columns: cols_pop_show.append('release_date')
        if 'original_language' in df.columns: cols_pop_show.append('original_language') # Cek dulu!
        
        st.dataframe(
            top_pop[cols_pop_show],
            use_container_width=True,
            hide_index=True
        )

# ==========================================
# SECTION 3: TREN & STATISTIK
# ==========================================
elif menu == "📈 Tren & Statistik":
    st.title("📈 Analisis Tren Perfilman")
    
    st.subheader("Produktivitas Industri Film per Tahun")
    if 'year' in df.columns:
        film_per_tahun = df.groupby('year').size().reset_index(name='Jumlah Film')
        film_per_tahun = film_per_tahun[(film_per_tahun['year'] > 1960) & (film_per_tahun['year'] <= 2024)]
        
        fig_line = px.area(film_per_tahun, x='year', y='Jumlah Film', color_discrete_sequence=['#FF4B4B'])
        fig_line.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_line, use_container_width=True)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        # HANYA TAMPILKAN DONUT CHART KALAU ADA KOLOM BAHASA
        if 'original_language' in df.columns:
            st.subheader("Distribusi Bahasa")
            lang_counts = df['original_language'].value_counts().head(7)
            fig_pie = px.pie(values=lang_counts.values, names=lang_counts.index, hole=0.5)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("⚠️ Data bahasa tidak tersedia di dataset ini.")
            
    with col_b:
        st.subheader("Rating vs Popularitas")
        col_pop = 'popularity' if 'popularity' in df.columns else df.columns[-1]
        col_rating = 'vote_average' if 'vote_average' in df.columns else df.columns[2]
        
        fig_scat = px.scatter(df.head(500), x=col_pop, y=col_rating, color=col_rating, size='vote_count')
        st.plotly_chart(fig_scat, use_container_width=True)

# ==========================================
# SECTION 4: SEARCH ENGINE - SUDAH DIPERBAIKI
# ==========================================
elif menu == "🔍 Movie Search Engine":
    st.title("🔍 Cari Detail Film")
    st.write("Cari database untuk melihat kartu performa film tertentu.")
    
    col_pop = 'popularity' if 'popularity' in df.columns else df.columns[-1]
    search_list = df.sort_values(by=col_pop, ascending=False)['title'].unique()
    
    judul_pilihan = st.selectbox("Ketik Judul Film:", search_list)
    
    if judul_pilihan:
        st.markdown("---")
        data_film = df[df['title'] == judul_pilihan].iloc[0]
        
        col_img, col_stats = st.columns([1, 2])
        
        with col_img:
            st.markdown("""
            <div style="background-color: #333; height: 300px; display: flex; align-items: center; justify-content: center; border-radius: 15px;">
                <h1 style="font-size: 80px;">🎬</h1>
            </div>
            """, unsafe_allow_html=True)
            
        with col_stats:
            st.subheader(f"{data_film['title']}")
            
            # CEK KETERSEDIAAN TANGGAL
            if 'release_date' in df.columns:
                try:
                    tgl = data_film['release_date'].strftime('%d %B %Y')
                    st.caption(f"Rilis: {tgl}")
                except:
                    st.caption("Tanggal Rilis: -")
            
            # FIX: CEK DULU ADA KOLOM BAHASA GAK
            if 'original_language' in df.columns:
                st.write(f"**Bahasa Asli:** {data_film['original_language'].upper()}")
            
            # Progress bar Rating
            rating_val = data_film['vote_average'] if 'vote_average' in data_film else 0
            st.write(f"**Rating:** {rating_val}/10")
            st.progress(rating_val/10)
            
            c1, c2 = st.columns(2)
            c1.metric("Popularitas", f"{data_film['popularity']:.0f}")
            c2.metric("Jumlah Vote", f"{data_film['vote_count']:,}")


# ==========================================
# 5. EKSPOR DATA UNTUK JAVA
# ==========================================
if df is not None:
    # 1. Olah data (ambil top 100 rating dengan min vote 1000)
    col_rating = 'vote_average' if 'vote_average' in df.columns else df.columns[2]
    top_100_java = df[df['vote_count'] >= 1000].sort_values(by=col_rating, ascending=False).head(100)

    # 2. Pilih kolom yang dibutuhkan Java (judul, rating, popularitas)
    cols_to_export = ['title', 'vote_average', 'popularity']

    # 3. Tentukan path penyimpanan yang BENAR
    export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'processed')
    export_path = os.path.join(export_dir, 'top_100_movies_java.csv')

    # Pastikan folder 'processed' ada
    os.makedirs(export_dir, exist_ok=True)

    # 4. Simpan ke CSV
    top_100_java[cols_to_export].to_csv(export_path, index=False)
    # st.success(f"File CSV untuk Java berhasil dibuat di: {export_path}") # Baris ini bisa dihapus setelah yakin