from mongoengine import Document, UUIDField, StringField, ListField, ReferenceField, DateTimeField
from datetime import datetime

class Groups(Document):
    id = UUIDField(primary_key=True, unique=True)
    name = StringField(max_length=50, required=True)
    members = ListField(UUIDField())
    created_date = DateTimeField(default=datetime.utcnow)
    updated_date = DateTimeField(default=datetime.utcnow)

