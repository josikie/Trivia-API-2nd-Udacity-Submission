# Backend - Trivia API

Trivia API is a REST API build for trivia game (frontend in this project) but you can use it too for other applications. 

All backend Code follows [PEP8 style guidelines](https://pep8.org/#introduction).

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

In the backend directory, make file config.py. config.py contains your configuration for host, user, and password. Example of config.py:
```SQL
DB_HOST="localhost:5432"
DB_USER="yourdb"
DB_PASSWORD="yourpassword"
```
Configure setup.sql in the main directory with match database user and password that you set in config.py.

Go to main directory of project, run postgres with default user and default database in postgres:

```bash
psql postgres postgres
```

Create database trivia, trivia_test, and user mydb with this command (postgres command already created on setup.sql so you just can run it with meta-command to do that in your local environment):

```bash
\i setup.sql
```

Go to the backend directory. From the `backend` folder in terminal populate the database using the `trivia.psql` file provided with run this command:

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

Using FLASK_DEBUG=TRUE in debug mode. Everytime you make changes, you don't need to run `flask run` again. Everytime you made error, it will help you by locate the error in the terminal. Don't use debug mode in production deployment.

## API Reference

Our API is a REST API. The API can receive json object body request, search parameters, and integer parameters for pagination. The return response from the server is a json object. You can use this API in the local environment, We don't host it online.

### Getting Started

- Base URL : For now, this API can only run locally and is not hosted as base URL. Hosted at the default localhost, `http://localhost:5000/`.

### Error Handling
There are four errors handler for four errors. The errors returned json object in the following format:

```json
{
  'success' : False,
  'message' : 'resource not found',
  'error' : 404
}
```

These are three errors type when requests fail:
- 400: bad request
- 404: resource not found
- 422: unprocessable

### Endpoints
There are six endpoints you can access to do something with data:

`GET '/api/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Return: A json object with key `success` contains boolean value and, `categories` contains an object of `id: category_string` key: value pairs.

Try in curl: `curl http://localhost:5000/api/categories`

Result and the structur of endpoint response:
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

`GET '/api/questions'`

- Fetches all questions, paginated by 10 books per page.
- Request Parameters: default is '/1', or specify the page number by other number.
- Request Arguments: None
- Return: A json object with key `success` contains boolean values, `questions` contains list of questions, `total_questions` contains total of all questions in the database, `categories` contains an object of `id: category_string` key: value pairs, and `current_category` contains ''.

Try in curl `curl http://localhost:5000/api/questions`

Result and the structur of endpoint response:
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "",
  "questions": [
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ],
  "success": true,
  "total_questions": 15
}
```

`POST 'api/quizzes'`

- Fetches next quizz by its category.
- Request Arguments: a json object request with key `previous_questions` contains the list of previous question ids, and the `quiz_category` contains the category for next quiz.
- Return: A json object with key `success` contains boolean value, `question` contains the selected question for next question, `previous` contains list of the previous question ids, `total_questions` contains total questions of this quiz session.

Try in curl: `curl -X POST http://localhost:5000/api/quizzes -H 'Content-Type: application/json' -d '{"previous_questions":[2],"quiz_category":{"id":2}}'`

Result and the structur of endpoint response:
```json
{
  "previous": [
    2
  ],
  "question": {
    "answer": "One",
    "category": 2,
    "difficulty": 4,
    "id": 18,
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  },
  "success": true,
  "total_questions": 3
}
```

`GET '/api/categories/<int:category_id/questions'`

- Fetches all questions based on its category.
- Request Parameters: the number category in integer.
- Return: A json object with key `success` contains boolean value, `total_questions` contains total questions of the specific category, `current_category` contains the current_category id, `questions` contains list of questions based on its category.

Try in curl: `curl http://localhost:5000/api/categories/2/questions`

Result and the structur of endpoint response:
```json
{
  "current_category": 2,
  "questions": [
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

`DELETE 'api/questions/<int:question_id>'`

- Deleted specific question.
- Request Parameters: question id.
- Return: A json object with key `success` contains boolean value.

Try in curl: `curl -X DELETE http://localhost:5000/api/questions/15`

Result and the structur of endpoint response:
```json
{
  "success": true
}
```

`POST '/api/questions'`

- Create a new question.
- Request arguments: A json object with key `question` contains a question, `answer` contains the answer of the question, `difficulty` contains the level of the difficulty (range 1 - 5), `category` contains category of the question (it's a number, check categories endpoint to know what number what category).
- Return: A json object with key `success` contains boolean value.

Try in curl: `curl -X POST http://localhost:5000/api/questions -H 'Content-Type: application/json' -d '{"question" : "Whose autobiography is entitled I Know Why the Caged Bird Sings?", "answer": "Maya Angelou", "difficulty":2, "category":4}'`

Result and the structur of endpoint response: 
```json
{
  "success": true
}
```

`POST '/api/questions'`

- Search Questions with search term.
- Request Arguments: A json object with key `searchTerm` contains the word or search term user type.
- Return: A json object with key `success` that contains boolean value, `questions` contains list of filtered questions, `total_questions` contains the total of filtered questions, `current_category` contains `All`.

Try in curl: `curl -X POST http://localhost:5000/api/questions -H 'Content-Type: application/json' -d '{"searchTerm":"which"}'`

Result and the structur of endpoint response:
```json
{
  "current_category": "All",
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true,
  "total_questions": 5
}
```
## Testing

I write the backend API using TDD paradigm. TDD is abbreviation of Test Driven Development, where I write test code first to define the behaviour of endpoint, run the test code, watch it fails, write the endpoint code, run it again until my endpoint behaviour match and passed the test. After an endpoint passed the test, I continue to write another test code for another endpoint. The process continue over and over until all needed endpoints created. 

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

### Contribute
If you want to make contributions, you can work in backend folder. Contributions example: adding new endpoints.

