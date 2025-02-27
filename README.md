# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

See instructions. Delete this line and place the Product Vision Statement here.

## User stories

See instructions. Delete this line and place a link to the user stories here.

## Steps necessary to run the software

### Build and launch the database

If you have not already done so, start up a MongoDB database:

-   run command, `docker run --name mongodb_dockerhub -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=secret -d mongo:latest`

The back-end code will integrate with this database. However, it may be occasionally useful interact with the database directly from the command line:

-   connect to the database server from the command line: `docker exec -ti mongodb_dockerhub mongosh -u admin -p secret`
-   show the available databases: `show dbs`
-   select the database used by this app: `use example`
-   show the documents stored in the `messages` collection: `db.messages.find()` - this will be empty at first, but will later be populated by the app.
-   exit the database shell whenever you have had your fill: `exit`

### Create a `.env` file

Copy the content of `.env` form the version shared in our Discord channel.

### Using pipenv

The ability to make virtual environemnts with [pipenv](https://pypi.org/project/pipenv/) is relatively easy, but it does not come pre-installed with Python. It must be installed.

Install `pipenv` using `pip`:

```
pip3 install pipenv
```

Activate it:

```
pipenv shell
```

Your command line will now be running within a virtual environment.

The file named, `Pipfile` contains a list of dependencies - other Python modules that this app depends upon to run. These will have been automatically installed into the virtual environment by `pipenv` when you ran the command `pipenv shell`.

### Run the app

#### Development server

To run the app locally in development mode using Flask's built-in development web server:

-   define two environment variables from the command line:
    -   on Mac, use the commands: `export FLASK_APP=app.py` and `export FLASK_ENV=development`.
    -   on Windows, use `set FLASK_APP=app.py` and `set FLASK_ENV=development`.
-   start flask with `flask run` - this will output an address at which the app is running locally, e.g. https://127.0.0.1:5000. Visit that address in a web browser.
-   in some cases, the command `flask` will not be found when attempting `flask run`... you can alternatively launch it with `python3 -m flask run --host=0.0.0.0 --port=5000` (or change to `python -m ...` if the `python3` command is not found on your system).

Note that this will run the app only on your own computer. Other people will not be able to access it. If you want to allow others to access the app running in development mode on your local machine, try using the [flask-ngrok](https://pypi.org/project/flask-ngrok/) module.

### Populate db data

To populate initial data in your local instance of the database, run `python populate_db_data.py`

## Task boards

See instructions. Delete this line and place a link to the task boards here.
