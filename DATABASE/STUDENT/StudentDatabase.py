from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
import hashlib


class StudentDatabase:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['CollegeSystem']
        self.collection = self.db['student']

    def insert_data(self, name, contact, email, password, branch, registeration_no, year, semester, blood_group,
                    address, role='student'):
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        studentData = {'name': name, 'contact': contact, 'email': email, 'password': password, 'branch': branch,
                       'registeration_no': registeration_no, 'year': year, 'semester': semester,
                       'blood_group': blood_group, 'address': address, 'role': role}
        try:
            self.collection.insert_one(studentData)
            return {'message': 'student registered successfully', 'status': 'success'}
        except Exception as error:
            return str(error)

    def fetch_all_student(self):
        studentData = self.collection.find({}, {'name': 1, 'email': 1,'_id':0})
        studentDataList = []
        for data_ in studentData:
            studentDataList.append(data_)
        return studentDataList

    def searchStudent(self, email):
        get_data = self.collection.find_one(
            {'email': email})
        if get_data:
            get_data['_id'] = str(get_data.get('_id'))
            return get_data
        else:
            return None

    def SearchStudent(self, registrationNo):
        get_data = self.collection.find_one(
            {'registeration_no': registrationNo})
        if get_data:
            get_data['_id'] = str(get_data.get('_id'))
            return get_data
        else:
            return None

    def save_reset_token(self, email, otp):
        expiry = datetime.now(timezone.utc) + timedelta(minutes=5)
        result = self.collection.update_one({"email": email}, {'$set': {'otp': otp, "token_Expiry": expiry}})
        return result.modified_count > 0

    def validate_otp(self, otp):
        user = self.collection.find_one({"otp": otp})
        if user:
            return user
        else:
            return None

    def update_password(self, otp, password):
        result = self.collection.update_one({"otp": otp}, {"$set": {'password': password}})
        return result.modified_count > 0

    def update_profile(self, email, data):
        update_data = self.collection.update_one({'email': email},
                                                 {"$set": {"contact": data['contact'], "year": data['year'],
                                                           'semester': data['semester'], "address": data['address'],
                                                           'blood_group': data['blood_group']}})
        if update_data.modified_count > 0:
            return {'message': "data updated successfully."}, 200
        else:
            return {'message': "some error occurs."}, 500


