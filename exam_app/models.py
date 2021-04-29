from django.db import models
import re
import bcrypt
from datetime import datetime, date, timedelta

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Invalid email format!"
        user_list = User.objects.filter(email=postData['email'])
        if len(user_list) > 0:
            errors['not_unique'] = "Email is already exists"
        if len(postData['password']) < 8 :
            errors['password'] = "Password must be at least 8 characters"
        if postData['password'] != postData['conforin_pw']:
            errors['conforin_pw'] = "Conforim password does not mactch password"
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Invalid email format!"
        if len(postData['password']) < 8 :
            errors['password'] = "Password must be at least 8 characters"
        user_list = User.objects.filter(email=postData['email'])
        if len(user_list) == 0:
            errors['email2'] = "Email not found in the database."
        elif not bcrypt.checkpw(postData['password'].encode(), user_list[0].password.encode()):
            errors['match'] = "Password not found in the database."
        return errors

class WishManager(models.Manager):
    def wish_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = "Name should be at least 2 characters"
        if len(postData['desc']) < 3:
            errors['desc'] = "Descrption should be at least 3 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    #wishes_maded
    #wishes_granted
    #liked_wishes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wish(models.Model):
    name = models.CharField(max_length=45)
    desc = models.CharField(max_length=255)
    made_by = models.ForeignKey(User, related_name="wishes_maded",on_delete = models.CASCADE)
    granted_by = models.ManyToManyField(User, related_name="wishes_granted")
    granted = models.BooleanField(default=False)
    liked_by = models.ManyToManyField(User, related_name="liked_wishes")
    liked = models.BooleanField(default=False)
    liked_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()