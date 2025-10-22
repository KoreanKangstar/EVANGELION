from flask import Blueprint, request, redirect, url_for, send_from_directory, abort, send_file
from routes.auth import auth_required
import os
import zipfile
from io import BytesIO

shared_bp = Blueprint("shared", __name__)
SHARED_DIR = "/mnt/ssd/shared"
os.makedirs(SHARED_DIR, exist_ok=True)

@shared_bp.route("/upload", methods=["POST"])
@auth_required
def upload_shared():
    f = request.files.get("file")
    if not f or f.filename == "":
        return "No file", 400
    f.save(os.path.join(SHARED_DIR, f.filename))
    user = request.authorization.username
    print(f"[UPLOAD SHARED] {f.filename} by {user}")
    return redirect("/")

@shared_bp.route("/download/<path:filename>")
@auth_required
def download_shared(filename):
    if not os.path.exists(os.path.join(SHARED_DIR, filename)):
        abort(404)
    return send_from_directory(SHARED_DIR, filename, as_attachment=True)

@shared_bp.route("/delete/<path:filename>")
@auth_required
def delete_shared(filename):
    path = os.path.join(SHARED_DIR, filename)
    if os.path.exists(path):
        os.remove(path)
        print(f"[DELETE SHARED] {filename}")
    return redirect("/")

@shared_bp.route("/download_all")
@auth_required
def download_all_shared():
    mem = BytesIO()
    with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in os.listdir(SHARED_DIR):
            file_path = os.path.join(SHARED_DIR, file)
            zf.write(file_path, os.path.basename(file))
    mem.seek(0)
    return send_file(mem, as_attachment=True, download_name="shared.zip")
