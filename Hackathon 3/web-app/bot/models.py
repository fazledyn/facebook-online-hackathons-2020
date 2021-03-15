"""
Basic Quick Reply Structure for easily sending payload based data
"""

from enum import Enum


class NotificationType(Enum):
    regular = "REGULAR"
    silent_push = "SILENT_PUSH"
    no_push = "NO_PUSH"


class QuickReply():
    reply_dict = []

    """
    Content type for different types of quick reply-
        - text: "text"
        - phone number: "user_phone_number"
        - email: "user_email"
    """
    def add_text_reply(self, content_type, title, payload):
        item = {}
        item['content_type'] = content_type
        item['title'] = title
        item['payload'] = payload

        self.reply_dict.append(item)

    def add_phone_number_reply(self, payload):
        self.add_text_reply(content_type="user_phone_number", title="Phone", payload=payload)

    def add_email_reply(self, payload):
        self.add_text_reply(content_type="user_email", title="Email", payload=payload)
    
    def as_dict(self):
        return self.reply_dict