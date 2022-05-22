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
	patient_id=models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="pharma_visites")
	pharma_id=models.ForeignKey(Pharmacie,on_delete=models.CASCADE,related_name="pharma_visites")
	class Meta:
		ordering=["-date_created"]
	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('doctor:get_visite_details', kwargs={'visite' : self.pk})
@receiver(post_save, sender=Visite)
def up(sender, instance,**kwargs):
        channel_layer=get_channel_layer()
        group=instance.pharma_id.INP
        async_to_sync(channel_layer.group_send)(group, {
            'type': 'send.visite',

            "visite":{			
            			"visite":instance.get_absolute_url(),
                        "name":instance.patient_id.person_id.nom+" "+instance.patient_id.person_id.prenom,
                        "img":instance.patient_id.person_id.img.url,
                        "email":instance.patient_id.person_id.user.email,
                        "sexe":instance.patient_id.person_id.sexe,
                        "username":instance.patient_id.person_id.user.username,
                        "adress":instance.patient_id.person_id.adresse,
                        "ville":instance.patient_id.person_id.ville,
                        "phone":instance.patient_id.person_id.phone,
                        "profile":instance.patient_id.get_absolute_url(),
                        "nais":str(instance.patient_id.person_id.datedenaissance)

                        }

            }
    )
