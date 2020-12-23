from flask_restful import Resource, reqparse
from models.chat import ChatModel
from flask_jwt_extended import (
    jwt_required,
    fresh_jwt_required,
    jwt_optional
)

"""
The following resources contain endpoints that are protected by jwt,
one may need a valid access token, a valid fresh token or a valid token with authorized privilege 
to access each endpoint, details can be found in the README.md doc.  
"""

_chat_parser = reqparse.RequestParser()
_chat_parser.add_argument('json_data',
                          type=str,
                          required=True,
                          help="Every chat needs a chat message."
                          )


class Chat(Resource):
    @jwt_required
    def post(self, chat_id: int):
        data = _chat_parser.parse_args()
        chat = ChatModel(data['json_data'])
        chat.save_to_db()

        return {"message": "Chat created successfully."}, 201

    @jwt_required
    def get(self, chat_id: int):
        if chat_id == 0:
            chats = [chat.json() for chat in ChatModel.find_all()]
            return {'chats': chats}, 200
        else:
            chat = ChatModel.find_by_id(chat_id)
            if chat:
                return chat.json()
        return {'message': 'Chat not found'}, 404

    @jwt_required
    def delete(self, chat_id):
        chat = ChatModel.find_by_id(chat_id)
        if chat:
            chat.delete_from_db()
            return {'message': 'Chat deleted.'}
        return {'message': 'Chat not found.'}, 404

    def put(self, chat_id):
        data = _chat_parser.parse_args()

        chat = ChatModel.find_by_id(chat_id)

        if chat:
            chat.json_data = data['json_data']
        else:
            chat = ChatModel(chat_id, **data)

        chat.save_to_db()
        return chat.json()


#class ChatList(Resource):
#    @jwt_optional
#    def get(self):
#        chats = [chat.json() for chat in ChatModel.find_all()]
#        return {'chats': chats}, 200

