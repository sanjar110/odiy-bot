from flask import request, render_template, jsonify
from app import app

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form.get("username")
    password = request.form.get("password")
    # TODO: DB tekshirish
    return jsonify({"status":"success","message":"Login muvaffaqiyatli!"})

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    username = request.form.get("username")
    password = request.form.get("password")
    # TODO: DB saqlash
    return jsonify({"status":"success","message":"Ro‘yxatdan o‘tish muvaffaqiyatli!"})
