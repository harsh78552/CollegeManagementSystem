from DATABASE.STUDENT.notification import StudentNotificationDatabase
from flask_smorest import Blueprint
from flask.views import MethodView

blp = Blueprint('student notification', __name__, description='notification api')


@blp.route('/get-notification')
class GetAllNotification(MethodView):
	def __init__(self):
		self.notify_db = StudentNotificationDatabase()

	def get(self):
		response = self.notify_db.getNotification()
		return response
