from app import ma
from serializers.base import BaseSchema
from serializers.genre import GenreSchema
from serializers.user import UserSchema
from serializers.comment import CommentSchema
from serializers.like import LikeSchema
from marshmallow import fields
from models.book import Book
from models.user import User
from models.like import Like

class PopulateBookSchema(ma.SQLAlchemyAutoSchema, BaseSchema):

  class Meta:
    model = Book
    load_instance = True

    load_only = ('user_id',)

  user_id = fields.Integer()
  


  comments = fields.Nested('CommentSchema', many=True)
  genres = fields.Nested('GenreSchema', many = True)
  likes = fields.Nested('LikeSchema', many = True)
  user = fields.Nested('UserSchema', only =('id', 'username'))

