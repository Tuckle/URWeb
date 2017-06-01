from django.db import models

class User(models.Model):
	username = models.CharField(max_length = 50)
	firstname = models.CharField(max_length = 50)
	lastname = models.CharField(max_length = 50)
	password = models.CharField(max_length = 32)
	email = models.CharField(max_length = 30)
	pos_lat = models.CharField(max_length = 30)
	pos_lng = models.CharField(max_length = 30)
	pos_timestamp = models.DateTimeField(auto_now = True)
	class Meta:
		db_table = "User"

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
