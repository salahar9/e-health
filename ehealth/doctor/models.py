from django.db import models
from patient.models import Patient
from landing.models import Person
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.serializers import serialize
import logging
logger = logging.getLogger(__name__)

class Doctor(models.Model):
	person_id=models.OneToOneField(Person,on_delete=models.CASCADE)
	ville = models.CharField(max_length=250)
	adresse= models.CharField(max_length=250)
	INP=models.IntegerField(primary_key=True)
	speciality=models.CharField(max_length=255)
	created=models.DateField(auto_now_add=True)
	activated=models.BooleanField(default=0)
class Visite(models.Model):
	date_created=models.DateTimeField(auto_now_add=True)
	patient_id=models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="visites")
	medcin_id=models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name="visites")
	class Meta:
		ordering=["-date_created"]
	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('doctor:get_visite_details', kwargs={'pk' : self.pk})
class Appointement(models.Model):
	class time(models.TextChoices):
		Matin = "09h - 12h"
		Midi = "12h - 14h"
		apres = "14h - 17h"
	class status_choices(models.TextChoices):
		accepted = "1"
		waiting = "2"
		refused = "3"
	patient_id=models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="appointements")
	medcin_id=models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name="appointements")
	date=models.DateField()
	heure=models.CharField(max_length=255,choices=time.choices)
	status=models.CharField(max_length=1,choices=status_choices.choices)
	class Meta:
		ordering=["-date"]
class Note(models.Model):
	id_visite=models.ForeignKey('Visite', on_delete=models.CASCADE)
	date_created=models.DateTimeField(auto_now_add=True)
	note=models.CharField(max_length=255)
	class Meta:
		ordering=["-date_created"]
@receiver(post_save, sender=Visite)
def up(sender, instance,**kwargs):
        channel_layer=get_channel_layer()
        group=instance.medcin_id.INP
        async_to_sync(channel_layer.group_send)(group, {
            'type': 'send.visite',

            "visite":{			
            			"visite":instance.get_absolute_url(),
                        "name":instance.patient_id.person_id.nom+" "+instance.patient_id.person_id.prenom,
                        "img":instance.patient_id.person_id.img.avatar.url,
                        "email":instance.patient_id.person_id.user.email,
                        "sexe":instance.patient_id.person_id.sexe,
                        "username":instance.patient_id.person_id.user.username,
                        "adress":instance.patient_id.person_id.adresse,
                        "ville":instance.patient_id.person_id.ville,
                        "phone":instance.patient_id.person_id.phone,
                        "profile":instance.patient_id.get_absolute_url()

                        }

            }
    )
