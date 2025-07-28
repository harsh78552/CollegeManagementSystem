from pymongo import MongoClient


class StudentAttendance:
	def __init__(self):
		self.client = MongoClient('mongodb://localhost:27017/')
		self.db = self.client['CollegeSystem']
		self.collection = self.db['studentAttendance']

	def insertStudentAttendance(self, data):
		try:
			student_name = data['name']
			email = data['email']
			date = data['date']
			day = data['day']
			subject = data['subject']
			status = data['status']
			student = self.collection.find_one({'name': student_name})
			if not student:
				new_attendance = {
					'name': student_name,
					'email': email,
					'attendanceData': [{
						'date': date,
						'day': day,
						'subjects': [{'subject': subject, 'status': status}]
					}]
				}
				self.collection.insert_one(new_attendance)
				return {'message': 'Attendance added for new student'}
			attendanceData = student.get('attendanceData', [])
			updated = False
			for entry in attendanceData:
				if entry['date'] == date:
					for subj in entry['subjects']:
						if subj['subject'] == subject:
							return {'message': 'Attendance already marked for this subject on this date'}
					entry['subjects'].append({'subject': subject, 'status': status})
					updated = True
					break
			if not updated:
				attendanceData.append({
					'date': date,
					'day': day,
					'subjects': [{'subject': subject, 'status': status}]
				})
			self.collection.update_one(
				{'name': student_name},
				{'$set': {'attendanceData': attendanceData}}
			)
			return {'message': 'Attendance marked successfully.'}
		except Exception as error:
			return str(error)

	def getAttendance(self, email, subject, date):
		result = self.collection.find_one({
			"email": email,
			"attendanceData": {
				"$elemMatch": {
					"date": date,
					"subjects": {
						"$elemMatch": {
							"subject": subject
						}
					}
				}
			}
		})

		if result:
			for day in result['attendanceData']:
				for sub in day['subjects']:
					if sub['subject'] == subject:
						return {
							"date": date,
							"subject": subject,
							"status": sub['status'],
							"day": day['day']
						}
		else:
			return {"message": f"Attendance not marked on this date. "}
