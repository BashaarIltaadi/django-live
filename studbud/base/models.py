from django.db import models
from django.contrib.auth.models import AbstractUser

# from django.contrib.auth.models import User

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # User
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
                                User,
                                related_name='participants',
                                blank=True)
    # Store all the active users in the room.
    updated = models.DateTimeField(auto_now=True)
    # Snapshot of anytime this model instance was updated.
    created = models.DateTimeField(auto_now_add=True)
    # Auto now takes a snapshot at every time we save this.
    # Auto now add only takes a snapshot when we first save/create this instance.
    # If we save multiple times,, auto now add will not update.
    # you can use:
    # id = # UUID

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user =  # user that's sending a message.
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # Room the user is sending message in.
    # set_NULL means when the parent is deleted, what do we want to do when with all the children
    # /messages here. if set to null the msesage would still exist in the database.
    # For cascade, it means when a room is deleted, delete all messages/children.
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]
