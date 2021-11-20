from django.urls import path
from .views import PostListView, PostDetailView, CommentDeleteView, ProfileView, AddFollower, RemoveFollower, AddLike, \
    ListFollowers

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name='add-follower'),
    path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name='remove-follower'),
    path('post/<int:pk>/like', AddLike.as_view(), name='like'),
    path('followers/<int:pk>', ListFollowers.as_view(), name='list-followers'),
]