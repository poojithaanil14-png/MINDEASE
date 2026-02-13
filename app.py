from flask import Flask, render_template, request, redirect,session 
import json
import os

app = Flask(__name__)
app.secret key = "hackathon_secret"
DATA_FILE = "entries.json"

# Load entries
def load_entries():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save entries
def save_entries(entries):
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f)

# Home page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        session["user"] = username
        return redirect("/home")
    return render_template("login.html")
@app.route("/")
def home():
    return render_template("index.html")

# Add entry
@app.route("/add", methods=["POST"])
def add_entry():
    text = request.form["entry"]

    entries = load_entries()
    entries.append(text)
    save_entries(entries)

    return redirect("/entries")

# Show entries
@app.route("/entries")
def show_entries():
    entries = load_entries()
    return render_template("entries.html", entries=entries)

if __name__ == "__main__":
    app.run(debug=True)