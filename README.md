# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

Our simple and user-friendly app allows students to schedule and organize events taking place in their daily lives, aiming to support their time management and productivity. 

## User stories

[Link to User Stories in Issues](https://github.com/software-students-spring2025/2-web-app-web-avengers/issues)

## Steps necessary to run the software

The following instructions present how to set up and run the event calendar app on your own local computer in development mode. 

### Step 1: Install Python 

To get started, install Python through [here](https://www.python.org/downloads/) and ensure Python 3.x.x. is downloaded (preferably Python 3.4 or later) for this project. If Python version 3.4 or later is used, `pip` will be installed by default. 

### Step 2: Clone the Repository on your Local Machine

Create a local repository through cloning with the following command:
```
git clone https://github.com/software-students-spring2025/2-web-app-web-avengers.git
```

### Step 3: Set up a Python Virtual Environment 

There are two ways you can set up a Python virtual environment, using `pip` or `pipenv`. Either method works for this project. Intially, ensure you are within the project directory `2-web-app-avengers`.

#### Pip
Create a new virtual environment named `venv` with:
```
python3 -m venv venv
```

Activate the `venv` virtual environment with: 

On Mac/Linux:
```
source venv/bin/activate
```
On Windows:
```
venv\Scripts\activate.bat
```

#### Pipenv
If you prefer to make a new virtual environment with `pipenv`, follow the instructions below. 

Install `pipenv`, which is not installed by default with Python. Try the command with `pip3` instead of `pip` if the following does not work: 
```
pip install pipenv
```

Activate the virtual environment with:
```
pipenv shell
```

### Step 4: Install Dependencies 

If the `venv` virtual environment was created with `pip`, install the dependencies in the environment with:
```
pip install -r requirements.txt
```

If the virtual environment was created with `pipenv`, dependencies in `Pipfile` will be automatically installed when activating it. 

### Step 5: Create .env file

Create an .env file, like the `env.example` file [here](https://github.com/software-students-spring2025/2-web-app-web-avengers/blob/main/env.example). Leave most of it the same, but replace the right side of the `=` sign with real values to configure `monogdb` (credentials can be found under team discord channel):
```
MONGO_DBNAME=your_db_name
MONGO_URI=mongodb+srv://your_db_username:your_db_password@your_db_host_server_name:27017
```

### Step 6: Run the App

Set environment variables in the command line for the  `flask-app` with:

On Mac/Linux:
```
export FLASK_APP=app.py
export FLASK_ENV=development
```

On Windows:
```
set FLASK_APP=app.py
set FLASK_ENV=development
```

Run the app with:
```
flask run
```
As a result, it will let you know that the app is running on http://127.0.0.1:5000, which you can check out in a web browser.  

## Task boards

[Sprint 1 Task Board](https://github.com/orgs/software-students-spring2025/projects/35)

[Sprint 2 Task Board](https://github.com/orgs/software-students-spring2025/projects/32)
