from django.db import models

class Entry(models.Model):
	serial = models.IntegerField(default=0)
	place = models.CharField(max_length=200) 
	total_cases = models.IntegerField(default=0)
	recovered = models.IntegerField(default=0)
	deaths = models.IntegerField(default=0)
	def __str__(self):
		return self.place 


