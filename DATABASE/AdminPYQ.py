from pymongo import MongoClient


class AdminQuestionPaperUploadDatabase:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['CollegeSystem']
        self.collection = self.db['previous-year-question']

    def insertPYQ(self, semester, year, paperType, subject, paper_urls):
        existing_doc = self.collection.find_one({"semester": semester, "year": year})
        if not existing_doc:
            self.collection.insert_one({
                "semester": semester,
                "year": year,
                "papers": [{
                    "paperType": paperType,
                    "subjects": [{
                        "subject": subject,
                        "url": paper_urls
                    }]
                }]
            })
            return {"message": 'paper upload successfully.'}, 200

        else:
            try:
                for paper in existing_doc['papers']:
                    if paper['paperType'] == paperType:
                        response = self.collection.update_one(
                            {
                                "_id": existing_doc["_id"],
                                "papers.paperType": paperType
                            },
                            {
                                "$push": {
                                    "papers.$.subjects": {
                                        "subject": subject,
                                        "url": paper_urls
                                    }
                                }
                            }
                        )
                        if response.modified_count > 0:
                            return {"message": 'paper add successfully.'}, 200
            except Exception as error:
                return {'message': f'{error}'}, 403
            try:

                response_ = self.collection.update_one(
                    {"_id": existing_doc["_id"]},
                    {
                        "$push": {
                            "papers": {
                                "paperType": paperType,
                                "subjects": [{
                                    "subject": subject,
                                    "url": paper_urls
                                }]
                            }
                        }
                    }
                )
                if response_.modified_count > 0:
                    return {"message": 'new paper type added successfully.'}, 200
            except Exception as error_:
                return {'message': f'{error_}'}, 403

    def getPyq(self, semester, paperType):
        PYQdata = self.collection.find_one({'semester': str(semester)})
        if PYQdata:
            for paper in PYQdata.get('papers'):
                if paper.get('paperType') == paperType:
                    return paper['subjects']
            return {"message": "Paper type not found for this semester."}, 404
        else:
            return {"message": "Semester not found."}, 404

