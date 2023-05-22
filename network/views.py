from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

import json
from .models import User
from .forms import *


def index(request):
    newPostForm = NewPostForm()
    allPosts = Post.objects.all().order_by("-postTime")
    paginator = Paginator(allPosts, 10)  # show 10 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        posts_liked_by_user = (
            LikedPost.objects.all().filter(liker=request.user)
            .values_list("post", flat=True))
    else:
        posts_liked_by_user = None

    if request.method == "POST":
        data = request.POST
        newPost = Post(
            postTitle=data["postTitle"],
            postBody=data["postBody"],
            postAuthor=request.user,
        )
        newPost.save()
        return HttpResponseRedirect(reverse("index"))
    return render(
        request,
        "network/index.html",
        {"form": newPostForm, "page_obj": page_obj, "likedList": posts_liked_by_user},
    )


@csrf_exempt
def edit_post(request, id):

    post_to_update = Post.objects.get(id=id)
    if request.method == "PUT":
        if request.user == post_to_update.postAuthor:
            stuff = json.loads(request.body)
            if stuff.get("post"):
                post_to_update.postBody = stuff["post"]
            post_to_update.save()
            return HttpResponse(status=204)
    return HttpResponse(status=400)


@csrf_exempt
def profile(request, username):
    user_id = User.objects.get(username=username)
    p = Profile.objects.all().filter(profilename=user_id)
    q = Profile.objects.all().filter(following=user_id)

    if request.user.is_authenticated:
        posts_liked_by_user = (
            LikedPost.objects.all()
            .filter(liker=request.user)
            .values_list("post", flat=True))
    else:
        posts_liked_by_user = None

    # allow follow/unfollow if user is logged in
    isFollower = False
    if request.user.is_authenticated:
        isFollower = Profile.objects.filter(
            profilename=request.user, following=user_id).exists()

        # for a POST method, add the logged in as a follower
        if request.method == "POST":
            stuff = json.loads(request.body)
            if stuff.get("user"):
                if not isFollower:
                    newFollower = Profile(profilename=request.user, following=user_id)
                    newFollower.save()
                    return HttpResponse(status=204)
                else:
                    Profile.objects.get(
                        profilename=request.user, following=user_id).delete()
                    return HttpResponse(status=204)

    authorPosts = Post.objects.all().filter(postAuthor=user_id).order_by("-postTime")
    return render(
        request,
        "network/profile.html",
        {
            "current_user": request.user.username,
            "name": username,
            "authorPosts": authorPosts,
            "show_button": (request.user.username != username)
            and (request.user.is_authenticated),
            "button_text": ["Follow", "Unfollow"][isFollower],
            "follows": p,
            "following": q,
            "likedList": posts_liked_by_user,
            "num_followers": len(p),
            "num_following": len(q),
        },
    )


@login_required
def following(request):
    # Allow logged in user to see all posts of people he follows
    followed_users = Profile.objects.filter(profilename=request.user)
    followed_posts = Post.objects.filter(
        postAuthor__in=followed_users.values("following_id")
    ).order_by("-postTime")
    posts_liked_by_user = (
        LikedPost.objects.all()
        .filter(liker=request.user)
        .values_list("post", flat=True)
    )
    return render(
        request,
        "network/following.html",
        {
            "followed_users": followed_users,
            "followed_posts": followed_posts,
            "likedList": posts_liked_by_user,
        },
    )

@csrf_exempt
def like(request, id):
    post = Post.objects.get(id=id)
    # determine whether or not the logged in user likes the post
    liked_state = LikedPost.objects.filter(post=post, liker=request.user).exists()

    if request.method == "GET":
        data = dict(post.serialize())
        data["btnState"] = liked_state
        return JsonResponse(data)

    if request.method == "PUT":
        if not liked_state:
            newLikedPost = LikedPost(post=post, liker=request.user)
            post.likes += 1            
            newLikedPost.save()          
        else:
            LikedPost.objects.get(post=post, liker=request.user).delete()
            post.likes -= 1
        post.save()
        data = dict(post.serialize())
        data["btnState"] = liked_state
        return JsonResponse(data)

    return HttpResponse(status=204)


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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")