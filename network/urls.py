
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:username>", views.user_page, name="userpage"),
    path('allposts', views.all_posts_view, name="allposts"),
    path('following', views.following_posts_view, name="following"),
    
    # API Routes
    path("user_profile/<str:username>", views.user_profile, name="user_profile"),
    path('follow', views.follow, name='follow'),
    path("see_all_posts", views.see_all_posts, name="see_all_posts"),
    path('see_following_posts', views.see_following_posts, name="see_following_posts"),
]
