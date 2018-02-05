from django.shortcuts import render, redirect

from .models import User, Wishlist, UserList
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "wishlist_app/index.html")

def register(request):
    print request.POST
    response = User.objects.register(
        name = request.POST["name"],
        username = request.POST["username"],
        password = request.POST["password"],
        confirm_password = request.POST["confirm_password"],
        datehired = request.POST["datehired"]
    )

    if response["valid"]:
        request.session["user_id"] = response["user"].id
        messages.add_message(request, messages.SUCCESS, "Welcome!")
        return redirect("/dashboard")
    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)

    return redirect("/")

def login(request):
    response = User.objects.login(
        username=request.POST["username"],
        password=request.POST["password"]
    )

    if response["valid"]:
        request.session["user_id"] = response["user"].id
        messages.add_message(request, messages.SUCCESS, "Welcome!")
        return redirect("/dashboard")
    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)

    return redirect("/")

def logout(request):
    return redirect("/index")

def dashboard(request):
    if "user_id" not in request.session:
        return redirect("/")

    totalWishlist = Wishlist.objects.all().exclude(id=request.session["user_id"])
    # myItems = Wishlist.objects.filter(id=request.session["user_id"])
    myWishlist_items = UserList.objects.filter(user_id=request.session["user_id"])
    myAddedItems = Wishlist.objects.filter(added_by_id=request.session["user_id"])

    for items in myWishlist_items:
        totalWishlist = totalWishlist.exclude(id=items.wishlist.id)

    for items in myAddedItems:
        totalWishlist = totalWishlist.exclude(added_by_id=request.session["user_id"])

    context = {
        "user":User.objects.get(id=request.session["user_id"]),
        "wishlist": totalWishlist,
        "myItems": myAddedItems,
        "myList": myWishlist_items
    }

    return render(request, "wishlist_app/dashboard.html", context)

def create(request):
    return render(request, 'wishlist_app/create.html')

def add_item(request):
    response = Wishlist.objects.add_item(
        item=request.POST["item"],
        added_by=User.objects.get(id=request.session["user_id"])
    )

    if response["valid"]:
        return redirect("/dashboard")
    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)

    return redirect("/create")

def myWishlist(request, id):
    UserList.objects.myWishlist(
        wishlist=Wishlist.objects.get(id=id),
        user=User.objects.get(id=request.session["user_id"])
    )

    return redirect("/dashboard")

def removeItem(request, id):
    UserList.objects.removeItem(id=id)
    return redirect("/dashboard")

def deleteItem(request, wishlist_id):
    deleted_item = Wishlist.objects.get(id=wishlist_id)
    deleted_item.delete()
    data = {
        "deleted": deleted_item
    }
    return redirect("/dashboard", data)

def wish_item(request, id):
    wishedBy = UserList.objects.filter(wishlist_id=id)
    firstwisher = Wishlist.objects.filter(added_by_id=id)

    context = {
        "wishers":wishedBy,
        "wishItem":Wishlist.objects.get(id=id),
        "mainwisher": firstwisher
    }
    print firstwisher
    return render(request, "wishlist_app/wish_item.html", context)