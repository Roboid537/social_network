
from datetime import timedelta
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.db.models import Q
from django.utils import timezone
from .models import User, FriendRequest
from .serializers import UserSerializer, UserSignUpSerializer, \
      FriendRequestSerializer, FriendRequestPostSerializer, \
      FriendRequestAcceptRejectSerializer

class UserLoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):

        email = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=email.lower().strip(), password=password)

        if user is not None:
            # Authentication successful
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({'non_field_errors': ['Unable to log in with provided credentials.']},
                            status=status.HTTP_400_BAD_REQUEST)

class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        request.data['email'] = request.data['email'].lower().strip()
        request.data['password'] = make_password(request.data.get('password'))
        return super().post(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserSignUpSerializer
        return super().get_serializer_class()

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        search_keyword = self.request.query_params.get('q', '')
        queryset = User.objects.filter(
            Q(email__iexact=search_keyword) |
            Q(name__icontains=search_keyword)
        ).exclude(id=self.request.user.id)
        return queryset

class FriendRequestView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        sender = self.request.user
        receiver_id = self.request.data.get('receiver')
        receiver = User.objects.get(id=receiver_id)

        # Check if the sender has already sent 3 requests within a minute
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests_count = FriendRequest.objects.filter(
            sender=sender,
            timestamp__gte=one_minute_ago
        ).count()
        if recent_requests_count >= 3:
            raise serializers.ValidationError(
                'Cannot send more than 3 friend requests within a minute.')

        serializer.save(sender=sender, receiver=receiver)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FriendRequestPostSerializer
        return super().get_serializer_class()

class AcceptRejectFriendRequestView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.receiver != self.request.user:
            raise serializers.ValidationError(
                'You are not authorized to accept or reject this friend request.')
        serializer.save()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return FriendRequestAcceptRejectSerializer
        return super().get_serializer_class()

class FriendListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friend_ids = FriendRequest.objects.filter(
            Q(sender=user) | Q(receiver=user),
            status='accepted'
        ).values_list('sender_id', 'receiver_id')
        friend_ids = [ids for sublist in friend_ids for ids in sublist if ids != user.id]
        return User.objects.filter(id__in=friend_ids)

class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(receiver=user, status='pending')
