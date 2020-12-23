from db import db


class ChatModel(db.Model):
    __tablename__ = 'chats'

    chat_id = db.Column(db.Integer, primary_key=True)
    json_data = db.Column(db.Text)

    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        return {
            'chat_id': self.chat_id,
            'json_data': self.json_data
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(chat_id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
