from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello, World!"
if name == "__main__":
    app.run(debug=True)
