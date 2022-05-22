from django.db import models
from django.conf import settings
from landing.models import Person
from patient.models import Patient
class Pharmacie(models.Model):
	person_id=models.OneToOneField(Person,on_delete=models.CASCADE)
	INP=models.IntegerField(primary_key=True)
	nom = models.CharField(max_length=30)
	ville = models.CharField(max_length=30)
	adresse=models.CharField(max_length=255)
	activated=models.BooleanField(default=False)
class Visite(models.Model):
	date_created=models.DateTimeField(auto_now_add=True)
	patient_id=models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="visites")
	pharma_id=models.ForeignKey(Pharmacie,on_delete=models.CASCADE,related_name="visites")
	class Meta:
		ordering=["-date_created"]
	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('doctor:get_visite_details', kwargs={'visite' : self.pk})