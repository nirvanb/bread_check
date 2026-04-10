from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import csv, os, random

app = Flask(__name__)

# Database setup
devskip = True
if not devskip:
    uri = os.environ.get("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = uri
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///responses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Database model
class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    selections = db.Column(db.Text)

IMAGE_FOLDER = os.path.join("static", "images")

def get_all_images():
    files = os.listdir(IMAGE_FOLDER)
    images = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]
    return images

IMAGES = get_all_images()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        place = request.form.get("place")
        selected = request.form.getlist("bread")

        # Save to database
        response = Response(
            name=place,
            selections=",".join(selected)
        )
        db.session.add(response)
        db.session.commit()

        return redirect("/thanks")

    return render_template("index.html", images=IMAGES)

@app.route("/thanks")
def thanks():
    return "Thanks for your response!"

# Create DB if it doesn't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
