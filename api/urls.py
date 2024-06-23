from django.urls import path
from .views import UserLoginView, UserSignupView, \
    UserSearchView, FriendRequestView, \
    AcceptRejectFriendRequestView, FriendListView, \
    PendingFriendRequestsView

app_name = 'api'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('friend-request/<int:pk>/', AcceptRejectFriendRequestView.as_view(), name='accept-reject-friend-request'),
    path('friends/', FriendListView.as_view(), name='friend-list'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending-friend-requests'),
]