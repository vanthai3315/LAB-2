@echo off
chcp 65001 > nul
echo ==========================================
echo      KHỞI ĐỘNG NOTE APP - LAB 2
echo ==========================================

echo [1/2] Đang khởi động Backend (FastAPI)...
:: Lệnh start /B giúp chạy ngầm backend mà không mở thêm cửa sổ mới
start /B uvicorn backend.main:app --port 8000 --reload

echo.
echo Đang đợi Backend khởi động (3 giây)...
timeout /t 3 /nobreak > nul

echo [2/2] Đang khởi động Frontend (Streamlit) và mở trình duyệt...
:: Streamlit sẽ tự động mở tab mới trên trình duyệt của bạn
streamlit run frontend/app.py

pause
