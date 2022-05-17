from django.db import models
from landing.models import Person

class Patient(models.Model):
	person_id=models.OneToOneField(Person,on_delete=models.CASCADE)
	class Gender(models.TextChoices):
		Male = 'M'
		Female = 'F'
	card_id=models.CharField(max_length=30,blank=True,null=True)
	permission_privacy=models.BooleanField(default=False)
	a_mutuelle=models.BooleanField(default=False,null=True,blank=True)
	immatriculation=models.IntegerField(null=True,blank=True)
	date_adhesion=models.DateField( null=True,blank=True)
	n_affiliation=models.IntegerField(null=True,blank=True)
	def save(self, *args, **kwargs):
		self.a_mutuelle=(True if (self.permission_privacy is not None and 
			self.immatriculation is not None and 
			self.date_adhesion is not None and 
			self.n_affiliation is not None) else False)
		super(Patient, self).save(*args, **kwargs)
	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('patient:profile', kwargs={'pk' : self.pk})

 	