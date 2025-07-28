from pymongo import MongoClient


class AdminMarksUploadDatabase:
	def __init__(self):
		self.client = MongoClient('mongodb://localhost:27017/')
		self.db = self.client['CollegeSystem']
		self.collection = self.db['StudentMarksheet']

	def insertMarksData(self, name, roll, semester, batch, branch, subjects):
		existing_student = self.collection.find_one({"roll": roll})

		if existing_student:

			semesters = existing_student.get('data', [])
			semester_exists = any(sem.get('semester') == semester for sem in semesters)

			if semester_exists:
				return {"message": "Semester already exists for this student."}

			self.collection.update_one(
				{"roll": roll},
				{
					"$push": {
						"data": {
							"subjects": subjects
						}
					},
					"$set": {
						"name": name,
						"batch": batch,
						"branch": branch,
						"semester": semester
					}
				}
			)
			return {"message": "New semester added for existing student."}

		else:
			student_data = {
				"name": name,
				"roll": roll,
				"batch": batch,
				"branch": branch,
				"semester": semester,
				"data": [{
					"subjects": subjects
				}]
			}
			self.collection.insert_one(student_data)
			return {"message": "Marks uploaded successfully for new student."}

	def fetchResultData(self, roll, semester):
		print(roll, semester)
		result = self.collection.find_one({'roll': roll})
		if result:
			for data_ in result['data']:
				if result['semester'] == semester:
					data_['semester'] = semester
					data_['name'] = result['name']
					data_['roll'] = roll
					data_['batch'] = result['batch']
					data_['branch'] = result['branch']
					return data_
		else:
			return {"message": 'result not found.'},404
