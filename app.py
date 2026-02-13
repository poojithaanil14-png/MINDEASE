from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = "hackathon_secret"  # Required for session tracking

DATA_FILE = "entries.json"

# Load and save entries
def load_entries():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_entries(entries):
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f)

# Login route
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        session["user"] = username
        return redirect("/home")
    return render_template("login.html")

# Journal home page (requires login)
@app.route("/home")
def index():
    if "user" not in session:
        return redirect("/")
    return render_template("index.html")

# Add new entry
@app.route("/add", methods=["POST"])
def add_entry():
    if "user" not in session:
        return redirect("/")
    text = request.form["entry"]
    entries = load_entries()
    entries.append({"user": session["user"], "text": text})
    save_entries(entries)
    return redirect("/entries")

# Show all entries
@app.route("/entries")
def show_entries():
    if "user" not in session:
        return redirect("/")
    entries = load_entries()
    # Show only entries of the logged-in user
    user_entries = [e for e in entries if e["user"] == session["user"]]
    return render_template("entries.html", entries=user_entries)

if __name__ == "__main__":
    app.run(debug=True)