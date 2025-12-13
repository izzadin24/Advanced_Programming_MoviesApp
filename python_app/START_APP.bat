@echo off
TITLE Movie Dashboard Launcher
echo ======================================================
echo   SEDANG MENYALAKAN MESIN APLIKASI...
echo   (Jendela ini jangan ditutup ya, minimize aja)
echo ======================================================

:: 1. Masuk ke folder proyekmu
cd /d "D:\KULIAH\SEMESTER 3\PEMROGRAMAN LANJUT\TUBES_PL"

:: 2. Nyalakan Venv secara otomatis
call python_app\venv\Scripts\activate.bat

:: 3. Masuk ke folder python dan jalankan Streamlit
cd python_app
streamlit run app.py