from django.db import models
from pharmacie.models import Pharmacie
import logging
from doctor.models import Visite
from med.models import Meds
from mutuelle.models import AllMutuelle
# Create your models here.

class Ordonnance(models.Model):
	id_visite=models.ForeignKey(Visite, on_delete=models.CASCADE,related_name="ordonnance")
	class typee(models.TextChoices):
		Traitement = 'Traitement'
		Medicaments = 'Medicaments'
	le_type=models.CharField(max_length=13,choices=typee.choices)
	id_medicament=models.ForeignKey(Meds,null=True,blank=True,on_delete=models.CASCADE)
	description_de_traitement=models.CharField(max_length=255)
	id_pharmacie=models.ForeignKey(Pharmacie,on_delete=models.CASCADE,null=True,blank=True)
	quantite=models.IntegerField(null=True,blank=True)
	price=models.FloatField(null=True,blank=True)
	a_mutuelle=models.BooleanField(default=False)
	nom_traitement=models.CharField(max_length=255,null=True,blank=True)
	date_purchase=models.DateTimeField(null=True,blank=True)
	date_created=models.DateTimeField(auto_now_add=True)
	class Meta:
		ordering=["-date_created"]
	def save(self,*args, **kwargs):
		if self.le_type=="Medicaments":
			logging.warning(f"{self.quantite},{self.id_medicament.prix_br}")
			self.price=float(self.quantite)*self.id_medicament.prix_br
		elif self.le_type=="Traitement" and self.id_visite.patient_id.a_mutuelle:
			
			try:
				mut=AllMutuelle(visite_id=self.id_visite,total=0,mutuelle_status="P")
				mut.save()
			except:
				AllMutuelle.objects.get(visite_id=self.id_visite)
		mut.total+=self.price
		mut.save()

		super(Ordonnance, self).save(*args, **kwargs)

