from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Connections
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":
        print(request.POST)
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
def all_posts_view(request):
    # Set up Pagination to put in the html context.
    
    p = Paginator(Post.objects.order_by("-posted_at").all(), 10)
    page = request.GET.get('page')
    posts = p.get_page(page)
    return render(request, 'network/allposts.html', {'pagination':posts})


@login_required
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
            })
        elif user not in post.liked_by.all():
            post.liked_by.add(user)
            return JsonResponse({
                'post':data.get('post'),
            })
            
    if request.method == 'POST':
        
        # Creates a new post.
        data = json.loads(request.body)
        content = data.get('content')
        posted_by = User.objects.get(username=data.get('posted_by'))
        Post.objects.create(posted_by=posted_by, content=content)
        
    # Set up Pagination.
    p = Paginator(Post.objects.order_by("-posted_at").all(), 10)
    page = request.GET.get('page')
    posts = p.get_page(page)
    return JsonResponse([post.serialize() for post in posts], safe=False)


@login_required
def user_profile(request, username):
    user = User.objects.get(username=username)
    
    # See user connections.
    connections = user.connections
    following = [following.username for following in connections.following.all()]
    followers = [follower.username for follower in connections.followers.all()]
 
    # Set up Pagination to see USER POSTS.
    p = Paginator(Post.objects.order_by("-posted_at").filter(posted_by=user), 10)
    page = request.GET.get('page')
    posts = p.get_page(page)
    
    return JsonResponse({'posts': [post.serialize() for post in posts], 'following':following,'followers':followers }, safe=False)


@login_required
def user_page(request, username):
    user = User.objects.get(username=username)
    
    # Set up Pagination to put in the html context.
    p = Paginator(Post.objects.order_by("-posted_at").filter(posted_by=user), 10)
    page = request.GET.get('page')
    posts = p.get_page(page)
    
    return render(request, 'network/user.html', {'username':username, 'pagination':posts})
 
 
@login_required
def following_posts_view(request):
    user = User.objects.get(username=request.user)
    
    # Get all followed users.
    following = user.connections.following.all()
    
    # Get all posts for each followed user.
    queryset_array = [User.objects.get(username=u).posts.order_by("-posted_at").all() for u in following]
    
    # Populate the list with all posts.
    posts = []
    for queryset in queryset_array:
        for post in queryset:
            posts.append(post)
            
    # Set up Pagination to put in the html context.
    p = Paginator(posts, 10)
    page = request.GET.get('page')
    followingposts = p.get_page(page)
    return render(request, 'network/following.html', {'pagination':followingposts})


@login_required
def see_following_posts (request):
    user = User.objects.get(username=request.user)
    
    # Get all followed users.
    following = user.connections.following.all()
    
    # Get all posts for each followed user.
    queryset_array = [User.objects.get(username=u).posts.order_by("-posted_at").all() for u in following]
    
    # Populate the list with all posts.
    posts = []
    for queryset in queryset_array:
        for post in queryset:
            posts.append(post)
            
    # Set up Pagination to see USER FOLLOWED POSTS
    p = Paginator(posts, 10)
    page = request.GET.get('page')
    followingposts = p.get_page(page)
    
    return JsonResponse({'posts':[post.serialize() for post in followingposts]})
 
    
@login_required   
@csrf_exempt
def follow(request):
    data = json.loads(request.body)
    user = User.objects.get(username=request.user)
    target = User.objects.get(username=data.get('target'))
    
    # User cannot be the target of the follow action.
    if user!=target:
        
        if target in user.connections.following.all():
            # Remove user from target's followers and remove target from user's following 
            
            user.connections.following.remove(target)
            target.connections.followers.remove(user)
            return JsonResponse({'message':f'Unfollowed {target} :('}, safe=False)
        else:
            # Add user from target's followers and add target from user's following 
            
            user.connections.following.add(target)
            target.connections.followers.add(user)
            return JsonResponse({'message':f'Now following {target} :)'}, safe=False)
    else:
        return(JsonResponse({"error":"You can't follow yourself."}, safe=False))

    
@login_required
@csrf_exempt
def edit_post(request):
    data = json.loads(request.body)
    post = Post.objects.get(id=int(data.get('post')))
    
    # Update the posts content and then save it to database
    newcontent = data.get('content')
    post.content = newcontent
    post.save()
    
    return JsonResponse({'post': [post.serialize()], 'newcontent':newcontent})