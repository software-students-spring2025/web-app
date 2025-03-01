# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

Our web application is a dedicated Lost and Found platform for NYU, enabling users to search for lost items by name while allowing admins to manage the product list by adding or removing items as needed.


## User stories
- As an NYU student who lost my laptop in the library, I want to search for my lost item by name so that I can see if someone has reported it.
- As an NYU student who misplaced my student ID on campus, I want to filter search results by category so that I can quickly find relevant lost items
- As an NYU student who found an item but isn’t sure if it has already been reported, I want to search the lost and found database so that I don’t create duplicate entries.
- As an NYU student who found a lost water bottle in the gym, I want to add the item to the lost and found list so that the owner can locate it.
- As an NYU admin managing lost items, I want to add detailed descriptions and images when registering a lost item so that users can better identify their belongings.
- As an NYU student who reported my lost backpack but provided incorrect details, I want to edit my lost item entry so that I can update it with the correct description.
- As an NYU admin handling lost items, I want to modify item descriptions to correct errors or add more details so that users have accurate information when searching.
Delete Functionality
- As an NYU student who has found my lost AirPods, I want to delete my lost item entry so that others don’t waste time looking for it.
- As an NYU admin managing the lost and found database, I want to remove duplicate or irrelevant listings so that the platform remains clean and useful.
- As an NYU admin handling outdated records, I want to automatically delete lost item reports after a set period so that only recent and relevant entries are displayed.

## Steps necessary to run the software

### Option 1

Use Docker Compose to boot up both the mongodb database and the flask-app web app with one command:

**docker-compose up --build**

View the app in your browser:

open a web browser and go to http://localhost:5001 (or change 5001 to whatever port number you used for the flask-app.)

Note that you edit any of the files in the project, you will have to stop and then restart the containers, as indicated above.

### Option 2

#### Prerequisites

Before starting, ensure you have the following installed:
- Python 3.9 or higher
- MongoDB
- Git

#### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/software-students-spring2025/2-web-app-s2gb.git
   cd 2-web-app-s2gb
2. **Set up a virtual environment (recommended)**
   ```bash
   python -m venv venv
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # venv\Scripts\activate
4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
6. **Ensure MongoDB is running**
   On macOS (if installed via Homebrew):
   ```bash
   brew services start mongodb-community

#### Running the Application

1. **Start the Flask application**
   ```bash
   python app.py
If port 5000 is already in use (common on macOS), you can modify app.py to use a different port (e.g., 5001) in the app.run() call

2. **Access the application**
Open your web browser and navigate to: http://localhost:5000


## Task boards

Sprint 1:  [Sprint 1 Task Board](https://github.com/orgs/software-students-spring2025/projects/110/views/1?layout=board)
