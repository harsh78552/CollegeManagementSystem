import os

import cloudinary
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager, unset_jwt_cookies
from flask_mail import Mail
from flask_smorest import Api

from STUDENT.studentLogin import blp as StudentLoginBlueprint
from STUDENT.studentLogout import blp as StudentLogoutBlueprint
from STUDENT.studentRegisteration import blp as StudentRegistrationBlueprint
from STUDENT.studentProfile import blp as StudentProfileBlueprint
from STUDENT.stdudentResetPassword import blp as StudentResetPasswordBlueprint
from STUDENT.studentAttendanceView import blp as StudentAttendanceBlueprint
from STUDENT.notification import blp as StudentNotificationBlueprint
from STUDENT.seeResult import blp as StudentSeeResultBlueprint
from STUDENT.editProfile import blp as StudentEditProfileBlueprint
from STUDENT.seePYQ import blp as StudentSeenPYQBlueprint

from STUDENT.books import blp as StudentBookBlueprint

from STUDENT.studentBlocklist import BLOCKLIST

from FACULTY.facultyLogin import blp as FacultyLoginBlueprint
from FACULTY.facultyLogout import blp as FacultyLogoutBlueprint
from ADMIN.facultyRegisteration import blp as FacultyRegisterationBlueprint
from FACULTY.facultyProfile import blp as FacultyProfileBlueprint
from FACULTY.attendanceMarked import blp as FacultyMarkedAttendanceBlueprint
from FACULTY.getEmail import blp as FacultyEmailBlueprint
from FACULTY.editProfile import blp as FacultyEditProfileBluePrint
from FACULTY.facultyBlocklist import BLOCKLIST

from ADMIN.adminLogin import blp as AdminLoginBlueprint
from ADMIN.adminLogout import blp as AdminLogoutBlueprint
from ADMIN.adminNotification import blp as AdminNotificationBlueprint
from ADMIN.AdminMarksheetUpload import blp as AdminMarksheetUploadBlueprint
from ADMIN.UploadPYQ import blp as AdminUploadPYQBlueprint

from LIBRARIAN.login import blp as LibrarianLoginBlueprint
from LIBRARIAN.logout import blp as LibrarianLogoutBlueprint
from LIBRARIAN.blocklist import BLOCKLIST
from LIBRARIAN.addBook import blp as LibrarianAddBookBlueprint
from LIBRARIAN.updateBook import blp as LibrarianUpdateBookBlueprint
from LIBRARIAN.issueBook import blp as LibrarianIssueBookBlueprint
from LIBRARIAN.BookSubmission import blp as LibrarianBookSubmitBlueprint
from HomePage.homePageAPI import blp as HomePageBlueprint

app = Flask(__name__)

CORS(app, origins=["http://localhost:63342"], supports_credentials=True)
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['API_TITLE'] = 'College-System'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger-ui"
app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config['JWT_SECRET_KEY'] = 'harsh8926466446jhgsfblsgwogw4lb'
app.config['SECRET_KEY'] = 'HARSH79565hergitgbslvwfcbiew'

app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config["JWT_COOKIE_SAMESITE"] = 'None'
app.config['JWT_COOKIE_HTTPONLY'] = True

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'ht728350@gmail.com'
app.config['MAIL_PASSWORD'] = "hnzx xeiq sqcj vglh"


cloudinary.config(
    cloud_name="dofbbfgg4",
    api_key="596269484844184",
    api_secret="0uzI8tt4-bGFwAZuTfOiEMEQD2o",
    secure=True
)

api = Api(app)
jwt = JWTManager(app)
mail_ = Mail(app)


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jte_header, jwt_payload):
    return jwt_payload['jti'] in BLOCKLIST


@jwt.revoked_token_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return (
        {"description": "User has been logged out....",
         'error': 'token_revoked'}
    ), 401


@app.after_request
def unset_jwt(response):
    if response.status_code == 401:
        unset_jwt_cookies(response)
    return response


api.register_blueprint(AdminLoginBlueprint)
api.register_blueprint(AdminLogoutBlueprint)
api.register_blueprint(AdminNotificationBlueprint)
api.register_blueprint(AdminMarksheetUploadBlueprint)
api.register_blueprint(HomePageBlueprint)
api.register_blueprint(AdminUploadPYQBlueprint)
api.register_blueprint(LibrarianLoginBlueprint)
api.register_blueprint(LibrarianLogoutBlueprint)
api.register_blueprint(LibrarianAddBookBlueprint)
api.register_blueprint(LibrarianUpdateBookBlueprint)
api.register_blueprint(LibrarianIssueBookBlueprint)
api.register_blueprint(LibrarianBookSubmitBlueprint)
api.register_blueprint(StudentLoginBlueprint)
api.register_blueprint(StudentLogoutBlueprint)
api.register_blueprint(StudentProfileBlueprint)
api.register_blueprint(FacultyLoginBlueprint)
api.register_blueprint(StudentNotificationBlueprint)
api.register_blueprint(StudentRegistrationBlueprint)
api.register_blueprint(StudentResetPasswordBlueprint)
api.register_blueprint(StudentAttendanceBlueprint)
api.register_blueprint(StudentSeeResultBlueprint)
api.register_blueprint(StudentEditProfileBlueprint)
api.register_blueprint(StudentBookBlueprint)
api.register_blueprint(StudentSeenPYQBlueprint)
api.register_blueprint(FacultyProfileBlueprint)
api.register_blueprint(FacultyLogoutBlueprint)
api.register_blueprint(FacultyMarkedAttendanceBlueprint)
api.register_blueprint(FacultyRegisterationBlueprint)
api.register_blueprint(FacultyEmailBlueprint)
api.register_blueprint(FacultyEditProfileBluePrint)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5005)
