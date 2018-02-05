from __future__ import unicode_literals

from django.db import models

import bcrypt
from datetime import datetime

# Create your models here.
class UserManager(models.Manager):
    def register(self, name, username, password, confirm_password, datehired):

        response = {
            "errors": [],
            "user": None,
            "valid": True
        }

        if len(name) < 3:
            response["valid"] = False
            response["errors"].append("Name must be at least 3 characters!")
        if len(username) < 3:
            response["valid"] = False
            response["errors"].append("Username must be at least 3 characters!")
        else:
            list_of_usernames = User.objects.filter(username=username.lower())
            if len(list_of_usernames) > 0:
                response["valid"] = False
                response["errors"].append("Username already exists")
        if len(password) < 8:
            response["valid"] = False
            response["errors"].append("Password must be 8 characters or more")
        if confirm_password != password:
            response["valid"] = False
            response["errors"].append("Password must match confirm password")
        if len(datehired) < 1:
            response["valid"] = False
            response["errors"].append("Date hired is required")
        else:
            date = datetime.strptime(datehired, '%Y-%m-%d')
            today = datetime.now()
            if date > today:
                response["errors"].append("Date hired must be today or before.")
        if response["valid"]:
            response["user"] = User.objects.create(
                name=name,
                username=username.lower(),
                password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
            datehired=datehired
            )
        return response

    def login(self, username, password):

        response = {
            "errors": [],
            "user": None,
            "valid": True
        }

        if len(username) < 1:
            response["valid"] = False
            response["errors"].append("Failed to login username is required")
        else:
            list_of_usernames = User.objects.filter(username=username.lower())
            if len(list_of_usernames) == 0:
                response["valid"] = False
                response["errors"].append("Failed to login username not registered")
        if len(password) < 8:
            response["valid"] = False
            response["errors"].append("Login failed password incorrect")

        if response["valid"]:
            if bcrypt.checkpw(password.encode(), list_of_usernames[0].password.encode()):
                response["user"] = list_of_usernames[0]
            else:
                response["valid"] = False
                response["errors"].append("Incorrect Password")

        return response

class WishlistManager(models.Manager):
    def add_item(self, item,  added_by):

        response = {
            "errors": [],
            "course": None,
            "valid": True
        }

        if len(item) < 4:
            response["valid"] = False
            response["errors"].append("Item name should be more than 3 characters.")

        if response["valid"]:
            response["quote"] = Wishlist.objects.create(
                item=item,
                added_by=added_by
            )
        return response

class UserListManager(models.Manager):
    def myWishlist(self, wishlist, user):
        UserList.objects.create(
            wishlist=wishlist,
            user=user
        )
        return

    def removeItem(self, id):
        UserList.objects.get(id=id).delete()
        return

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    datehired = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Wishlist(models.Model):
    item = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, related_name="added_item")
    date_added = models.DateTimeField(auto_now_add=True)
    objects = WishlistManager()

class UserList(models.Model):
    user = models.ForeignKey(User, related_name="wishlist_item")
    wishlist = models.ForeignKey(Wishlist, related_name="wishlisted_item")
    objects = UserListManager()