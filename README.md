# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

A mobile friendly app that helps travelers find compatible travel partners based on their personal preferences and traveling habits which fosters a new way to meet friends and emphasize traveling safely.

## User stories


- As a traveler, I want to create a profile with my travel preferences (e.g., early airport arrival, budget, favorite food) so that I can showcase what matters to me.
- As a college graduate, I would like to create a profile for my trip to London, so I am able to create a group of like-minded travelers. 
- As a budgeting traveler, I would like to find other budgeting travelers, so I am able to travel efficiently on a budget.
- As a traveler, I want to view a list of potential travel partners whose profiles match my preferences so that I can choose a compatible partner.
- As a frequent traveler, I want to update my travel preferences whenever they change so that my profile stays accurate.
- As a traveler, I want to message potential travel partners directly within the app so that I can easily discuss and coordinate travel details.
- As a traveler, I want to search for specific travel partners based on criteria (like budget or travel style) so that I can quickly find what I need.
- As a solo traveler, I would like to find other solo travelers that enjoy the same food cuisines as me, so I am able to enjoy new types of food. 
- As a traveler, I want to receive notifications when new profiles that match my travel criteria are added so that I never miss an opportunity to connect with a compatible partner.
- As a traveler, I want to bookmark profiles of potential travel partners so that I can easily compare and revisit them before making a connection.

https://github.com/software-students-spring2025/2-web-app-diet-coke/issues/


## Steps necessary to run the software

### Prerequisites
- Python 3.8 or higher
- MongoDB (local installation or MongoDB Atlas account)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   - Copy the example environment file:
     ```bash
     cp env.example .env
     ```
   - Edit the `.env` file with your specific configuration:
     - Set `MONGO_URI` to your MongoDB connection string
     - Set a secure `SECRET_KEY` for Flask session management

6. **Run the application**
   ```bash
   flask run
   ```
   The application will be available at http://127.0.0.1:5000/

## Task boards

https://github.com/orgs/software-students-spring2025/projects/56/views/1
