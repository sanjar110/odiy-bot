from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# Import qilinadigan modullar
import auth, search, player, upload, library, social, premium, admin
import recommendation, streaming, events, gamification

if __name__ == "__main__":
    app.run(debug=True)
