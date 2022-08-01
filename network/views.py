from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models.base import ObjectDoesNotExist

from .models import User, Post, Connections


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user and empty connections
        try:
            user = User.objects.create_user(username, email, password)
            newconnection = Connections.objects.create(user=user)
            user.save()
            
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
def see_all_posts(request):
    if request.method == 'PUT':
        # Insert the user in the post's liked_by array.
        data = json.loads(request.body)
        post = Post.objects.get(id=int(data.get('post')))
        user = User.objects.get(username=data.get('user'))
        if user in post.liked_by.all():
            post.liked_by.remove(user)
            return JsonResponse({
                'post':data.get('post'),
                'liked':'Disliked',
            })
        elif user not in post.liked_by.all():
            post.liked_by.add(user)
            return JsonResponse({
                'post':data.get('post'),
                'liked':'Liked',
            })
            
    if request.method == 'POST':
        # Creates a new post.
        data = json.loads(request.body)
        content = data.get('content')
        posted_by = User.objects.get(username=data.get('posted_by'))
        Post.objects.create(posted_by=posted_by, content=content)
        
    all_posts = Post.objects.order_by("-posted_at").all()
    return JsonResponse([post.serialize() for post in all_posts], safe=False)

def user_profile(request, username):
    user = User.objects.get(username=username)
    connections = user.connections
    following = [following.username for following in connections.following.all()]
    followers = [follower.username for follower in connections.followers.all()]
    userpost = Post.objects.order_by("-posted_at").filter(posted_by=user)
    
    return JsonResponse({'posts': [post.serialize() for post in userpost], 'following':following,'followers':followers }, safe=False)


@csrf_exempt   
def follow(request):
    data = json.loads(request.body)
    user = User.objects.get(username=request.user)
    target = User.objects.get(username=data.get('target'))
    if user!=target:
        if target in user.connections.following.all():
            user.connections.following.remove(target)
            target.connections.followers.remove(user)
        else:
            user.connections.following.add(target)
            target.connections.followers.add(user)
    else:
        return(JsonResponse({"error":"You can't follow yourself."}, safe=False))

    following = [u.username for u in user.connections.following.all()]
    print(following)
    return JsonResponse({'following':following}, safe=False)
      
def following_posts (request):
    user = User.objects.get(username=request.user)
    following = user.connections.following.all()
    posts = [User.objects.get(username=u).posts.all() for u in following]

    return JsonResponse({'following':[users.username for users in following]})
    