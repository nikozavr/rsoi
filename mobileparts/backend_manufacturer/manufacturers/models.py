from django.db import models

# Create your models here.
class Manufacturer(models.Model):
	name = models.CharField(max_length=30)
	established = models.IntegerField()
	country = models.CharField(max_length=30)

	def as_json(self):
		return dict(id=self.id, 
			name=self.name, 
			established =self.established,
			country=self.country)