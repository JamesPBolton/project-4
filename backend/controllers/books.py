from flask import Blueprint, request
from models.book import Book
from models.comment import Comment
from models.age import Age
from models.genre import Genre
from serializers.book import BookSchema
from serializers.comment import CommentSchema
from serializers.age import AgeSchema
# from serializers.genre import GenreSchema 
from middleware.secure_route import secure_route
from serializers.genre import GenreSchema 
from marshmallow import ValidationError



book_schema = BookSchema()
comment_schema = CommentSchema()
genre_schema = GenreSchema()
age_schema = AgeSchema()
router = Blueprint(__name__, 'books')


# ! ROUTES FOR AGE

# GET ALL AGES
@router.route('/ages', methods=['GET'])
def all_age():
  ages = Age.query.all()

  return age_schema.jsonify(ages, many=True), 200

# GET a single age
@router.route('/ages/<int:id>', methods=['GET'])
def get_single_age(id):
  
  age = Age.query.get(id) 

  if not age:
    return { 'message': 'Age not found!' }, 404

  return age_schema.jsonify(age), 200

  # CREATE a Age 
@router.route('/ages', methods=['POST'])
def create_age():
  age_dictionary = request.get_json()

  try: 
    age = age_schema.load(age_dictionary)
  
  except ValidationError as e:
    return { 'errors': e.messages, 'message': 'Something went wrong!'}
  
  age.save()

  return age_schema.jsonify(age), 200


# DELETE a age
@router.route('/ages/<int:id>', methods=['DELETE'])
def remove_age(id):

  age = Age.query.get(id)

  if not age:
    return { 'message': 'Age not found!' }, 404

  age.remove()

  return { 'message': f'Age {id} ---deleted successfully '}, 200


# ! ROUTES FOR BOOKS

# GET all books
@router.route('/books', methods=['GET'])
def index():
  books = Book.query.all()

  return book_schema.jsonify(books, many=True), 200

# GET a single book
@router.route('/books/<int:id>', methods=['GET'])
def get_single_book(id):
  
  book = Book.query.get(id) 

  if not book:
    return { 'message': 'Book not found!' }, 404

  return book_schema.jsonify(book), 200

# CREATE a book
@router.route('/books', methods=['POST'])
def create():
  book_dictionary = request.get_json()

  try: 
    book = book_schema.load(book_dictionary)
  
  except ValidationError as e:
    return { 'errors': e.messages, 'message': 'Something went wrong!'}
  
  book.save()

  return book_schema.jsonify(book), 200


# UPDATE a book
@router.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
  existing_book = Book.query.get(id)
  if not existing_book:
    return { 'message': 'Book not found!!'}, 404

  # ? Deserialization step
  try: 
    book = book_schema.load(
      request.get_json(),
      instance= existing_book,
      partial=True
    )
  
  except ValidationError as e:
    return { 'errors': e.messages, 'message': 'Something went wrong!'}

  book.save()


  # ? Serialization step
  return book_schema.jsonify(book), 200


# DELETE a book
@router.route('/books/<int:id>', methods=['DELETE'])
def remove(id):

  book = Book.query.get(id)

  if not book:
    return { 'message': 'Book not found!' }, 404

  book.remove()

  return { 'message': f'Book {id} ---deleted successfully '}, 200


# ! ROUTES FOR COMMENTS

# Create a new comment - Not Working!
@router.route('/books/<int:book_id>/comments', methods=['POST'])
def comment_create(book_id):
  comment_data = request.get_json()
  book = Book.query.get(book_id)
  

  # ? Deserialization step
  try: 
    comment = comment_schema.load(comment_data)
  
 
  except ValidationError as e:
    return { 'errors': e.messages, 'message': 'Something went wrong!' }

  comment.book = book
  comment.save()

   # ? Serialization step
  return comment_schema.jsonify(comment)


# !  ROUTES FOR GENRES

# GET all genres

# @router.route('/genres', methods=['GET'])
# def get_genres():

#   all_genres = Genre.query.all()

#   return genre_schema.jsonify(all_genres, many=True), 200