import streamlit as st
import pyrebase
import requests
import json

# 1. Cấu hình Firebase
firebaseConfig = {
    "apiKey": "AIzaSyCHjAaGkwcoM8OaIjIvIRGiOlb2eZTUtdQ",
    "authDomain": "note-app-da7cf.firebaseapp.com",
    "projectId": "note-app-da7cf",
    "storageBucket": "note-app-da7cf.firebasestorage.app",
    "messagingSenderId": "943212736093",
    "appId": "1:943212736093:web:72eebf6c57a2399f06e7b4",
    "databaseURL": "https://note-app-da7cf-default-rtdb.firebaseio.com"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# 2. Cấu hình trang
st.set_page_config(page_title="Ghi chú cá nhân", page_icon="📝")
st.title("📝 Note App")

if "user" not in st.session_state:
    st.session_state.user = None

# 3. Giao diện Đăng nhập / Đăng ký
if st.session_state.user is None:
    email = st.text_input("Email")
    password = st.text_input("Mật khẩu", type="password", key="user_pass_input")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Đăng nhập", use_container_width=True):
            try:
                st.session_state.user = auth.sign_in_with_email_and_password(email, password)
                st.rerun()
            except Exception:
                st.error("Email hoặc mật khẩu không chính xác.")
                
    with col2:
        if st.button("Đăng ký", use_container_width=True):
            try:
                auth.create_user_with_email_and_password(email, password)
                st.success("Tạo tài khoản thành công! Hãy đăng nhập.")
            except Exception:
                st.error("Đăng ký thất bại hoặc Email đã tồn tại.")

# 4. Giao diện chính sau khi đăng nhập
else:
    st.write(f"Đang đăng nhập: **{st.session_state.user['email']}**")
    
    if st.button("Đăng xuất"):
        st.session_state.user = None
        st.rerun()

    st.divider()

    # --- KHU VỰC THÊM GHI CHÚ ---
    content = st.text_area("Nội dung ghi chú mới:", placeholder="Nhập nội dung tại đây...")
    
    if st.button("Lưu ghi chú"):
        if content.strip():
            try:
                res = requests.post("http://127.0.0.1:8000/notes", json={
                    "email": st.session_state.user['email'], 
                    "content": content
                })
                if res.status_code == 200:
                    st.session_state.show_success = True
                    st.rerun()
                else:
                    st.error("Lỗi: Server phản hồi không mong muốn.")
            except Exception:
                st.error("Lỗi: Không thể kết nối tới Backend.")
        else:
            st.warning("Vui lòng không để trống nội dung.")

    # --- PHẦN HIỂN THỊ THÔNG BÁO (DỜI XUỐNG DƯỚI NÚT LƯU) ---
    if st.session_state.get("show_success"):
        st.success("Đã lưu ghi chú thành công!")
        del st.session_state["show_success"]
    
    if st.session_state.get("show_delete"):
        st.info("Đã xóa ghi chú thành công.")
        del st.session_state["show_delete"]

    st.divider()

    # --- KHU VỰC LỊCH SỬ ---
    st.subheader("Ghi chú của bạn")
    try:
        res = requests.get("http://127.0.0.1:8000/notes", params={"email": st.session_state.user['email']})
        notes = res.json().get("notes", [])
        
        if not notes:
            st.info("Chưa có ghi chú nào.")
        else:
            for n in notes:
                with st.expander(f"📅 {n['timestamp']}"):
                    st.write(n['content'])
                    if st.button("Xóa ghi chú này", key=f"del_{n['id']}", type="secondary"):
                        try:
                            del_res = requests.delete(f"http://127.0.0.1:8000/notes/{n['id']}")
                            if del_res.status_code == 200:
                                st.session_state.show_delete = True
                                st.rerun()
                            else:
                                st.error("Lỗi: Không thể xóa ghi chú.")
                        except Exception:
                            st.error("Lỗi kết nối khi xóa.")
    except Exception:
        st.warning("Đang đồng bộ dữ liệu với hệ thống...")