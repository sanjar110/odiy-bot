from flask import request, render_template
from app import app

@app.route("/search")
def search():
    query = request.args.get("q")
    results = [{"title":"Qo‘shiq A"},{"title":"Video B"}]  # Mock
    return render_template("search.html", results=results)
