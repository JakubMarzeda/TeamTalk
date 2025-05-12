from mongoengine import Document, UUIDField, StringField, DateTimeField, ReferenceField, NULLIFY
import datetime

class Messages(Document):
    id = UUIDField(primary_key=True)
    sender = ReferenceField("User", required=True, reverse_delete_rule=NULLIFY)
    recipient_user = ReferenceField("User", required=False, reverse_delete_rule=NULLIFY)
    recipient_group = ReferenceField("Group", required=False, reverse_delete_rule=NULLIFY)
    content = StringField(required=True)
    sent_date = DateTimeField(default=datetime.datetime.utcnow)
    updated_date = DateTimeField(default=datetime.datetime.utcnow)

    def is_private(self):
        return self.recipient_user is not None

    def is_group(self):
        return self.recipient_group is not None