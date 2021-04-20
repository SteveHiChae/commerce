from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing_page/<int:listing_id>", views.listing_page, name="listing_page"),
    path("bidding_adding_watchlist/<int:listing_id>", views.bidding_adding_watchlist, name="bidding_adding_watchlist")
]
