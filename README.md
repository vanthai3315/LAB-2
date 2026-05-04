# LAB 2 - APPLICATION PROGRAMMING INTERFACE AND FIREBASE STUDIO

Dự án này là một ứng dụng ghi chú (Note App) đơn giản, được xây dựng để hoàn thành Bài thực hành số 2 môn **Tư duy tính toán**. Ứng dụng tách biệt rõ ràng giữa Frontend và Backend, tích hợp xác thực người dùng và cơ sở dữ liệu đám mây Firebase.

*   **Trường**: Đại học Khoa học Tự nhiên - ĐHQG TP.HCM
*   **Khoa**: Công nghệ Thông tin
*   **Môn học**: Tư duy tính toán
*   **Giảng viên**: Lê Đức Khoan
*   **Sinh viên thực hiện**: Chu Văn Thái

---

## 🚀 Tính năng chính (Feature)
*   **Đăng ký/Đăng nhập**: Sử dụng Firebase Authentication (Email/Password).
*   **Quản lý ghi chú**: Người dùng có thể thêm ghi chú mới và xem danh sách ghi chú cá nhân.
*   **Xóa ghi chú**: Cho phép người dùng xóa các thẻ ghi chú đã lưu.
*   **Thời gian thực**: Dữ liệu được đồng bộ hóa với Google Firestore theo múi giờ Việt Nam (GMT+7).

---

## 🛠 Cấu trúc dự án (Project Structure)
Dự án được tổ chức theo cấu trúc chuẩn để tách biệt logic xử lý và giao diện:
```text
project/
├── backend/
│   ├── main.py              # API xử lý logic (FastAPI)
│   └── serviceAccountKey.json # Chìa khóa Firebase (Không đẩy lên GitHub)
├── frontend/
│   └── app.py               # Giao diện người dùng (Streamlit)
├── .gitignore               # Chặn các file rác và mã bảo mật
├── requirements.txt         # Danh sách thư viện cần cài đặt
└── README.md                # Hướng dẫn dự án