# routing.py
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from coquus.consumer import MyConsumer


# class MyConsumer:
#     async def connect(self):
#         # Your connection handling logic here
#         pass

#     async def disconnect(self, close_code):
#         # Your disconnection handling logic here
#         pass

#     async def receive(self, text_data):
#         # Your message receiving logic here
#         # You can use the 'send_notification' function defined above to send messages back
#         await self.send(text_data=text_data)


application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/mywebsocket/", MyConsumer.as_asgi()),
    ]),
})
