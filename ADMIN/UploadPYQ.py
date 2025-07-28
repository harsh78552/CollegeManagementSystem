from DATABASE.ADMIN.AdminPYQ import AdminQuestionPaperUploadDatabase
import cloudinary.uploader
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from DATABASE.AdminPYQ import AdminQuestionPaperUploadDatabase
import cloudinary.uploader

blp = Blueprint('admin upload pyq', __name__, description='admin upload pyq api')


@blp.route('/upload-paper')
class UploadPYQ(MethodView):
    def __init__(self):
        self.paper_db = AdminQuestionPaperUploadDatabase()

    def post(self):
        semester = request.form.get('semester')
        year = request.form.get('year')
        paper_type = request.form.get('paperType')
        subject = request.form.get('subject')
        paper_file = request.files.get('file')
        try:
            upload_result = cloudinary.uploader.upload(
                paper_file,
                resource_type="auto",
                public_id=f"{subject}_{paper_type}_{semester}",
                overwrite=True
            )
            pdf_url = upload_result['secure_url']
        except Exception as error:
            return {"error": str(error)}, 503
        response = self.paper_db.insertPYQ(semester, year, paper_type, subject, pdf_url)
        return response
