from flask import render_template
from app import app

@app.route("/gamification")
def gamification():
    badges = ["Top Listener","Premium User","Uploader"]
    return render_template("gamification.html", badges=badges)
