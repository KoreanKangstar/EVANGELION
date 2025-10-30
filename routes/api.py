from flask import Blueprint, jsonify, request, send_from_directory
from datetime import datetime
import os, json, shutil

api_bp = Blueprint("api", __name__, url_prefix="/api")

BASE_DIR = "/mnt/ssd"
SHARED_DIR = os.path.join(BASE_DIR, "shared")
META_FILE = os.path.join(SHARED_DIR, "shared_meta.json")

def load_meta():
    if not os.path.exists(META_FILE):
        return {}
    with open(META_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@api_bp.route("/files", methods=["GET"])
def list_files():
    meta = load_meta()
    files = []
    for f in os.listdir(SHARED_DIR):
        path = os.path.join(SHARED_DIR, f)
        if not os.path.isfile(path): continue
        files.append({
            "name": f,
            "size": os.path.getsize(path),
            "timestamp": meta.get(f, {}).get("timestamp", os.path.getmtime(path))
        })
    return jsonify(files)

@api_bp.route("/download/<name>", methods=["GET"])
def download_file(name):
    return send_from_directory(SHARED_DIR, name)

@api_bp.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if not file: return "No file", 400
    file.save(os.path.join(SHARED_DIR, file.filename))
    return jsonify({"status": "uploaded"}), 200



