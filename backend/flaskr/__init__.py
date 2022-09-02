import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random
import sys
from marshmallow import ValidationError

from models import (
            setup_db,
            Question,
            Category,
            QuestionSchema,
            CategorySchema)

QUESTIONS_PER_PAGE = 10


def paginate_objects(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    objects = [object.format() for object in selection]
    current_objects = objects[start:end]

    return current_objects


def format_categories(categories):
    categoryIdList = []
    categoryTypeList = []

    for category in categories:
        categoryIdList.append(category.id)
        categoryTypeList.append(category.type)

    return {key: value for key, value in zip(categoryIdList, categoryTypeList)}


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    setup_db(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization,true'
                             )
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS'
                             )
        return response

    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {}

        if len(categories) == 0:
            abort(404)

        formatted_categories = format_categories(categories)

        return jsonify({
            "success": True,
            "status": 200,
            "categories": formatted_categories
        })

    @app.route('/questions')
    def get_questions():
        current_questions = []
        formatted_categories = {}
        currentCategory = ""

        questionSelection = Question.query.order_by(Question.id).all()
        current_questions = paginate_objects(request, questionSelection)

        if len(current_questions) == 0:
            abort(404)

        question = random.choice(questionSelection)
        currentCategory = Category.query.get(question.category).type

        categories = Category.query.order_by(Category.id).all()
        if len(categories) > 0:
            formatted_categories = format_categories(categories)

        return jsonify({
            "success": True,
            "status": 200,
            "questions": current_questions,
            "total_questions": len(questionSelection),
            'categories': formatted_categories,
            "currentCategory": currentCategory
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(
            Question.id == question_id
            ).one_or_none()

        if question is None:
            abort(404)

        try:
            question.delete()
            return jsonify({
                "success": True,
                "status": 200,
                "deleted": question_id
            })
        except Exception:
            print(sys.exc_info())
            abort(422)

    @app.route("/questions", methods=["POST"])
    def search_create_question():
        body = request.get_json()

        if 'searchTerm' in body:
            searchTerm = body.get("searchTerm")
            selection = Question.query.filter(
                Question.question.ilike(f'%{searchTerm}%')
                ).order_by(Question.id).all()

            current_questions = paginate_objects(request, selection)

            if len(current_questions) == 0:
                return jsonify({
                    "success": True,
                    "status": 200,
                    "questions": current_questions,
                    "totalQuestions": len(selection),
                    "currentCategory": ""
                })

            question = random.choice(selection)
            currentCategory = Category.query.get(question.category).type

            return jsonify({
                "success": True,
                "status": 200,
                "questions": current_questions,
                "totalQuestions": len(selection),
                "currentCategory": currentCategory
            })
        else:
            try:
                schema = QuestionSchema()
                result = schema.load(body)
            except ValidationError as err:
                abort(400)

            new_question = body.get("question", None)
            new_answer = body.get("answer", None)
            new_category = body.get("category", None)
            new_difficulty = body.get("difficulty", None)

            category = Category.query.filter(
                Category.id == new_category
                ).one_or_none()

            if category is None:
                abort(404, "category not found")

            sameQuestions = Question.query.filter(
                Question.question.ilike(f'%{new_question}%')
                ).order_by(Question.id).all()

            if len(sameQuestions) > 0:
                abort(409, "duplicated question")

            try:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    category=new_category,
                    difficulty=new_difficulty
                    )
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_objects(request, selection)

                return jsonify({
                    "success": True,
                    "status": 200
                })
            except Exception:
                print(sys.exc_info())
                abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        category = Category.query.filter(
            Category.id == category_id
            ).one_or_none()

        if category is None:
            abort(404, "category not found")

        selection = Question.query.filter(
            Question.category == category_id
            ).order_by(Question.id).all()

        current_questions = paginate_objects(request, selection)

        if len(current_questions) == 0:
            return jsonify({
                "success": True,
                "status": 200,
                "questions": current_questions,
                "totalQuestions": len(Question.query.all()),
                "currentCategory": category.type
            })

        return jsonify({
            "success": True,
            "status": 200,
            "questions": current_questions,
            "totalQuestions": len(Question.query.all()),
            "currentCategory": category.type
        })

    @app.route("/categories", methods=["POST"])
    def create_category():
        body = request.get_json()
        try:
            schema = CategorySchema()
            result = schema.load(body)
        except ValidationError as err:
            return jsonify(err.messages), 400

        new_type = body.get("type", None)
        sameCategory = Category.query.filter(
            Category.type.ilike(f'%{new_type}%')
            ).order_by(Category.id).all()

        if len(sameCategory) > 0:
            abort(409, "duplicated category")

        try:
            category = Category(type=new_type)
            category.insert()

            selection = Category.query.order_by(Category.id).all()
            current_categories = format_categories(selection)

            return jsonify({
                "sucess": True,
                "status": 200,
                "added category": new_type
            })
        except Exception:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def quizz():
        try:
            body = request.get_json()
            previous_questions = body.get("previous_questions")
            quiz_category_id = body.get("quiz_category")['id']

            category = Category.query.filter(
                Category.id == quiz_category_id
                ).one_or_none()

            if category is None:
                questions = Question.query.filter(
                    ~Question.id.in_(previous_questions)
                    ).order_by(Question.id).all()

            else:
                questions = Question.query.filter(
                    ~Question.id.in_(previous_questions),
                    Question.category == category.id
                    ).order_by(Question.id).all()

            if len(questions) == 0:
                return jsonify({
                    "success": True,
                    "status": 200,
                    "question": ""
                })

            current_questions = paginate_objects(request, questions)
            question = random.choice(current_questions)

            return jsonify({
                "success": True,
                "status": 200,
                "question": question
            })
        except Exception:
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({"success": False,
                         "error": 400,
                         "message": "bad request"}),
                400)

    @app.errorhandler(404)
    def not_found(error, message="resource not found"):
        return (jsonify({
                        "success": False,
                        "error": 404,
                        "message": message}),
                404)

    @app.errorhandler(409)
    def resource_conflict(error, message="resources conflict"):
        return (jsonify({
                        "success": False,
                        "error": 409,
                        "message": message}),
                409)

    @app.errorhandler(422)
    def unprocessable(error):
        return (
                jsonify({
                        "success": False,
                        "error": 422,
                        "message": "unprocessable"}),
                422)

    return app
