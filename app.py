import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
DB_PATH = os.path.join(BASE_DIR, "orders.db")
ALLOWED_EXTENSIONS = {"mp4", "mov", "mkv", "avi", "jpg", "jpeg", "png"}

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500 MB

INSTAGRAM_URL = "https://www.instagram.com/_vj_505?dlrf=ZG1mMTN3MDJvZ2xz"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                category TEXT NOT NULL,
                package TEXT,
                event_date TEXT,
                details TEXT,
                file_name TEXT,
                created_at TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'New'
            )
        """)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html", instagram_url=INSTAGRAM_URL)

@app.route("/order", methods=["GET", "POST"])
def order():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        category = request.form.get("category", "").strip()
        package = request.form.get("package", "").strip()
        event_date = request.form.get("event_date", "").strip()
        details = request.form.get("details", "").strip()

        if not name or not phone or not category:
            flash("Please fill in your name, mobile number and video category.", "error")
            return redirect(url_for("order"))

        uploaded = request.files.get("reference_file")
        saved_name = None
        if uploaded and uploaded.filename:
            if not allowed_file(uploaded.filename):
                flash("File type not supported. Upload MP4, MOV, MKV, AVI, JPG or PNG.", "error")
                return redirect(url_for("order"))
            safe_name = secure_filename(uploaded.filename)
            saved_name = datetime.now().strftime("%Y%m%d_%H%M%S_") + safe_name
            uploaded.save(os.path.join(app.config["UPLOAD_FOLDER"], saved_name))

        with get_db() as conn:
            conn.execute("""
                INSERT INTO orders (name, phone, category, package, event_date, details, file_name, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, phone, category, package, event_date, details, saved_name,
                  datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        flash("Your request has been submitted! Please DM VJ EDIT on Instagram to confirm your order.", "success")
        return redirect(url_for("order"))
    return render_template("order.html", instagram_url=INSTAGRAM_URL)

@app.route("/admin")
def admin():
    # Demo dashboard. Add login protection before deploying publicly.
    with get_db() as conn:
        orders = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    return render_template("admin.html", orders=orders, instagram_url=INSTAGRAM_URL)

@app.route("/admin/status/<int:order_id>", methods=["POST"])
def update_status(order_id):
    status = request.form.get("status", "New")
    if status not in {"New", "Processing", "Completed", "Cancelled"}:
        status = "New"
    with get_db() as conn:
        conn.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
    flash("Order status updated.", "success")
    return redirect(url_for("admin"))

@app.errorhandler(413)
def too_large(_error):
    flash("File is too large. Maximum upload size is 500 MB.", "error")
    return redirect(url_for("order"))

init_db()

if __name__ == "__main__":
    app.run(debug=True)
