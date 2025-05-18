from mongoengine import Document, StringField, EmailField, UUIDField, DateTimeField, ListField, ReferenceField
from datetime import datetime

class Users(Document):
    id = UUIDField(primary_key=True, unique=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    email = EmailField(max_length=50, required=True)
    password = StringField(required=True)
    register_date = DateTimeField(default=datetime.utcnow)
    updated_date = StringField(default=datetime.utcnow)
