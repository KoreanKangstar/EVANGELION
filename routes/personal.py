from flask import Blueprint, request, redirect, url_for, send_from_directory, abort, render_template
from routes.auth import auth_required
import os
import shutil
import zipfile
from io import BytesIO
from flask import send_file

personal_bp = Blueprint("personal", __name__)
BASE_DIR = "/mnt/ssd"

@personal_bp.route("/")
@auth_required
def view_personal():
    user = request.authorization.username
    user_dir = os.path.join(BASE_DIR, user)
    os.makedirs(user_dir, exist_ok=True)
    files = sorted(os.listdir(user_dir))
    return render_template("home.html", personal_files=files, user=user)

@personal_bp.route("/upload", methods=["POST"])
@auth_required
def upload_personal():
    user = request.authorization.username
    user_dir = os.path.join(BASE_DIR, user)
    os.makedirs(user_dir, exist_ok=True)
    f = request.files.get("file")
    if not f or f.filename == "":
        return "No file", 400
    f.save(os.path.join(user_dir, f.filename))
    print(f"[UPLOAD PERSONAL] {f.filename} by {user}")
    return redirect("/")

@personal_bp.route("/download/<path:filename>")
@auth_required
def download_personal(filename):
    user = request.authorization.username
    user_dir = os.path.join(BASE_DIR, user)
    if not os.path.exists(os.path.join(user_dir, filename)):
        abort(404)
    return send_from_directory(user_dir, filename, as_attachment=True)

@personal_bp.route("/delete/<path:filename>")
@auth_required
def delete_personal(filename):
    user = request.authorization.username
    user_dir = os.path.join(BASE_DIR, user)
    path = os.path.join(user_dir, filename)
    if os.path.exists(path):
        os.remove(path)
        print(f"[DELETE PERSONAL] {filename} by {user}")
    return redirect("/")

@personal_bp.route("/download_all")
@auth_required
def download_all_personal():
    user = request.authorization.username
    user_dir = os.path.join(BASE_DIR, user)
    mem = BytesIO()
    with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in os.listdir(user_dir):
            file_path = os.path.join(user_dir, file)
            zf.write(file_path, os.path.basename(file))
    mem.seek(0)
    return send_file(mem, as_attachment=True, download_name=f"{user}_personal.zip")
