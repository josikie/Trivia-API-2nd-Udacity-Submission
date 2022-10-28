# Backend - Trivia API

Trivia API is a REST API build for trivia game (frontend in this project) but you can use it too.

## Setting up the Backend

I write the backend API using TDD paradigm. TDD is abbreviation of Test Driven Development, where I write test code first for the behaviour of endpoint, run the test code, watch it fails, write the endpoint code, run it again until my endpoint behaviour match and passed the test. After an endpoint passed the test, I continue to write another test code for another endpoint. The process continue over and over until all needed endpoints created. 

For support paradigm I use, I make two databases i.e trivia and trivia_test. So there are two sets of database configuration, one in backend/test_flaskr.py and one in backend/models.py

### Install Dependencies

1. **Python 3.7** - We use python. Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Postgres** - A database management system. We use it to manage our database. Download postgres in [PostgresSQL](https://www.postgresql.org/)

3. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Here is how to install, initialize, and activate virtual environment for Python Projects:

Install virutal environment to your computer:
`pip install virtualenv`

Go to the backend directory, and create virtual environment (pip usually automatically installed if you downloaded Python from [python.org](https://www.python.org/)):

```bash
python3 -m virutalenv env
```

Run project in virutal environment:

```bash
source env/Scripts/activate
```

or read instructions for setting up a virtual environment on your platform in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

4. **PIP Dependencies** - Pip is package manager for Python, we use it to download packages from Python Indexes and other Indexes. Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](https://flask.palletsprojects.com/en/2.2.x/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

Go to main directory of project, run postgres with default user and database in postgres:

```bash
psql postgres postgres
```

Create database trivia, trivia_test, and user mydb with this command (postgres command already created on setup.sql so you just can run it with meta-command to do that in your local environment):

```bash
\i setup.sql
```

Go to the backend directory. Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql -d trivia -U postgres -a -f trivia.psql
```

### Run the Server

Go to backend directory, run this command to execute the backend server:

```bash
export FLASK_APP=flaskr
```

```bash
export FLASK_DEBUG=TRUE
```

```bash
flask run
```

Using FLASK_DEBUG=TRUE in debug mode. Everytime you make changes, you don't need to run `flask run` again to refresh it. Everytime you made error, it will help you by locate the error in the terminal. Don't use debug mode in production deployment.

## To Do Tasks

These are the files I edited in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

I'm expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. I completed the code by:

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

## Testing

I write the backend API using TDD paradigm. TDD is abbreviation of Test Driven Development, where I write test code first for the behaviour of endpoint, run the test code, watch it fails, write the endpoint code, run it again until my endpoint behaviour match and passed the test. After an endpoint passed the test, I continue to write another test code for another endpoint. The process continue over and over until all needed endpoints created. 

For support paradigm I use, I make two databases i.e trivia and trivia_test. So there are two sets of database configuration, one in backend/test_flaskr.py and one in backend/models.py

Go to the backend directory, run this command:

```bash
psql -d trivia_test -U postgres -a -f trivia.psql
```

To execute test, run this command:
```bash
python test_flaskr.py
```
or
```bash
python test_flaskr.py
```

