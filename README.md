# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where I come in! I help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app give me the ability to structure plan, implement, and test an API - skills essential for enabling my future applications to communicate with others.

## About the Stack

Udacity team give me the started of the full stack application. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. I work primarily in `__init__.py` to define my endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files I edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`
> View the [Backend README](./backend/README.md) for more details. 

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. I read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

I pay special attention to what data the frontend is expecting from each API response to help guide how I format my API. The places where I may change the frontend behavior, and where I'm looking for the above information, are marked with `TODO`. These are the files I edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

I practice the core skill of being able to read, understand code, and structur simple plan to follow to build out the endpoints of my backend API

> View the [Frontend README](./frontend/README.md) for more details.

### IDE and Other Tools
I use Visual Studio code for the IDE, and Git Bash to run command lines. Download [Visual Code](https://code.visualstudio.com/download) and [Git Bash](https://git-scm.com/downloads)

### Authors
1. Udacity's Team (code starter and frontend)
2. Josi Kie (backend API and a little changes in frontend logic)

### Code Starter
Code starter is from [Udacity API Development And Documentation Project](https://github.com/udacity/cd0037-API-Development-and-Documentation-project)
