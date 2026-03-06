from flask import render_template
from app import app

@app.route("/events")
def events():
    return render_template("events.html")
