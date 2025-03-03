# LFG (Looking For Group) App


## Web Application Exercise
A little exercise to build a web application following an agile development process. See the instructions for more detail.


---


## Team Members
- **Chen Jun Hsu**: [Junpapadiamond](https://github.com/Junpapadiamond)
- **Brandon**: [BAMOEQ](https://github.com/BAMOEQ)
- **Steve Lin**: [Echoudexigaigu](https://github.com/Echoudexigaigu)
- **Eric Zhao**: [Ericzzy675](https://github.com/Ericzzy675)


---


## Product Vision Statement
The **LFG App** helps gamers find teammates quickly by posting and searching for multiplayer game listings.


---


## User Stories


### As a Gamer:
- I want to post an LFG listing so that I can find teammates.
- I want to include specific descriptions to better find potential teammates.
- I want to search listings by game to find a better match.
- I want to search posts by my level to find the best match.


### As a Poster:
- I want to edit my listing to update details in case I make mistakes.
- I want to delete my listing when I find a group.


### As a User:
- I want to edit my profile, including username, profile pic, and pinned postings.
- I want to have a login feature to manage my posts securely.


### As an Admin:
- I want to search descriptions to keep track of inappropriate speech.
- I want to have more access to remove inappropriate posts.
- I want exclusive access to prevent others from removing my posts.


---


## Steps to Run the Software
Make sure **[Docker](https://www.docker.com/)** is installed on your machine.


1. **Clone this repository:**
```bash
git clone https://github.com/software-students-spring2025/2-web-app-ez-squad-2-0
cd 2-web-app-ez-squad-2-0 

2. **Create a .env file based on the .env.example template:**
```bash
cp .env.example .env

3. **Start the application with Docker Compose:**
```bash
docker-compose up -d

4. **Access the application in your browser at:**
```bash
http://localhost:5001

5. **To stop the application:**
```bash
docker-compose down

6. **To stop the application and remove volumes:**
```bash
docker-compose down -v

---


## Task Boards
[Task Board Sprint 1 Link](https://github.com/orgs/software-students-spring2025/projects/30)
