from flask import render_template
from app import app

@app.route("/streaming")
def streaming():
    return render_template("streaming.html")
