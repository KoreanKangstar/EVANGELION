import os
import mimetypes
import zipfile
from io import BytesIO
from flask import send_from_directory, send_file

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def list_files(path: str) -> list:
    """Return sorted, non-hidden file list."""
    if not os.path.isdir(path):
        return []
    return sorted([f for f in os.listdir(path) if not f.startswith(".")])

def download_response(directory: str, filename: str):
    """Send a file with UTF-8 friendly headers and sensible mimetype."""
    file_path = os.path.join(directory, filename)
    if not os.path.exists(file_path):
        return None  # caller should handle 404
    resp = send_from_directory(directory, filename, as_attachment=True)
    mime, _ = mimetypes.guess_type(filename)
    if mime and "text" in mime:
        resp.headers["Content-Type"] = f"{mime}; charset=utf-8"
    else:
        resp.headers["Content-Type"] = "application/octet-stream; charset=utf-8"
    resp.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{filename}"
    return resp

def zip_dir_to_response(dir_path: str, zip_name: str):
    """Zip a directory to memory and return as Flask send_file response."""
    mem = BytesIO()
    with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(dir_path):
            for file in files:
                fp = os.path.join(root, file)
                arcname = os.path.relpath(fp, dir_path)
                zf.write(fp, arcname)
    mem.seek(0)
    return send_file(mem, as_attachment=True, download_name=zip_name, mimetype="application/zip")
