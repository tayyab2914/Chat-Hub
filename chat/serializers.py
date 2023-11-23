from rest_framework import serializers
from .models import *

class RoomSerializer(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField()
    class Meta:
        model = Room
        fields = ['name','language','flag_url','key','admin']
    def get_admin(self, obj):
        return obj.admin.username

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['user','content']