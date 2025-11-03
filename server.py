# server.py
from flask import Flask, request, jsonify, send_file
import json, os

app = Flask(__name__)

# 저장 폴더 (Render 서버 안)
SAVE_DIR = "uploads"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route("/")
def home():
    return "✅ roadvision JSON server is running."

# ==============================
# 📤 업로드
# ==============================
@app.route("/upload", methods=["POST"])
def upload_file():
    """
    Streamlit Cloud에서 전일근무.json 업로드 시 호출.
    body 예시:
    {
        "filename": "전일근무.json",
        "content": {...}
    }
    """
    data = request.json
    filename = data.get("filename", "data.json")
    content = data.get("content", {})

    filepath = os.path.join(SAVE_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)

    return jsonify({"ok": True, "saved": filename})

# ==============================
# 📥 다운로드
# ==============================
@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    """
    Streamlit에서 Render에 저장된 파일을 다시 불러올 때 사용.
    URL 예시: /download/전일근무.json
    """
    filepath = os.path.join(SAVE_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "file not found"}), 404

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==============================
# 📂 파일 목록 확인용 (브라우저 접근용)
# ==============================
@app.route("/list", methods=["GET"])
def list_files():
    """
    저장된 JSON 파일 목록을 반환.
    예시: /list → { "files": ["전일근무.json", "아침열쇠.json", ...] }
    """
    try:
        files = sorted(os.listdir(SAVE_DIR))
        return jsonify({"files": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==============================
# 🚀 실행
# ==============================
if __name__ == "__main__":
    # Render가 내부적으로 포트를 지정하므로, os.environ에서 가져오도록 설정
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
