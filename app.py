from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

IMAGES = [
    "baguette.jpg",
    "sourdough.jpg",
    "croissant.jpg"
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected = request.form.getlist("bread")

        with open("responses.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(selected)

        return redirect("/thanks")

    return render_template("index.html", images=IMAGES)

@app.route("/thanks")
def thanks():
    return "Thanks for your response!"

if __name__ == "__main__":
    app.run(debug=True)
