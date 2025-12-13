import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="Movie Dashboard UI", layout="wide", page_icon="🍿")

# CSS Custom biar rapi
st.markdown("""
<style>
    .stMetric { background-color: #f0f2f6; padding: 15px; border-radius: 10px; }
    .stProgress > div > div > div > div { background-color: #ff4b4b; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. LOAD DATA (JURUS ANTI-NYASAR)
# ==========================================
@st.cache_data
def load_data():
    # Ini triknya: Kita suruh Python cari folder tempat app.py berada dulu
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Lalu mundur satu langkah, masuk folder data, masuk folder raw, cari file yang BENAR
    # Sesuai path yang kamu kirim: D:\...\data\raw\Top_Rated_Movies.csv
    file_path = os.path.join(current_dir, '..', 'data', 'raw', 'Top_Rated_Movies.csv')
    
    print(f"Sedang mencari file di: {file_path}") # Ini bakal muncul di terminal buat cek

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # Ambil semua kolom dulu biar aman, nanti baru difilter
        return df
    else:
        return None

df = load_data()

# Error Handling (Kalau masih gak ketemu juga)
if df is None:
    st.error("❌ FILE MASIH TIDAK KETEMU!")
    st.warning(f"Sistem mencari di: `../data/raw/Top_Rated_Movies.csv`")
    st.info("Coba cek: Apakah file CSV benar-benar ada di dalam folder 'raw'?")
    st.stop()

# ==========================================
# 2. DASHBOARD CONTENT
# ==========================================
st.title("🍿 TMDB Top Rated Movies")
st.markdown(f"**Status Data:** Berhasil memuat {len(df)} film.")
st.markdown("---")

# KPI Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Film", f"{len(df):,}")
with col2:
    # Cek dulu nama kolomnya (kadang beda dikit huruf besar/kecil)
    col_rating = 'vote_average' if 'vote_average' in df.columns else df.columns[2] # Tebak kolom ke-3
    avg_rating = df[col_rating].mean()
    st.metric("Rata-rata Rating", f"{avg_rating:.1f} / 10")
with col3:
    col_pop = 'popularity' if 'popularity' in df.columns else df.columns[-1] # Tebak kolom terakhir
    st.metric("Popularitas Tertinggi", f"{df[col_pop].max():.1f}")

st.markdown("---")

# Progress Bar Rating
st.subheader("⭐ Cek Kualitas Film")
# Ambil judul (asumsi kolom 'title' ada)
if 'title' in df.columns:
    # Ambil 50 film pertama aja buat contoh
    pilihan_film = st.selectbox("Pilih Film:", df['title'].head(50).unique())
    
    # Ambil rating film itu
    rating_val = df[df['title'] == pilihan_film][col_rating].iloc[0]
    st.progress(rating_val/10, text=f"Rating: {rating_val}/10")
else:
    st.write("Kolom 'title' tidak ditemukan di CSV.")

# ==========================================
# 3. EXPORT BUTTON (FINAL)
# ==========================================
st.markdown("---")
if st.button("DOWNLOAD DATA JAVA", type="primary"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(current_dir, '..', 'data', 'processed')
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    save_path = os.path.join(output_folder, 'top_100_movies_java.csv')
    df.head(100).to_csv(save_path, index=False)
    
    st.balloons()
    st.success(f"Mantap! File sudah jadi di: {save_path}")