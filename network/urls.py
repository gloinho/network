
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:username>", views.user_view, name='user'),
    
    # API Routes
    path("user_profile/<str:username>", views.user_profile, name="user_profile"),
    path("all_posts", views.see_all_posts, name="all_posts"),
    path('follow', views.follow, name='follow'),
]
