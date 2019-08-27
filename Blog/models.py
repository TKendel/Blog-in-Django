from django.db import models
from django.db.models.signals import post_save
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User


class Category( models.Model ):
	name = models.CharField( max_length = 255 )
	created_at = models.DateTimeField( auto_now_add = True )
	updated_at = models.DateTimeField( auto_now = True )
	#ovo nam koriste create viewovima kao succesurl kada su gotovi
	def get_absolute_url(self):
		return reverse("Posts:ShowCategories")

	def __str__( self ):
		return self.name


class Tag( models.Model ):
	name = models.CharField( max_length = 255 )
	created_at = models.DateTimeField( auto_now_add = True )
	updated_at = models.DateTimeField( auto_now = True )

	def get_absolute_url(self):
		return reverse("Posts:ShowTags")

	def __str__( self ):
		return self.name


class Post( models.Model ):
	user = models.ForeignKey( User, on_delete = models.CASCADE, null = True )
	category = models.ForeignKey( 'Category' , on_delete = models.CASCADE )
	tags = models.ManyToManyField( Tag )
	title = models.CharField( max_length = 255 )
	slug = models.SlugField( max_length = 255 )
	description = models.TextField()
	thumbnail = models.ImageField( upload_to = 'images', blank = True, null = True )
	created_at = models.DateTimeField( auto_now_add = True ) #ovako ce automatski napraviti datum kreacije
	updated_at = models.DateTimeField( auto_now = True )
	
	def get_absolute_url(self):
		return reverse("Posts:Welcome")

	def approved_comments(self):
		return self.comments.filter(approved_comments = True)

	def __str__( self ):	#ovo ce imenovat nas querry prema titlu da nije numerirano
		return self.title


class Settings( models.Model ):
	siteName = models.CharField( max_length = 255, default="test")
	contact_number = models.CharField( max_length = 255, default="000" )
	contact_address = models.CharField( max_length = 255, default="test" )
	email = models.EmailField( max_length = 255, default="test@test.com")
	created_at = models.DateTimeField( auto_now_add = True )
	updated_at = models.DateTimeField( auto_now = True )

	def get_absolute_url(self):
		return reverse("Posts:Welcome")

	def __str__( self ):
		return self.siteName


class Profile( models.Model ):
	user = models.OneToOneField( User, on_delete = models.CASCADE) #spajanje profile sa userom
	avatar = models.ImageField( upload_to = 'images', blank = True, default = "" )
	about = models.TextField( blank = True, default = "" )
	link = models.CharField( max_length = 255, blank = True, default = "" )
	created_at = models.DateTimeField( auto_now_add = True)
	updated_at = models.DateTimeField( auto_now = True)

def create_profile(sender, **kwargs):
	user = kwargs["instance"]
	if kwargs["created"]:
		user_profile = Profile(user = user)
		user_profile.save()
post_save.connect(create_profile, sender = User)


class Comment(models.Model):
	post = models.ForeignKey( Post, on_delete = models.CASCADE )
	author = models.CharField( max_length = 200 )
	text = models.TextField()
	created_at = models.DateTimeField( auto_now_add = True )
	approved_comment = models.BooleanField( default = False )

	def approved(self):
		self.approved_comment = True
		self.save()

	def __str__(self):
		return self.text
