@echo off
TITLE Movie Dashboard Auto-Setup
echo ======================================================
echo   AUTO SETUP & RUN (VERSI DALAM FOLDER)
echo ======================================================

:: 1. Pindah ke lokasi file ini berada
cd /d "%~dp0"

:: 2. CEK APAKAH KITA SUDAH DI DALAM FOLDER YANG BENAR?
if exist "app.py" (
    echo [INFO] Lokasi benar. File app.py ditemukan.
) else (
    echo [ERROR] FILE app.py TIDAK KETEMU!
    echo Pastikan file .bat ini ditaruh TEPAT di samping app.py!
    pause
    exit
)

:: 3. LOGIKA VENV
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Venv ditemukan. Mengaktifkan...
    call venv\Scripts\activate.bat
) else (
    echo [ALERT] Venv belum ada. Membuat baru...
    
    :: Bikin Venv
    python -m venv venv
    call venv\Scripts\activate.bat
    
    :: Install Library
    echo [INFO] Menginstall Library...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    echo [SUCCESS] Setup Selesai!
)

:: 4. JALANKAN
echo.
echo [START] Menjalankan Streamlit...
streamlit run app.py

:: Biar kalau error gak langsung close
pause