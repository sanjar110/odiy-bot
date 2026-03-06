from flask import render_template, request, jsonify
from app import app

# Mock tariflar
tariffs = [
    {"name":"Basic","price":"10$"},
    {"name":"Standard","price":"15$"},
    {"name":"Premium","price":"20$"}
]

@app.route("/premium")
def premium():
    return render_template("premium.html", tariffs=tariffs)

@app.route("/subscribe", methods=["POST"])
def subscribe():
    plan = request.form.get("plan")
    # TODO: DB ga yozish (foydalanuvchi obunasi)
    return jsonify({"status":"success","message":f"{plan} tarifiga obuna bo‘ldingiz!"})

@app.route("/admin/tariffs", methods=["POST"])
def admin_tariffs():
    action = request.form.get("action")
    name = request.form.get("name")
    price = request.form.get("price")

    if action == "add":
        tariffs.append({"name":name,"price":price})
    elif action == "update":
        for t in tariffs:
            if t["name"] == name:
                t["price"] = price
    elif action == "delete":
        tariffs[:] = [t for t in tariffs if t["name"] != name]

    return jsonify({"status":"success","message":"Tariflar yangilandi!"})
