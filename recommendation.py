from flask import request, jsonify
from app import app

@app.route("/recommendations")
def recommendations():
    user_id = request.args.get("user_id")
    data = [
        {"title":"Sevimli qo‘shiq","artist":"Artist A"},
        {"title":"Yangi klip","artist":"Artist B"}
    ]
    return jsonify(data)
