from mongoengine import Document, UUIDField, StringField, DateTimeField
from datetime import datetime

class Messages(Document):
    id = UUIDField(primary_key=True)
    sender_id = UUIDField(required=True)
    recipient_user_id = UUIDField(required=False)
    recipient_group_id = UUIDField(required=False)
    content = StringField(required=True)
    sent_date = DateTimeField(default=datetime.utcnow)
    updated_date = DateTimeField(default=datetime.utcnow)

    def is_private(self):
        return self.recipient_user_id is not None

    def is_group(self):
        return self.recipient_group_id is not None