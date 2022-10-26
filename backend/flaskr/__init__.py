import json
from multiprocessing import current_process
import os
from unittest import result
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginated_questions(request, questions):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        thequestions = [question.format() for question in questions]
        current_questions = thequestions[start:end]
        return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    with app.app_context():
        setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={f"/*" : {'origins' : '*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # set response header
    @app.after_request
    def afterRequest(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,PATCH,DELETE,OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def getCategories():
        categories = {}
        results = Category.query.all()
        if results is None:
            abort(404)
        for category in results:
            categories[category.id] = category.type
            
        return jsonify({
            'success' : True,
            'categories' : categories
        })
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def getPaginatedQuestions():
        questions = Question.query.order_by(Question.id).all()
        paginated = paginated_questions(request, questions)
        if len(paginated) == 0:
            abort(404)

        categories = Category.query.order_by(Category.id).all()
        results = {}
        for category in categories:
            results[category.id] = category.type

        return jsonify({
            'success' : True,
            'questions' : paginated,
            'total_questions' : len(Question.query.all()),
            'categories' : results,
            'current_category' : '',
        })    

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def deleteQuestion(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({
                'success' : True
            })
        except:
            abort(422)
            

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions', methods=['POST'])
    def createOrSearchQuestions():
        body = request.get_json()
        questionId = body.get('id', None)
        if questionId:
            abort(400)
        theQuestion = body.get('question', None)
        questionAnswer = body.get('answer', None)
        questionDifficulty = body.get('difficulty', None)
        questionCategory = body.get('category', None)
        searchTerm = body.get('searchTerm', None)
        try:
            if searchTerm:
                # take title
                title = searchTerm
                # filter all question with that title
                filteredQuestions = Question.query.filter(Question.question.ilike('%' + title + '%')).all()
                # return 'success', 'questions', 'total_questions', 'current_category'
                return jsonify({
                    'success' : True,
                    'questions' : [filteredQuestion.format() for filteredQuestion in filteredQuestions],
                    'total_questions' : len(filteredQuestions),
                    'current_category' : '',
                })
            elif questionCategory:
                question = Question(question=theQuestion,answer=questionAnswer,category=questionCategory,difficulty=questionDifficulty)
                question.insert()
                return jsonify({
                    'success' : True
                })
            else:
                abort(422)
        except:
            abort(422)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def getQuestionsByCategory(category_id):
        # get specific category 
        category = Category.query.filter_by(id=category_id).one_or_none()
        if category is None:
            abort(404)
        # get all question's of that category
        questions = category.questions
        # return json object
        return jsonify({
            'success' : True,
            'total_questions' : len(questions),
            'current_category' : category_id,
            'questions' : [question.format() for question in questions]
        })
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    def random_question(quizCategory, previousQuestions):
        # if the category is 0, then fetch all questions in the database
        if quizCategory == 0:
            allQuestions = Question.query.order_by(Question.id).all()
        # if the category is not 0, then fetch specific questions based on its category number in the database
        else:
            allQuestions = Question.query.order_by(Question.id).filter(Question.category==quizCategory).all()
        
        # change the fetched data type to list
        questions = [allQuestion.format() for allQuestion in allQuestions]

        # initialize total questions
        totalQuestions = 0
        if quizCategory == 0:
            totalQuestions = 5
        else :
            if len(questions) < 5:
                totalQuestions = len(questions)
            else:
                totalQuestions = 5

        # get random number
        randomNumber = random.randint(1, len(questions))
        # do function recursive if random question is in previous questions
        for previousQuestion in previousQuestions:
            if previousQuestion == randomNumber and randomNumber-1 <= len(questions):
                random_question(questions, previousQuestions)
        randomQuestion = questions[randomNumber-1]
        return [randomQuestion, totalQuestions]

    @app.route('/quizzes', methods=['POST'])
    def getNextQuestion():
        
        body = request.get_json()
        previousQuestions = body.get('previous_questions', None)
        quizCategory = body.get('quiz_category', None)
        if quizCategory is None:
            abort(404)
        categoryNumber = quizCategory['id']
        question = random_question(categoryNumber, previousQuestions)

        return jsonify({
            'success' : True,
            'question' : question[0],
            'previous' : previousQuestions,
            'total_questions' : question[1]
        })


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def badRequest(error):
        return jsonify({
            'success' : False,
            'message' : 'bad request',
            'error' : 400
        }), 400
    @app.errorhandler(404)
    def notFound(error):
        return jsonify({
            'success' : False,
            'message' : 'resource not found',
            'error' : 404
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success' : False,
            'message' : 'unprocessable',
            'error' : 422
        }), 422
    return app

