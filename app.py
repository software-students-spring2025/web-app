from flask import Flask
import os

app = Flask(__name__, template_folder='templates', static_folder='public', static_url_path='/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000), debug=False)