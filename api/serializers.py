from rest_framework import serializers
from .models import User, FriendRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password']

class FriendRequestPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'receiver', 'status', 'timestamp']


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'timestamp']

class FriendRequestAcceptRejectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['status']