from __future__ import unicode_literals

from django.db import models

class User(models.Model):
	email = models.CharField(max_length=64)
	btc_address = models.CharField(max_length=64)
	hash_value = models.CharField(max_length=64)
	payment_received = models.BooleanField()
