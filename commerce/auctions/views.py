from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django import forms
import decimal

from .models import *
from .forms import *

def index(request):
    listings = Listing.objects.filter(active_listing="YES").all()
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        watchlist_count = Watchlist.objects.filter(watcher=user.id).count()
    else:
        watchlist_count = 0

    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist_count": str(watchlist_count)
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

def categories(request):
    return HttpResponse("Categories!!!")

@login_required()
def watchlist(request):
    watchlists = Watchlist.objects.filter(watcher=request.user.id).all()
    return render(request, "auctions/watchlist.html", {
        "watchlists": watchlists
    }) 

@login_required()
def create_listing(request):

    if not request.user.is_authenticated: 
        message = "Invalid credentials"
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        listing_form = ListingForm(request.POST, request.FILES) 
        if listing_form.is_valid():
            listing_form.save()
            message = "Successfly saved!"
        else:
            message = "Value is not valid!"

        return render(request, "auctions/create_listing.html", {
            "message": message
        })

    else:
        listing_form = ListingForm()        
        return render(request, "auctions/create_listing.html", {
            "form": listing_form 
        })

def listing_page(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bidding_price = listing.starting_bid + decimal.Decimal('0.1')
    num_bidders = Bid.objects.filter(item=listing)
    max_price = Bid.objects.filter(item=listing).order_by('-price').first()

    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        watchlist_count = Watchlist.objects.filter(watcher=user.id, item=listing).count()
        bid_count = Bid.objects.filter(item=listing).count()
        if bid_count > 1:
            bid_max = Bid.objects.filter(item=listing).order_by('-price').first()
            bid_tie = Bid.objects.filter(item=listing, price=bid_max.price)
            # highest bidders => bid_tie[].bidder
            # if bid_tie.count() > 1:
                # handle who is who
            # compare request.user.username with bid_tie[].bidder ??
            # if request.user.username == bid_max.bidder:
                # You're the the current bidder, highest bidder
        else:
            bid_max = 0
            bid_tie = ""

        return render(request, "auctions/listing_page.html", {
            "listing": listing,
            "bidding_price": bidding_price,
            "watchlist_count": watchlist_count,
            "bid_count": bid_count,
            "bid_max": bid_max
        })

    else:
        watchlist_count = 0

    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "bidding_price": bidding_price,
        "watchlist_count": watchlist_count
    })

@login_required()
def bidding_adding_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(pk=request.user.id)

    if request.method == "POST":
        if 'placebid' in request.POST:
            bid_value = request.POST['bid']
            listing.starting_bid = bid_value
            listing.save()
            message = "Successfully updated bidding!"

        elif 'add-watchlist' in request.POST:
            listing.watchlist = "YES"
            listing.save()
            # user = User.objects.get(pk=request.user.id)
            w = Watchlist(watcher=user, item=listing)
            w.save()
            message = "Successfully added to watch list!"

        elif 'remove-watchlist' in request.POST:
            listing.watchlist = "NO"
            listing.save()
            # user = User.objects.get(pk=request.user.id)
            w = Watchlist.objects.filter(watcher=user, item=listing).delete()
            message = "Delete the watch list!"


    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "message": message
    })
