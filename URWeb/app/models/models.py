from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Plugins(models.Model):
	username = models.CharField(max_length = 50)
	name = models.CharField(max_length = 50)
	path = models.CharField(max_length = 255)
	description = models.CharField(max_length = 1000)	
	class Meta:
		db_table = "Plugins"

class Location(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	pos_lat = models.CharField(max_length = 30)
	pos_lng = models.CharField(max_length = 30)
	pos_timestamp = models.DateTimeField(auto_now = True)
	class Meta:
		db_table = "Location"

class Friends(models.Model):
	username1 = models.CharField(max_length = 50)
	username2 = models.CharField(max_length = 50)
	class Meta:
		db_table = "Friends"

class FriendsRequest(models.Model):
	from_user = models.CharField(max_length = 50)
	to_user = models.CharField(max_length = 50)	
	class Meta:
		db_table = "FriendsRequest"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Location.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.location.save()