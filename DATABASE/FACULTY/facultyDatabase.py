from pymongo import MongoClient
import hashlib


class FacultyDatabase:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['CollegeSystem']
        self.collection = self.db['faculty']

    def insert_data(self, name, contact, email, password, role=None, subject=None, qualification=None, blood_group=None,
                    image_url=None):
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        facultyData = {'name': name, 'contact': contact, 'email': email, 'password': password, 'role': role,
                       'subject': subject, 'qualification': qualification, 'blood_group': blood_group,
                       'image': image_url}
        try:
            self.collection.insert_one(facultyData)
            return {'message': 'faculty register successfully.', 'status': 'success'}
        except Exception as error:
            return str(error)

    def getAllFaculty(self):
        response = self.collection.find()
        facultyDataList = []
        for data in response:
            if data['role'] == 'faculty':
                facultyDataDict = {'name': data['name'], 'email': data['email']}
                facultyDataList.append(facultyDataDict)
        return facultyDataList

    def searchFacultyOrAdmin(self, email):
        data = self.collection.find_one({'email': email})
        data['_id'] = str(data.get('_id'))
        if data:
            return data
        else:
            return None

    def EditProfile(self, email, data):
        subject_str = data['subject']
        subject_list = [s.strip() for s in subject_str.split(',') or ' ']
        response = self.collection.update_one({'email': email}, {
            '$set': {'contact': data['contact'], 'subject': subject_list, 'qualification': data['qualification'],
                     'blood_group': data['blood_group']}})
        if response.modified_count > 0:
            return {'message': 'profile updated successfully.'}, 200
        else:
            return {'message': 'some error occurred'}, 500


facultyData_ = FacultyDatabase()
# facultyData_.insert_data('Bhavani Sir', '8235218297', 'bhavani123@gmail.com', 'bhavani@456720-', "faculty",
#                          'python-programming',
#                          'B.tech(ECE)', 'O+')
# facultyData_.insert_data('Harsh Tiwari', '7654092577', 'ht728350@gmail.com', 'adminHarsh@82352', role='admin')
# facultyData_.getAllFaculty()
