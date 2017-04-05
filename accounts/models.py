from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from persons.models import Home
class Like(models.Model):
	user = models.ForeignKey(User)
	home = models.ForeignKey(Home)
	created = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.home.name

	def has_liked(user, home):
		qs = None
		try:
			qs = Like.objects.get(user=user, home= home)
		except:
			qs = None
		if qs:
			return True
		return False