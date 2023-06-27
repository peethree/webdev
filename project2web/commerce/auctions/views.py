from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from datetime import datetime

from .models import User, Auction, Comment, Bid, Watchlist


class NewListing(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description")
    starting_bid = forms.DecimalField(label="Starting bid", decimal_places=2)  
    image = forms.ImageField(label="Product image")   
    CATEGORY_CHOICES = [             
        ("Art", "Art"),    
        ("Books", "Books"),   
        ("Computer", "Computer"),
        ("Electronics", "Electronics"),    
        ("Health & Fitness", "Health & Fitness"),      
        ("Travel", "Travel"),   
        ("Other", "Other")]
    category = forms.ChoiceField(label="Category", choices=CATEGORY_CHOICES)   
    # submit form button
    _ = forms.CharField(widget=forms.widgets.Input(attrs={"type": "submit", "value": "Create listing"}))


class NewBid(forms.Form):
    bid = forms.DecimalField(label="", decimal_places=2)
    # button to submit bids
    _ = forms.CharField(widget=forms.widgets.Input(attrs={"type": "submit", "value": "Bid"}))


class NewWatchlist(forms.Form):    
    add = forms.CharField(label="", widget=forms.widgets.Input(attrs={"type": "submit", "value": "Add to watchlist"}))           

    
class RemoveWatchlistItem(forms.Form):    
    remove = forms.CharField(label="", widget=forms.widgets.Input(attrs={"type": "submit", "value": "Remove from watchlist"}))           


class CloseAuction(forms.Form):    
    end = forms.CharField(label="", widget=forms.widgets.Input(attrs={"type": "submit", "value": "Close your auction"}))  


class NewComment(forms.Form):
    comment = forms.CharField(label="",widget=forms.Textarea(attrs={"rows": 3, "cols": 45}))
    # button to post comment
    post = forms.CharField(label="", widget=forms.widgets.Input(attrs={"type": "submit", "value": "Post comment"}))    
    


def index(request):
    auctions = Auction.objects.all()
    return render(request, "auctions/index.html", {
        "auctions": auctions
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
    
@login_required(login_url="/login")
def create_listing(request):    
    """allows users to list products for auction"""

    if request.method == "POST":
        # form needs both POST and FILES data, FILES is for the image the user uploads.
        form = NewListing(request.POST, request.FILES)        
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            category = form.cleaned_data["category"]               
            image = request.FILES.get("image")                 
            user_id = request.user 

            # create listing object, populate its fields
            listing = Auction(
                title=title, 
                description=description, 
                starting_bid=starting_bid, 
                image=image, 
                user_id=user_id,
                category=category
                )

            listing.save()
            return redirect("index")
    else:
        form = NewListing() 

    return render(request, "auctions/createlisting.html", {
        "form": form    
    })


#TODO: instead of using title as a means to load the page, use a unique id instead. 
# In that case 2 auctions can have the same title and still be redirected to.
@login_required(login_url="/login")
def listing(request, title):
    """view function for auction details"""

    # try to get the title of the auction that we want to visit the page of. if unsuccessful, auction doesn't exist
    try:
        auction = Auction.objects.get(title=title)
    except Auction.DoesNotExist:
        return render(request, "auctions/pagenotfound.html")
    
    # if user_id and auction_id of current auction match with those of an item on the user's watchlist: on_watchlist gets set to True
    on_watchlist = False
    if request.user.is_authenticated:
        on_watchlist = Watchlist.objects.filter(user_id=request.user, auction_id=auction).exists()
    
    # user submits any of the page's forms
    if request.method == "POST":
        # new bid form
        form = NewBid(request.POST)
        
        # add item to watchlist form
        form2 = NewWatchlist(request.POST)

        # remove item from watchlist form
        form3 = RemoveWatchlistItem(request.POST)

        # close auction form
        form4 = CloseAuction(request.POST)

        # comment form
        form5 = NewComment(request.POST)
       
        if form.is_valid():     

            # auction must be open for users to make bids
            if auction.closed == False:                 
                   
                # first bid can be same as starting bid    
                if auction.bid_number == 0:              
                    bid = Bid(
                        user_id=request.user,
                        auction_id=auction,
                        bid_time=datetime.now(),
                        bid_amount=form.cleaned_data["bid"])
                    
                    if bid.bid_amount >= auction.starting_bid:
                        # updating the value of auction.starting_bid with the value of the latest viable bid
                        auction.starting_bid = bid.bid_amount
                        auction.bid_number += 1  

                        bid.save()
                        auction.save()      
                    else:
                        raise forms.ValidationError("Bid must be higher than the starting bid.")    
                                
                

                # consecutive bids must be larger            
                else:
                    bid = Bid(
                        user_id=request.user,
                        auction_id=auction,
                        bid_time=datetime.now(),
                        bid_amount=form.cleaned_data["bid"])

                    if bid.bid_amount > auction.starting_bid:
                        auction.starting_bid = bid.bid_amount

                        # increment bid number when validation criteria are met and update db with new highest bidding price
                        auction.bid_number += 1

                        bid.save()
                        auction.save()     
                    else:
                        raise forms.ValidationError("Bid must be higher than the previously highest bid")                                         

        # user tries to add item to watchlist
        elif form2.is_valid():

            watchlist = Watchlist(
                user_id=request.user,
                auction_id=auction)     
            watchlist.save()   

        # user tries to remove item from watchlist
        elif form3.is_valid():

            watchlist = Watchlist.objects.get(user_id=request.user, auction_id=auction)     
            watchlist.delete()

        # user tries to close auction
        elif form4.is_valid():   

            # close the auction
            auction.closed=True        
            
            # filter for bids on the auction
            closing_bid = Bid.objects.filter(auction_id=auction)
            
            final_bid = None

            # if someone made a viable bid at all 
            if closing_bid:                
                final_bid = auction.bid_set.latest("bid_time")     

            # get the username of the person who placed the final bid.
            if final_bid:                                
                auction.winner=final_bid.user_id.username

            auction.save()        
        
        # user attempts to post a comment
        elif form5.is_valid():
            comment = Comment(
                auction_id=auction,
                user_id=request.user,
                message = form5.cleaned_data["comment"],
                time_sent=datetime.now())
            comment.save()              

        return redirect('listing', title=title)
    
    # GET request
    else:        
        bids = Bid.objects.filter(auction_id=auction)    

        # if a fresh auction has no bids, set bids and recent_bidder to None. 
        # otherwise variables will be referenced without having a value
        if not bids:
            bids = None   
            recent_bidder = None 
        else:    
            # Most recent, viable bid will be the winning bid
            latest_bid = auction.bid_set.latest("bid_time")  
            recent_bidder = latest_bid.user_id       
        
        comment = Comment.objects.filter(auction_id=auction)

        # similar to bids, if there are no comments yet for a specific auction, set comment to None
        if not comment:
            comment = None   

        return render(request, "auctions/listing.html", {
            "auction": auction,
            "form": NewBid(),   
            "form2": NewWatchlist(),
            "form3": RemoveWatchlistItem(),
            "form4": CloseAuction(),
            "form5": NewComment(),         
            "bids": bids,
            "recent_bidder": recent_bidder,
            "comment": comment,
            "on_watchlist": on_watchlist
        })    
    
    
@login_required(login_url="/login")
def watchlist(request): 
    """list of auctions user wants to keep track of"""   
                
    watchlists = Watchlist.objects.filter(user_id=request.user)     
    
    return render(request, "auctions/watchlist.html", {                                   
        "watchlists": watchlists
    })
        
        
def categories(request):
    """all the (currently existing) categories of auctions"""

    auction_categories = Auction.objects.values_list("category", flat=True).distinct()
    
    return render(request, "auctions/categories.html", {                                   
        "auction_categories": auction_categories        
    })


def auctions_by_category(request, category):   
    """list of auctions for each category"""    

    auction_objects = Auction.objects.filter(category=category)

    return render(request, "auctions/auctions_by_category.html", {
        "auction_objects": auction_objects,
        "category": category
    })
        
    
        


 

