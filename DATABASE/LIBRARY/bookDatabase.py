from pymongo import MongoClient


class BookDatabase:
	def __init__(self):
		self.client = MongoClient('mongodb://localhost:27017/')
		self.db = self.client['CollegeSystem']
		self.collection = self.db['books']

	def insertBook(self, name, author, publisher, published_year, edition, genre, total_copies, available_copies,
	               description, location=None):
		bookDict = {'name': name, 'author': author, 'publisher': publisher, 'published_year': published_year,
		            'edition': edition, 'genre': genre, 'total_copy': total_copies,
		            'available_copies': available_copies, 'description': description, 'location': location}
		try:
			genre_doc = self.collection.find_one({'genre': genre})
			if genre_doc:
				self.collection.update_one({"genre": genre}, {"$push": {"books": bookDict}})
			else:
				self.collection.insert_one({'genre': genre, 'books': [bookDict]})
			return {'message': 'book added successfully.', 'status': 'success'}, 200
		except Exception as error:
			return {'message': str(error), 'status': 'fail'}, 403

	def getAllBook(self):
		books = self.collection.find()
		booksList = []
		for book in books:
			booksList.append(book.get('books')[0])
		return booksList, 200

	def getGenre(self):
		books = self.collection.find()
		genreList = []
		for genre in books:
			genreList.append(genre.get('genre'))
		return genreList

	def getGenreBook(self, genre):
		bookData = self.collection.find_one({'genre': genre})
		bookData['_id'] = str(bookData['_id'])
		return bookData, 200

	def getBook(self, genre, bookName):
		bookData = self.collection.find_one({'genre': genre})
		for book in bookData['books']:
			if book['name'] == bookName:
				return book

	def updateBook(self, bookData):
		try:
			response = self.collection.update_one({'genre': bookData['genre'], 'books.name': bookData['name']}, {
				"$set": {'books.$.author': bookData['author'], 'books.$.publisher': bookData['publisher'],
				         'books.$.published_year': bookData['published_year'], 'books.$.edition': bookData['edition'],
				         'books.$.total_copy': bookData['total_copy'],
				         'books.$.available_copies': bookData['available_copies'],
				         'books.$.description': bookData['description'], 'books.$.location': bookData['location']}})
			if response.modified_count > 0:
				return {"message": "book data updated successfully."}, 200
			else:
				return {"message": "some unknown error occurred"}, 500
		except Exception as error:
			return {'error': str(error)}, 503
