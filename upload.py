from flask import request, render_template, jsonify
from app import app

@app.route("/upload", methods=["GET","POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    file = request.files.get("file")
    # TODO: Faylni saqlash
    return jsonify({"status":"success","message":"Yuklash muvaffaqiyatli!"})
