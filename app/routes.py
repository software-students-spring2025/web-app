from app import app

@app.route('/')
@app.route('/index')

def index():
    return "Hello, World!"

@app.route('/new')
def new():
    return "New page!"