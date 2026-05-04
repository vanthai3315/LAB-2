from fastapi import FastAPI
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta, timezone

# 1. Kết nối Firebase
cred = credentials.Certificate("backend/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

def get_vn_time():
    return datetime.now(timezone.utc) + timedelta(hours=7)

@app.get("/")
def read_root():
    return {"message": "Welcome to Note App API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": get_vn_time().strftime("%Y-%m-%d %H:%M:%S")}

class Note(BaseModel):
    email: str
    content: str

@app.post("/notes")
def create_note(note: Note):
    doc_ref = db.collection("notes").document()
    vn_now = get_vn_time()
    doc_ref.set({
        "email": note.email,
        "content": note.content,
        "timestamp": vn_now.strftime("%Y-%m-%d %H:%M:%S")
    })
    return {"message": "Success!"}

# --- CẬP NHẬT HÀM LẤY GHI CHÚ (CÓ LẤY ID) ---
@app.get("/notes")
def get_notes(email: str):
    notes_ref = db.collection("notes").where("email", "==", email).stream()
    notes = []
    for doc in notes_ref:
        item = doc.to_dict()
        item["id"] = doc.id  # Lấy ID của document để làm khóa xóa
        notes.append(item)
    # Sắp xếp mới nhất lên đầu
    return {"notes": sorted(notes, key=lambda x: x['timestamp'], reverse=True)}

# --- THÊM ENDPOINT XÓA ---
@app.delete("/notes/{note_id}")
def delete_note(note_id: str):
    try:
        db.collection("notes").document(note_id).delete()
        return {"message": "Deleted successfully"}
    except Exception as e:
        return {"error": str(e)}