from flask import Flask, render_template, redirect, url_for, session
from flask_cors import CORS
from routes.shared import shared_bp
from routes.personal import personal_bp
from routes.api import api_bp
import os

app = Flask(__name__)
app.secret_key = "evangelion_secure_key"
CORS(app)

# 블루프린트 등록
app.register_blueprint(shared_bp)
app.register_blueprint(personal_bp)
app.register_blueprint(api_bp)


# 루트 페이지 → 로그인 or shared로 이동
@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("shared.shared_home"))
    else:
        # 임시 로그인 (자동 로그인 테스트용)
        session["username"] = "kyhoon0828"
        return redirect(url_for("shared.shared_home"))

if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_RUN_PORT", 5000))
    print(f"🚀 EVANGELION NAS running on http://{host}:{port}/shared/")
    app.run(host=host, port=5000)



