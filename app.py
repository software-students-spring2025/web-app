from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulating a database (replace with MongoDB later)
users = {}

# Login Page
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Check if user eaxists and password matches
        if email in users and users[email] == password:
            return "Login Successful! Welcome to Course Content Helper."
        else:
            return "Invalid Credentials. Try again."

    return render_template("login.html")

# Registration Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Store the user (replace this with a database in the future)
        if email in users:
            return "Email already registered. Try logging in."
        users[email] = password

        return redirect(url_for("login"))  # Redirect to login after successful registration
    return render_template("register.html")

# TODO-Search Page
@app.route("/search", methods=["GET"])
def search():
    

    return render_template("search.html")

# TODO-Upload Page
@app.route("/upload", methods=["GET", "POST"])
def upload():

    
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
