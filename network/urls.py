
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # API Routes
    path("user_profile/<str:username>", views.user_profile, name="user_profile"),
    path("all_posts", views.see_all_posts, name="all_posts"),
    path('follow', views.follow, name='follow'),
    path('following_posts', views.following_posts, name="following_posts")
]
