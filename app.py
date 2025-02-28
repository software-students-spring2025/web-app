from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Route for the login page
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        # Temporary check, need to replace with database chec!!!!!!!!!!!!!!!!!!!!!!!!!!
        if email == "test@nyu.edu" and password == "password123":
            return "Login Successful!"
        else:
            return "Invalid Credentials. Try again."
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
