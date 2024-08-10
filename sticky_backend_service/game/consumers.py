import json

from channels.generic.websocket import WebsocketConsumer


class PingConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        self.send(text_data=json.dumps({"message": "pong"}))
