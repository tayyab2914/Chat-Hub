import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from core.models import UserProfile
from .models import Room, Message

class ChatConsumer(WebsocketConsumer):
    online_users = set()

    def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['key']
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # Add user to the list of online users
        self.online_users.add(self.scope["user"])

        # Update online users for the room
        self.update_online_users()

        self.accept()
    
    def disconnect(self, close_code):
        # Remove user from the list of online users
        self.online_users.remove(self.scope["user"])

        # Update online users for the room
        self.update_online_users()

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"]

        room = Room.objects.get(key=self.room_name)
        Message.objects.create(room=room, user=user, content=message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'user': user,
            }
        )

    def chat_message(self, event):
        message = event['message']
        user = event['user']

        user_profile = UserProfile.objects.get(user=user)

        self.send(text_data=json.dumps({
            'type': 'message',
            'message': message,
            'user': user.username,
            'profile_pic':user_profile.profile_picture.url
        }))

    def update_online_users(self):
        # Send the updated online user list to all clients in the room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat.online_users',
                'online_users': list(self.online_users),
            }
        )

    def chat_online_users(self, event):
        # Send the updated online user list to the client
        online_users = event['online_users']
        online_users_data={'users':[], "profile_pictures":[]}
        for user in online_users:
            online_users_data['users'].append(user.username)
            user_profile = UserProfile.objects.get(user=user)
            online_users_data['profile_pictures'].append(user_profile.profile_picture.url)
        online_users_data['type'] = 'online_users'
        
        # self.send(text_data=online_users_data)
        self.send(text_data=json.dumps(

            online_users_data,
        ))