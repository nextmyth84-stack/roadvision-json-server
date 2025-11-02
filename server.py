# server.py
from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)

# 저장 폴더 (Render 서버 안)
SAVE_DIR = "uploads"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route("/")
def home():
    return "✅ roadvision JSON server is running."

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

    with open(os.path.join(SAVE_DIR, filename), "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)

    return jsonify({"ok": True, "saved": filename})

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    """
    Streamlit에서 Render에 저장된 파일을 다시 불러올 때 사용.
    URL 예시: /download/전일근무.json
    """
    try:
        with open(os.path.join(SAVE_DIR, filename), "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify({"error": "file not found"}), 404

if __name__ == "__main__":
    # Render가 내부적으로 포트를 지정하므로, os.environ에서 가져오도록 설정
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
