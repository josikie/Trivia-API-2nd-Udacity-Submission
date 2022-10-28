import os
from unicodedata import category
import unittest
import json
from urllib import request
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from dotenv import load_dotenv

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST, self.database_name)

        # binds the app to the current context
        with self.app.app_context():
            setup_db(self.app, self.database_path)
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_base_url(self):
        req = self.client().get('/api')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['message']))
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_paginate_questions(self):
        req = self.client().get('/api/questions')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['current_category'], '')
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_404_paginate_questions(self):
        req = self.client().get('/api/questions?page=234040')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['success'], False)

    def test_questions_by_category(self):
        req = self.client().get('/api/categories/3/questions')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 3)

    def test_404_question_by_category(self):
        req = self.client().get('/api/categories/4550044/questions')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_search_question(self):
        req = self.client().post('/api/questions', json={'searchTerm' : 'What'})
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 'All')

    def test_200_search_questions_by_category(self):
        req = self.client().post('/api/questions', json={'searchTerm' : 'owodnjendjenw'})
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 'All')
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)

    # def test_delete_questions(self):
    #     req = self.client().delete('/api/questions/20')
    #     data = json.loads(req.data)
    #     self.assertEqual(req.status_code, 200)
    #     self.assertEqual(data['success'], True)
    
    def test_422_delete_questions(self):
        req = self.client().delete('/api/questions/0')
        data = json.loads(req.data)
        self.assertEqual(req.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_categories(self):
        req = self.client().get('/api/categories')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_404_categories(self):
        req = self.client().get('/api/categoriess')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_question(self):
        req = self.client().post('/api/questions', json={'question' : 'Whose autobiography is entitled \'I Know Why the Caged Bird Sings\'?', 'answer' : 'Maya Angelou', 'difficulty' : 2, 'category' : 4})
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_422_create_question(self):
        req = self.client().post('/api/questions', json={'id' : 23, 'question' : 'Whose autobiography is entitled \'I Know Why the Caged Bird Sings\'?', 'answer' : 'Maya Angelou', 'difficulty' : 2, 'category' : 4})
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_422_create_question(self):
        req = self.client().post('/api/questions', json={'answer' : 'Maya Angelou', 'difficulty' : 2})
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_next_question(self):
        with self.app.app_context():
            previous_questions = Question.query.order_by(Question.id).filter(Question.category==2).all()
            questions = [previous_question.id for previous_question in previous_questions]
        req = self.client().post('/api/quizzes', json={'previous_questions' : questions[0:1], 'quiz_category' : {'id' : 2}})
        data = json.loads(req.data)
        print(data['question'])
        print(data['previous'])

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len([data['question']]), 1)

    def test_404_get_next_question(self):
        with self.app.app_context():
            previous_questions = Question.query.order_by(Question.id).filter(Question.category==2).all()
            questions = [previous_question.id for previous_question in previous_questions]
        req = self.client().post('/api/quizzes', json={'previous_questions' : questions[0:1]})
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    
    def test_get_next_question_all_category(self):
        with self.app.app_context():
            previous_questions = Question.query.order_by(Question.id).all()
            questions = [previous_question.id for previous_question in previous_questions]
        req = self.client().post('/api/quizzes', json={'previous_questions' : questions[0:2], 'quiz_category' : {'id' : 0}})
        data = json.loads(req.data)
        print(f'\n{data}')

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len([data['question']]), 1)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()