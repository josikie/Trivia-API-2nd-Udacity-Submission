import json
from multiprocessing import current_process
import os
from unicodedata import category
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
    cors = CORS(app, resources={f"/api/*" : {'origins' : '*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # set response header
    @app.after_request
    def afterRequest(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,PATCH,DELETE,OPTIONS')
        return response

    # endpoint for base url
    @app.route('/api')
    def api_endpoint():
        message = ['This endpoint without data, to do something or access the endpoint use this urls:', {
            'Get Categories' : 'GET /api/categories',
            'Get Questions' : 'GET /api/questions',
            'Delete Questions' : 'DELETE /api/questions/<int:question_id>',
            'Create or Search Questions' : 'POST /api/questions',
            'Get Questions by Category' : 'GET /api/categories/<int:category_id>/questions',
            'Get Next Quiz' : 'POST /api/quizzes'
        }]

        return jsonify({
            'success' : True,
            'message' : message
        })

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/api/categories')
    def getCategories():
        try:
            categories = {}
            results = Category.query.all()
            for category in results:
                categories[category.id] = category.type
                
            return jsonify({
                'success' : True,
                'categories' : categories
            })
        except:
            abort(404)
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
    @app.route('/api/questions')
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
    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
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
    @app.route('/api/questions', methods=['POST'])
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
                    'current_category' : 'All',
                })
            elif searchTerm == '':
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
            elif questionCategory and theQuestion and questionAnswer:
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
    @app.route('/api/categories/<int:category_id>/questions')
    def getQuestionsByCategory(category_id):
        # get specific category 
        try:
            category = Category.query.filter_by(id=category_id).one_or_none()
            # get all question's of that category
            questions = category.questions
            # return json object
            return jsonify({
                'success' : True,
                'total_questions' : len(questions),
                'current_category' : category_id,
                'questions' : [question.format() for question in questions]
            })
        except:
            abort(404)
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
        allQuestions = None
        firstQuestion = None
        currentQuestion = None
        # if quiz category equal to 0, then get all questions that is not in previous qestions
        if quizCategory == 0:
            allQuestions = Question.query.filter(Question.id.not_in(previousQuestions)).all()
        # if previous questions equal to zero, then get first question prior to specific category
        elif previousQuestions == 0:
            firstQuestion = Question.query.filter(Question.category==quizCategory).first()
            allQuestions = list(firstQuestion)
        else:
            allQuestions = Question.query.filter(Question.id.not_in(previousQuestions), Question.category==quizCategory).all()
        
        questions = [question.format() for question in allQuestions]

        randomMax = len(questions)
        # get random question if randomMax more than zero
        if randomMax > 0:
            currentQuestion = questions[random.randint(0, randomMax-1)]
        else:
            currentQuestion = False

        return currentQuestion

    @app.route('/api/quizzes', methods=['POST'])
    def getNextQuestion():
        # get body request
        body = request.get_json()
        previousQuestions = body.get('previous_questions', None)
        quizCategory = body.get('quiz_category', None)
        # if quiz category is none, then abort
        if quizCategory is None:
            abort(404)
        # get the id of category
        categoryNumber = quizCategory['id']

        total_questions = 0
        # if category is all (0), set total_questions to 5
        if categoryNumber == 0:
            total_questions = 5
        else:
            # get all questions based on its category
            allQuestions = Question.query.filter(Question.category==categoryNumber).all()
            listQuestions = [question.format() for question in allQuestions]
            # if number of questions less than 5, then set total_questions to the total all questions
            if len(listQuestions) < 5:
                total_questions = len(listQuestions)
            # if number of questions more than 5, then set total_questions to 5
            else: 
                total_questions = 5

        # take a random question
        question = random_question(categoryNumber, previousQuestions)

        return jsonify({
            'success' : True,
            'question' : question,
            'previous' : previousQuestions,
            'total_questions' : total_questions
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

    @app.errorhandler(500)
    def internalError(error):
        return jsonify({
            'success': False,
            'message': 'Internal Server Error',
            'error' : 500
        }), 500
    return app

