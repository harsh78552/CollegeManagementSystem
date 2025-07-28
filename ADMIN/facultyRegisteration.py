import cloudinary.uploader
from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint
from DATABASE.FACULTY.facultyDatabase import FacultyDatabase
from SCHEMA.FACULTY.facultySchema import FacultyRegistrationSchema

blp = Blueprint('faculty-registeration', __name__, description='faculty registered from here')


@blp.route('/faculty-registration')
class FacultyRegisteration(MethodView):
    def __init__(self):
        self.faculty_db = FacultyDatabase()

    @blp.arguments(FacultyRegistrationSchema)
    def post(self, request_data):
        name = request_data['name']
        contact = request_data['contact']
        email = request_data['email']
        password = request_data['password']
        subject = request_data['subject']
        qualification = request_data['qualification']
        blood_group = request_data['blood_group']
        role = request_data['role']
        image_file = request.files.get('image')
        if image_file:
            upload_image = cloudinary.uploader.upload(image_file)
            image_url = upload_image['secure_url']
        else:
            image_url = None
        response = self.faculty_db.insert_data(name, contact, email, password, role, subject, qualification, blood_group
                                               , image_url)
        return jsonify(response)
