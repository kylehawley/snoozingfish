import sqlite3

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("listings.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/nl-listings")
def listings_page():
    conn = get_db_connection()
    listings = conn.execute("SELECT * FROM listings").fetchall()
    conn.close()
    return render_template("listings.html", listings=listings)


@app.route("/apply/<int:id>", methods=["POST"])
def apply_to_listing(id):
    print("trying to apply to listing")
    conn = get_db_connection()
    conn.execute("UPDATE listings SET is_new = 0 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
