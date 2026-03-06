from flask import render_template
from app import app

@app.route("/library")
def library():
    items = ["Qo‘shiq A","Video B"]
    return render_template("library.html", items=items)
