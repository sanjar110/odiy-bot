from flask import render_template
from app import app

@app.route("/social")
def social():
    return render_template("social.html")
