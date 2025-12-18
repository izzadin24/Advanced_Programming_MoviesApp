@echo off
TITLE Movie Dashboard Launcher
echo ======================================================
echo   SEDANG MENYALAKAN MESIN APLIKASI...
echo   (Jendela ini jangan ditutup ya, minimize aja)
echo ======================================================

:: 1. Pindah ke lokasi di mana file .bat ini berada (Universal)
cd /d "%~dp0"

:: 2. Masuk ke folder python_app (Relatif terhadap file .bat)
cd python_app

:: --- PERINGATAN PENTING SOAL VENV (BACA DI BAWAH) ---
:: Cek apakah folder venv ada.
if exist "venv\Scripts\activate.bat" (
    echo Mengaktifkan Virtual Environment...
    call venv\Scripts\activate.bat
) else (
    echo [WARNING] Folder venv tidak ditemukan atau rusak!
    echo Mencoba menjalankan dengan Python Global...
)

:: 3. Jalankan Streamlit
echo Menjalankan Streamlit...
streamlit run app.py

pause