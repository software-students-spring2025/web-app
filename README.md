# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

See instructions. Delete this line and place the Product Vision Statement here.

## User stories


## Initial setup

See instructions. Delete this line and place instructions to download, configure, and run the software here.

1. Virtual environment setup
```
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies
```
pip install flask pymongo flask-login python-dotenv bcrypt
```

3. Freeze requirements
```
pip freeze > requirements.txt
```

4. MongoDB setup
```
brew tap mongodb/brew
brew install mongodb-community@6.0
brew services start mongodb-community@6.0
```

5. Launch MongoDB
```
mongosh
use url_shortener
db.createCollection("users")
db.createCollection("urls")
```

6. Update your .env
```
MONGO_URI=mongodb://localhost:27017/url_shortener
```


## How to run
```
cd url_shortener_app
python3 app.py
```

### Page is located at http://127.0.0.1:8000


## Task boards

>[Task Board Link](https://github.com/orgs/software-students-spring2025/projects/7)
