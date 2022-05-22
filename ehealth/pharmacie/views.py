from django.shortcuts import render
from doctor.models import Visite
from ordonnance.models import Ordonnance
from pharmacie.models import Pharmacie,Visite
import datetime
from django.views.decorators.http import require_POST
from  django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models.aggregates import Count,Sum
from django.contrib.auth.decorators import login_required
from .decorators import check_pharmacist
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import logging
# Create your views here.

@require_POST
@csrf_exempt
def create_visite(request):
	"""
	date_created=models.DateField(auto_now_add=True)
	patient_id=models.OneToOneField(Doctor,on_delete=models.CASCADE)
	medcin_id=models.OneToOneField(Patient,on_delete=models.CASCADE)"""
	params=request.POST
	patient=params["patient"]
	pharma=params["pharma"]
	patient=Patient.objects.get(pk=patient)
	pharma=Pharmacie.objects.get(pk=pharma)
	obj=Visite(patient_id=patient,pharma_id=pharma)
	obj.save()
	data={"Done":"Visite created"}
	return  JsonResponse(data)
@login_required
@check_pharmacist
def dashboard(request):
	filt=datetime.date.today()-datetime.timedelta(days=7)
	ordonnances=Ordonnance.objects.filter(
		le_type="Medicaments",id_pharmacie=request.user.person.pharmacie.pk,
		).order_by("-date_purchase").select_related("id_visite__patient_id")

	ordonnances_stats=Ordonnance.objects.filter(
		le_type="Medicaments",id_pharmacie=request.user.person.pharmacie.pk,date_purchase__gte=filt
		).aggregate(
		count=Count("id_visite__patient_id",distinct=True),prix=Sum("price",distinct=True)
		)
	
	#logging.warning(ordonnances[0].prix)
	
	
	return render(request,"pharmacist/dashboard.html",{"dashboard":True,"title":"Dashboard","pat_num":ordonnances_stats["count"],"income":ordonnances_stats["prix"],"ordonnances":ordonnances})

@login_required
@check_pharmacist
def register(request):
	if request.method=="POST":
			try:
				INP=request.POST["INP"]
				ville=request.POST["ville"]
				adresse=request.POST["adresse"]
				nom=request.POST["nom"]
				
				Pharmacie.objects.update_or_create(
					person_id=request.user.person,
					defaults={"INP":INP,"ville":ville,"adresse":adresse,"nom":nom}
					)
				messages.add_message(request,messages.SUCCESS,"Values Updated")
				return JsonResponse({"data":"Done"})
			except Exception as e:
					messages.add_message(request, messages.ERROR, 'Something is Wrong')
					return JsonResponse({"data":str(e)})
	else:
			return render(request,"patient/edit.html",{"profile_settings":True,"title":"Settings & Privacy"})

def sales(request):
	ordonnances = Ordonnance.objects.filter(
            le_type="Medicaments", id_pharmacie=request.user.person.pharmacie.pk,
        ).order_by("-date_purchase").select_related("id_visite__patient_id")
	return render(request, 'pharmacist/sales.html', {'pharmacist': True, 'sales': True, "ordonnances": ordonnances})

def clients(request):
	return render(request, 'pharmacist/clients.html', {'pharmacist': True, 'clients': True})
