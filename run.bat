@echo off
chcp 65001 > nul
echo ======================================================
echo       HỆ THỐNG TỰ ĐỘNG KHỞI ĐỘNG NOTE APP - LAB 2
echo ======================================================

echo [1/3] Đang kiểm tra và cài đặt thư viện (nếu thiếu)...
echo Vui lòng đợi trong giây lát...
:: Lệnh này sẽ quét file requirements.txt và cài những gì còn thiếu
python -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [!] Có lỗi xảy ra khi cài đặt thư viện. Vui lòng kiểm tra lại Python/Pip.
    pause
    exit /b
)
echo [OK] Thư viện đã sẵn sàng!

echo.
echo [2/3] Đang khởi động Backend (FastAPI)...
:: Chạy ngầm backend để không chiếm dụng cửa sổ hiện tại
start /B uvicorn backend.main:app --port 8000 --reload

echo.
echo Đang đợi Backend ổn định (3 giây)...
timeout /t 3 /nobreak > nul

echo [3/3] Đang khởi động Frontend (Streamlit) và mở trình duyệt...
echo Chúc bạn có buổi demo thành công!
streamlit run frontend/app.py

pause
