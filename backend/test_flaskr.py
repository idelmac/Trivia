import os
from unicodedata import category
import unittest
import json
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
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(
                                                            'postgres',
                                                            '12345678',
                                                            'localhost:5432',
                                                            self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_200_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_200_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['currentCategory'])

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=99999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        res = self.client().delete('/questions/21')
        data = json.loads(res.data)

        question = Question.query.filter(
                                        Question.id == 21
                                        ).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertEqual(data['deleted'], 21)
        self.assertEqual(question, None)

    def test_404_if_question_does_not_exist(self):
        res = self.client().delete("/question/99999")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_200_get_question_search_with_results(self):
        res = self.client().post("/questions", json={"searchTerm": "africa"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 1)
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(data["currentCategory"])

    def test_200_get_question_search_without_results(self):
        res = self.client().post("/questions", json={"searchTerm": ".2.5!"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 0)
        self.assertEqual(data["totalQuestions"], 0)
        self.assertEqual(data["currentCategory"], "")

    def test_200_create_new_question(self):
        question = {"question": "The best club",
                    "answer": "Real Madrid",
                    "difficulty": 1,
                    "category": 6}

        res = self.client().post("/questions", json=question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_400_if_question_bad_request(self):
        question = {"question": "The best club",
                    "answer": "Real Madrid",
                    "category": 6}

        res = self.client().post("/questions", json=question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_404_if_question_category_does_not_exist(self):
        question = {"question": "The best club",
                    "answer": "Real Madrid",
                    "difficulty": 1,
                    "category": 9999}

        res = self.client().post("/questions", json=question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_409_if_question_is_duplicated(self):
        question = {"question": "What is the largest lake in Africa?",
                    "answer": "Lake Victoria",
                    "difficulty": 1,
                    "category": 3}

        res = self.client().post("/questions", json=question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resources conflict")

    def test_200_get_category_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['totalQuestions'], 20)
        self.assertEqual(data['currentCategory'], "Science")

    def test_404_if_category_questions_does_not_exist(self):
        res = self.client().get("/categories/9999/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_200_get_quizz(self):
        previous_questions = [20, 21]
        category = {'type': 'Science', 'id': '1'}

        res = self.client().post(
                                "/quizzes",
                                json={
                                    "previous_questions": previous_questions,
                                    "quiz_category": category})
        data = json.loads(res.data)

        question = Question.query.filter(
                                        ~Question.id.in_(previous_questions),
                                        Question.category == category['id']
                                        ).order_by(Question.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))

    def test_200_get_quizz_withouth_questions(self):
        previous_questions = [20, 21, 22]
        category = {'type': 'Science', 'id': '1'}

        res = self.client().post(
                                "/quizzes",
                                json={
                                    "previous_questions": previous_questions,
                                    "quiz_category": category})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], "")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
