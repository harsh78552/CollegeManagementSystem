from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from DATABASE.AdminPYQ import AdminQuestionPaperUploadDatabase

blp = Blueprint("student-pyq", __name__, description='student see PYQ paper')


@blp.route('/get-pyq')
class SeePYQ(MethodView):
    def __init__(self):
        self.PYQ_db = AdminQuestionPaperUploadDatabase()

    def post(self):
        PYQdata = request.get_json()
        semester = PYQdata['semester']
        paperType = PYQdata['paperType']
        response = self.PYQ_db.getPyq(semester, paperType)
        print(response)
        return response, 200
