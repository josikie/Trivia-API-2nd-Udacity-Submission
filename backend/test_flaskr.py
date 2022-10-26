import os
import unittest
import json
from urllib import request
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('mydb','mydb','localhost:5432', self.database_name)

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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_paginate_questions(self):
        req = self.client().get('/questions')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['current_category'], '')
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_404_paginate_questions(self):
        req = self.client().get('/questions?page=234040')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['success'], False)

    def test_questions_by_category(self):
        req = self.client().get('/categories/3/questions')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 3)

    def test_404_question_by_category(self):
        req = self.client().get('/categories/4550044/questions')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_search_question(self):
        req = self.client().post('/questions', json={'searchTerm' : 'What'})
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], '')

    def test_200_questions_by_category(self):
        req = self.client().post('/questions', json={'searchTerm' : 'owodnjendjenw'})
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], '')
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)

    # def test_delete_questions(self):
    #     req = self.client().delete('/questions/5')
    #     data = json.loads(req.data)
    #     self.assertEqual(req.status_code, 200)
    #     self.assertEqual(data['success'], True)
    
    def test_422_delete_questions(self):
        req = self.client().delete('/questions/1')
        data = json.loads(req.data)
        self.assertEqual(req.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_categories(self):
        req = self.client().get('/categories')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_404_categories(self):
        req = self.client().get('/categoriess')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_question(self):
        req = self.client().post('/questions', json={'question' : 'Whose autobiography is entitled \'I Know Why the Caged Bird Sings\'?', 'answer' : 'Maya Angelou', 'difficulty' : 2, 'category' : 4})
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_422_create_question(self):
        req = self.client().post('/questions', json={'id' : 23, 'question' : 'Whose autobiography is entitled \'I Know Why the Caged Bird Sings\'?', 'answer' : 'Maya Angelou', 'difficulty' : 2, 'category' : 4})
        data = json.loads(req.status_code)

        self.assertEqual(req.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_422_create_question(self):
        req = self.client().post('/questions', json={'answer' : 'Maya Angelou', 'difficulty' : 2})
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()