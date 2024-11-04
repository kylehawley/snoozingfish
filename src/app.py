import os
import sqlite3

from flask import Flask, abort, jsonify, render_template

app = Flask(__name__)

DB_PATH = "../listings.db"

def get_db_connection():
    if not os.path.exists(DB_PATH):
        return None
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/nl-listings")
def listings_page():
    conn = get_db_connection()
    if not conn:
        abort(400)

    listings = conn.execute("SELECT * FROM listings WHERE is_new = 1").fetchall()
    conn.close()
    return render_template("listings.html", listings=listings)


@app.route("/apply/<int:id>", methods=["POST"])
def apply_to_listing(id):
    conn = get_db_connection()
    if not conn:
        abort(400)
    
    conn.execute("UPDATE listings SET is_new = 0 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
