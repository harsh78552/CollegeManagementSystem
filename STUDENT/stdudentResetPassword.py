import secrets
import hashlib
from flask import request, render_template, jsonify
from flask.views import MethodView
from flask_mail import Message
from flask_smorest import Blueprint
from DATABASE.STUDENT.StudentDatabase import StudentDatabase

blp = Blueprint('reset-password', __name__, description='user reset password')


@blp.route('/reset-password')
class ResetPassword(MethodView):
    def __init__(self):
        self.user_db = StudentDatabase()

    def post(self):
        from app import mail_
        userMail = request.json.get('email')
        response = self.user_db.searchStudent(userMail)
        if response:
            token = secrets.token_urlsafe(32)
            # token_expiry = datetime.utcnow() + timedelta(hours=1)
            self.user_db.save_reset_token(userMail, token)
            reset_link = f"http://127.0.0.1:5005/reset-password-form/{token}"
            msg = Message(subject="Password Reset Request",
                          sender="ht728350@gmail.com",
                          recipients=[userMail],
                          body=f"Click this link to reset your password: {reset_link}")
            mail_.send(msg)
            return {"message": "Password reset link sent to your email"}, 200
        return {"message": "Email not registered"}, 404


@blp.route('/reset-password-form/<string:token>', methods=['GET', 'POST'])
class ResetPassword(MethodView):
    def __init__(self):
        self.user_db = StudentDatabase()

    def get(self, token):
        user = self.user_db.validate_otp(token)
        if user:
            return render_template('students/reset_password_form.html', token=token)
        else:
            return "Invalid or expired token", 400

    def post(self, token):
        data = request.get_json()
        new_password = data.get('new_password')
        hashPassword = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
        if new_password:
            self.user_db.update_password(token, hashPassword)
            return jsonify({"message": "Password has been reset successfully!"}), 200
        else:
            return jsonify({"message": "Invalid data."}), 400
