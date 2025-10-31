from flask import Blueprint, render_template, request, send_from_directory, jsonify, session, redirect, url_for
import os, shutil

personal_bp = Blueprint("personal", __name__, url_prefix="/personal")

BASE_DIR = "/mnt/ssd"
PERSONAL_DIR = os.path.join(BASE_DIR, "personal")
TRASH_DIR = os.path.join(BASE_DIR, "trash_personal")

os.makedirs(PERSONAL_DIR, exist_ok=True)
os.makedirs(TRASH_DIR, exist_ok=True)

def user_dir():
    username = session.get("username", "guest")
    path = os.path.join(PERSONAL_DIR, username)
    os.makedirs(path, exist_ok=True)
    return path

@personal_bp.route("/")
def index():
    if "username" not in session:
        session["username"] = "ID"
    return redirect(url_for("personal.user_home", username=session["username"]))

@personal_bp.route("/<username>")
def user_home(username):
    files = os.listdir(user_dir())
    return render_template("personal.html", username=username, files=files)

@personal_bp.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not f: return "no file", 400
    f.save(os.path.join(user_dir(), f.filename))
    return "OK", 200

@personal_bp.route("/delete/<path:filename>", methods=["DELETE"])
def delete(filename):
    src = os.path.join(user_dir(), filename)
    dst = os.path.join(TRASH_DIR, filename)
    shutil.move(src, dst)
    return jsonify({"status": "moved_to_trash"}), 200



