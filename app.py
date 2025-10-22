from flask import Flask, render_template
from routes.auth import auth_required
from routes.personal import personal_bp
from routes.shared import shared_bp
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1GB limit

# Register blueprints
app.register_blueprint(personal_bp, url_prefix="/personal")
app.register_blueprint(shared_bp, url_prefix="/shared")

@app.route("/")
@auth_required
def home():
    return render_template("home.html")

if __name__ == "__main__":
    print("EVANGELION - EdgeNAS running on port 5000...")
    app.run(host="0.0.0.0", port=5000)
