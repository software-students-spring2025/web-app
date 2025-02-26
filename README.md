# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

A minimalist and intuitive to-do list app designed for simple and quick task management.

## User stories

- As a student, I want to sign up so I can track my to-do.
- As a developer, I want to edit so I can be flexible with my to-do.
- As a professor, I want to delete so I can remove to-dos that are no longer relevant.
- As an enterpreneur, I want to finish so I can list my to-do as done and feel good about it.
- As a busy CEO, I want to search so I can remember my to-do.
- As a writer, I want to see a display of my to-do so I can visualize my progress.
- As a non-tech savvy user, I want a simple interface so I can easily use the app.
- As a teacher, I want to prioritize tasks, so I can focus on the most important ones first.

## Screens

1. **Login Screen:**

   - **Purpose:** Authenticate the user.
   - **Database Interaction:** Verify credentials against stored user data.
   - Endpoints:
     - POST /login (username + passsword)
     - POST /signup (username + passsword)

2. **Todo List Screen:**

   - **Purpose:** Display all todos (retrieved from the database) in a clear, ordered manner (e.g., by deadline).
   - **Database Interaction:** Reads data from the database.
   - Endpoints:
     - GET /todos

3. **Todo Detail Screen:**

   - **Purpose:** Show detailed information for a selected todo, including deadline, details, and status.
   - **Database Interaction:** Displays data fetched from the database.
   - Endpoints:
     - GET /todos/<id>

4. **Add Todo Screen:**

   - **Purpose:** Allow the user to add a new todo.
   - **Database Interaction:** Inserts new data into the database.
   - Endpoints:
     - POST /todos

5. **Edit/Delete Todo Screen:**

   - **Purpose:** Enable the user to modify an existing todo (update deadline, details, etc.).
   - **Database Interaction:** Updates existing data in the database.

- Endpoints:
    - PUT /todos/<id>
    - DELETE /todos/<id>

6. **Search Screen:**
   - **Purpose:** Allow the user to search for todos using keywords or deadlines.
   - **Database Interaction:** Queries the database based on user input.
   - Endpoints:
     - (same as above) GET /todos?filtersxyz=123

## Steps necessary to run the software

### Prerequisites

- Docker and Docker Compose installed on your system

### Setup and Run

Make sure [docker](https://www.docker.com/) is installed on your machine

1. Clone this repository:

   ```
   git clone https://github.com/software-students-spring2025/2-web-app-bytebuddies.git
   cd 2-web-app-bytebuddies
   ```

2. Create a `.env` file based on the `.env.example` template:

   ```
   cp .env.example .env
   ```

3. Start the application with Docker Compose:

   ```
   docker-compose up -d
   ```

4. Access the application in your browser at:

   ```
   http://localhost:8000
   ```

5. To stop the application:

   ```
   docker-compose down
   ```

6. To stop the application and remove volumes:

   ```
   docker-compose down -v
   ```

## Task boards

<https://github.com/orgs/software-students-spring2025/projects/30>
