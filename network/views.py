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
    if request.method == 'POST':
        # Creates a new post.
        data = json.loads(request.body)
        content = data.get('content')
        posted_by = User.objects.get(id=int(data.get('posted_by')))
        new_post = Post(
            posted_by= posted_by,
            content = content,   
        )
        new_post.save()
    return render(request, "network/index.html",{
            'newPost': newPost
        })


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

@login_required
def see_all_posts(request):
    all_posts = Post.objects.order_by("-posted_at").all()
    return JsonResponse([post.serialize() for post in all_posts], safe=False)

@login_required
@csrf_exempt
def home(request):
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
        new_post = Post(
            posted_by= posted_by,
            content = content,   
        )
        new_post.save()
    return render(request, 'network/home.html',{
        'newPost': newPost
    })

class newPost(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['content']    
        labels = {'content':''}
        widgets = {'content': forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':"What's poppin?!",
            'id':'post_content'
        })}

def user_profile(request, username):
    user = User.objects.get(username=username)
    try:
        connections = user.connections.following.all()
        following = [following.username for following in connections]
        followers = [follower.username for follower in connections]
    except ObjectDoesNotExist:
        following = 'undefined'
        followers = 'undefined'
    try:
        posts = [post.id for post in user.posts.all()]
        
    except ObjectDoesNotExist:
        posts = 'undefined'
        
    return JsonResponse([{'posts': posts, 'following':following,'followers':followers }], safe=False)


#TODO
def see_user_posts(request):
    pass