from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError 
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from datetime import datetime
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json



from .models import User, Post, Follow

class NewPost(forms.Form):
    post = forms.CharField(label="", widget=forms.Textarea(attrs={"rows": 3, "cols": 45}))
    _ = forms.CharField(widget=forms.widgets.Input(attrs={"type": "submit", "value": "Post"}))
    image = forms.ImageField(label="", required=False, widget=forms.widgets.ClearableFileInput(attrs={"class": "attach-image"}))

class NewFollow(forms.Form):
    follow = forms.CharField(label="", widget=forms.widgets.Input(attrs={"type": "submit", "value": "Follow"}))
    
class NewUnfollow(forms.Form):
    unfollow = forms.CharField(label="", widget=forms.widgets.Input(attrs={"type": "submit", "value": "Unfollow"}))
    
class NewEdit(forms.Form):
    # take the existing post and edit it 
    post = forms.CharField(label="", widget=forms.Textarea(attrs={"rows": 3, "cols": 45}))
    _ = forms.CharField(widget=forms.widgets.Input(attrs={"type": "submit", "value": "Edit"}))
    pass


def index(request):       
    # POST request (user fills out form)
    if request.method == "POST":  
        # allow only the users who are logged in to make new posts.
        if request.user.is_authenticated:      
            form = NewPost(request.POST, request.FILES)   

            if form.is_valid():
                post_content = form.cleaned_data["post"]
                user_id = request.user
                post_time = datetime.now()
                image = request.FILES.get("image")

                post = Post(
                    post_content=post_content,
                    user_id = user_id,
                    post_time = post_time,
                    )
                
                # adding an image to a post is optional
                if image:
                    post.image = image

                post.save()  
                # most recent post shows first
                posts = Post.objects.order_by('-post_time')

                # empty the form after succesful post
                form = NewPost()

        # when a user who is not logged in attempts to make a post, redirect to login screen
        else:    
            return redirect('login')

               
    # GET request (user loads the initial page)
    else:
        form = NewPost()        
        posts = Post.objects.order_by('-post_time')  

        if not posts:
            page_obj = None
    
    paginator = Paginator(posts, 10)  

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
          
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "form": form                         
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

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    

def profile_page(request, user_id):
    # only allow for profile pages of user that exist.
    try:
        user = User.objects.get(username=user_id) 
    except User.DoesNotExist:
        return render(request, "network/pagenotfound.html")

    # set the 'already_following' variable to false initially. 
    already_following = False
    if request.user.is_authenticated:
        user_profile = User.objects.get(username=user) 
        # if .exists() is true, set the already_following variable to true. 
        already_following = Follow.objects.filter(user_id=user_profile, follower=request.user).exists()
    
        follower_count = Follow.objects.filter(followed=user).count()
        following_count = Follow.objects.filter(follower=user_profile).count() 
        # all of the user's posts in reverse chronological order
        posts = Post.objects.filter(user_id=user).order_by("-post_time")

        # paginate 10 posts per page
        paginator = Paginator(posts, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    # if a logged out user checks someone's profile, load that page but without following functionality
    else:
        user_profile = User.objects.get(username=user) 
        follower_count = Follow.objects.filter(followed=user).count() 
        following_count = Follow.objects.filter(follower=user_profile).count()   
        posts = Post.objects.filter(user_id=user).order_by("-post_time")
        
        paginator = Paginator(posts, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/profile.html", {
            "user": request.user,
            "user_profile": user_profile,            
            "follower_count": follower_count,
            "following_count": following_count,
            "page_obj": page_obj
        })


    # instantiate 2 forms for either follow / unfollow
    follow_form = NewFollow()
    unfollow_form = NewUnfollow()

    if request.method == "POST":

        follow_form = NewFollow(request.POST)

        unfollow_form = NewUnfollow(request.POST)        

        # when follow button is clicked, create new object and save it to db
        if follow_form.is_valid():
            new_follow = Follow(
                user_id=user,
                follower=request.user,
                followed=user
            )
            new_follow.save()

        # when unfollow is clicked, remove the existing object
        elif unfollow_form.is_valid():
            already_following = Follow.objects.get(user_id=user, follower=request.user)
            already_following.delete()

        # redirect to show the changes 
        return redirect('profile', user_id=user)
    
    # GET request
    else:
        return render(request, "network/profile.html", {
            "user": request.user,
            "user_profile": user_profile,
            "already_following": already_following,
            "follower_count": follower_count,
            "following_count": following_count,
            "page_obj": page_obj,
            "follow_form": follow_form,
            "unfollow_form": unfollow_form
        })
    
    
@login_required(login_url="/login")    
def following(request):
    
    # a page with all the posts of followed accounts.    
    followed_accounts = Follow.objects.filter(follower=request.user)

    # when user visits the following page, but doesn't follow anyone yet, render a message
    if not followed_accounts.exists():
        return render(request, "network/following.html", {
            "message": "Not following any other users yet."
        })

    user_ids_of_followed_accounts = followed_accounts.values_list('followed__id', flat=True)
    # order post from new to old
    posts = Post.objects.filter(user_id__in=user_ids_of_followed_accounts).order_by('-post_time')

    # paginate 10 posts per page
    paginator = Paginator(posts, 10) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "network/following.html", {
        "page_obj": page_obj        
    })

# API function
@login_required(login_url="/login")
def get_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "GET":
        serialized_post = post.serialize()
        return JsonResponse(serialized_post, safe=False)       
    
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)
    

@csrf_exempt
@login_required(login_url="/login")  
def update_post(request, post_id):    
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        # Get the updated content from the request
        content = json.loads(request.body)

        if not content:
            return JsonResponse({"error": "No post content."}, status=400)

        # Update the post content
        post.post_content = content["post_content"]
        post.edited = True        
        post.save()

        # Return the updated post
        updated_post = post.serialize()       
        return JsonResponse(updated_post, safe=False)
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)


@csrf_exempt
@login_required(login_url="/login")  
def like_post(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(pk=post_id)
        user = request.user

        # Check if the user has already disliked the post
        if user in post.dislikes.all():
            post.dislikes.remove(user)
        # Check if the user has already liked the post
        if user not in post.likes.all():
            post.likes.add(user)
        post.likecount = post.likes.count() - post.dislikes.count()

        post.save()

        updated_post = post.serialize()
        updated_post["likecount"] = post.likecount         
        return JsonResponse(updated_post, safe=False)
    else:
        return JsonResponse({"error": "Invalid request method"})    


@csrf_exempt
@login_required(login_url="/login")  
def dislike_post(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(pk=post_id)
        user = request.user

        # Check if the user has already liked the post
        if user in post.likes.all():
            post.likes.remove(user)
        # Check if the user has already disliked the post
        if user not in post.dislikes.all():
            post.dislikes.add(user)
        post.likecount = post.likes.count() - post.dislikes.count()
            
        post.save()       

        updated_post = post.serialize()        
        updated_post["likecount"] = post.likecount         
        return JsonResponse(updated_post, safe=False)
    else:
        return JsonResponse({"error": "Invalid request method"})


# unused API function   
@login_required(login_url="/login")
def get_posts(request):
    try:
        posts = Post.objects.all()
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "GET":
        serialized_posts = [post.serialize() for post in posts]
        return JsonResponse(serialized_posts, safe=False)
    
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)
