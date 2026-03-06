from flask import render_template
from app import app

@app.route("/player/<content_id>")
def player(content_id):
    return render_template("player.html", content_id=content_id)
