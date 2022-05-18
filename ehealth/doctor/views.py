from django.shortcuts import render,get_object_or_404,redirect
from patient.models import Patient
from ordonnance.models import Ordonnance
from doctor.models import Visite,Doctor,Appointement,Note
from med.models import Meds
from django.core import serializers
from django.views.decorators.http import require_POST
from  django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import logging
import datetime
from django.db.models import Q    

from django.contrib.auth.decorators import login_required
from .decorators import check_doctor,check_activated

from django.db.models.aggregates import Count
PAGINATION_COUNT=10
def register(request):
	if request.method=="POST":
		params=request.POST
		INP=params["INP"]
		ville=params["ville"]
		adresse=params["adresse"]
		speciality=params["speciality"]
		if INP=="" or ville=="" or ville=="":
			return render(request,"patient/edit.html",{"profile_settings":True})

		obj=Doctor.objects.update_or_create(
			person_id=request.user.person,
			defaults={"ville":ville,"INP":INP,"speciality":speciality,"adresse":adresse})
		
		
		return  redirect("doctor:visites")
	else:
		return render(request,"patient/edit.html",{"profile_settings":True})

@require_POST
@csrf_exempt
def create_visite(request):
	"""
	date_created=models.DateField(auto_now_add=True)
	patient_id=models.OneToOneField(Doctor,on_delete=models.CASCADE)
	medcin_id=models.OneToOneField(Patient,on_delete=models.CASCADE)"""
	params=request.POST
	patient=params["patient"]
	medcin=params["medcin"]
	patient=Patient.objects.get(pk=patient)
	medcin=Doctor.objects.get(pk=medcin)
	obj=Visite(patient_id=patient,medcin_id=medcin)
	obj.save()
	data={"Done":"Visite created"}
	return  JsonResponse(data)
@require_POST
@csrf_exempt
def get_meds_history(request):
	params=request.POST
	patient=params["patient"]
	visites = Visite.objects.filter(patient_id=patient).values("id")
	privacy = Patient.objects.get(pk=patient,activated=True).permission_privacy
	data={"error":"you're not allowed"}
	if privacy==False:
		return JsonResponse(data)
	meds=Ordonnance.objects.filter(id_visite__in=visites,le_type="Medicaments").values()
	# res={}
	# i=0
	# for med in meds:
	# # 	x=Ordonnance.objects.filter(id_visite=visite.id,le_type="Medicaments")
	#  	res[f"{i}"]=med
	#  	i+=1
	return JsonResponse({"result":list(meds)})

@require_POST
@csrf_exempt
def get_visites_history(request):
	params=request.POST
	patient=params["patient"]
	visites = Visite.objects.filter(patient_id=patient)
	privacy = Patient.objects.get(pk=patient).permission_privacy
	data={"error":"you're not allowed"}
	if privacy==False:
		return HttpResponse(data, mimetype='application/json')
	
	return render(request,"visites.html",{"result":visites})
@check_activated
@login_required
@check_doctor
def get_doc_visites_history(request):
	doctor=request.user.person.doctor
	visites = Visite.objects.filter( medcin_id=doctor.INP)	
	filt=datetime.date.today()-datetime.timedelta(days=7)
	pat_stat=Patient.objects.filter(visites__medcin_id=doctor,visites__date_created__gte=filt).aggregate(
							tot=Count("id",distinct=True),visites_sum=Count("visites",filter=Q(visites__medcin_id=doctor),distinct=True),
							appoint_count=Count("appointements",filter=Q(appointements__medcin_id=doctor),distinct=True)
						)
	
	paginator=Paginator(visites, PAGINATION_COUNT)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	temp_data={"data":page_obj,'visite_seek':True,"title":"My Consultations","num_doc":pat_stat["tot"],"num_visite":pat_stat["visites_sum"],"num_appointement":pat_stat["appoint_count"]}
	return render(request,"doctor/visites.html",temp_data)

@check_activated
@login_required
@check_doctor
def get_visite_details(request,visite):
	visite=get_object_or_404( Visite,pk=visite)
	traitements=Ordonnance.objects.filter(id_visite=visite,le_type="Traitement")
	meds=Ordonnance.objects.filter(id_visite=visite,le_type="Medicaments").select_related("id_medicament")
	privacy=visite.patient_id.permission_privacy
	modifiable=True
	notes=Note.objects.filter(id_visite=visite)

	condition=int(request.user.person.doctor.INP)!=visite.medcin_id.INP
	if condition:
		modifiable=False
	if modifiable ==False and privacy==0:
		return HttpResponse({"error":"you're not allowed"}, mimetype='application/json')


	return render(request,"doctor/visite_details.html",{
				"modifiable":modifiable,
				"show_notes":modifiable,
				"visite":visite,
				"profile":True,
				"traitements":traitements,
				"meds":meds,
				"notes":notes,

		})

@check_activated
@login_required
@check_doctor
def dashboard(request):
	doctor=request.user.person.doctor
	filt=datetime.date.today()-datetime.timedelta(days=7)
	pat_stat=Patient.objects.filter(visites__medcin_id=doctor,visites__date_created__gte=filt).aggregate(
							tot=Count("id",distinct=True),visites_sum=Count("visites",filter=Q(visites__medcin_id=doctor),distinct=True),
							appoint_count=Count("appointements",filter=Q(appointements__medcin_id=doctor),distinct=True)
						)
	visites = Visite.objects.filter(medcin_id=doctor).values('patient_id')
	pat=Patient.objects.filter(pk__in=visites).distinct()[:3]
	appointements=Appointement.objects.filter(medcin_id=request.user.person.doctor,status="2")[0:3]
	appointements_list=Appointement.objects.filter(medcin_id=request.user.person.doctor)[:6]
	return render(request,"doctor/dashboard.html",{"appointements":appointements,"dashboard":True,"title":"Dashoard","last_3":pat,"visites":appointements_list,"num_doc":pat_stat["tot"],"num_visite":pat_stat["visites_sum"],"num_appointement":pat_stat["appoint_count"]})
@check_activated
@login_required
@check_doctor
def get_patient(request):
	doctor=request.user.person.doctor
	filt=datetime.date.today()-datetime.timedelta(days=7)
	visites = Visite.objects.filter(medcin_id=doctor).values('patient_id')
	pat=Patient.objects.filter(pk__in=visites).distinct()
	pat_stat=Patient.objects.filter(visites__medcin_id=doctor,visites__date_created__gte=filt).aggregate(
							tot=Count("id",distinct=True),visites_sum=Count("visites",filter=Q(visites__medcin_id=doctor),distinct=True),
							appoint_count=Count("appointements",filter=Q(appointements__medcin_id=doctor),distinct=True)
						)
	paginator=Paginator(pat, PAGINATION_COUNT)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request,"doctor/visites.html",{"data":page_obj,"title":"Patients","get_patient":True,"num_doc":pat_stat["tot"],"num_visite":pat_stat["visites_sum"],"num_appointement":pat_stat["appoint_count"]})
@check_activated
@login_required
@check_doctor
@require_POST
def add_note(request,visite):
	note=request.POST['note']
	visite=get_object_or_404(Visite,pk=visite)
	note=Note(id_visite=visite,note=note)
	note.save()
	return redirect("doctor:get_visite_details",visite=visite.pk)
def fill(request):
	import sqlite3
	db=sqlite3.connect("meds.db")
	cur=db.cursor()
	sql="SELECT * FROM Meds"
	res=cur.execute(sql)

	for x in res:
		logging.warning(x)
		Meds.objects.create(
			code=x[0],
			nom=x[2] ,
			dci1=x[3],
			dosage1=x[4],
			unite_dosage1=x[5],
			forme=x[6],
			presentation=x[7],
			ppv=x[8],
			ph=x[9],
			prix_br=x[10],
			princeps_generique=x[11],
			taux_remboursement=x[12],)

	return render(request,"doctor/visites.html",{"title":"done"})
@require_POST
@login_required
@check_activated
@check_doctor
def accept_app(request,app):
	app=Appointement.objects.get(pk=app)
	dec=request.POST["decision"]
	if int(dec)==1:
		app.status="1"
	elif int(dec)==0:
		app.status="3"
	app.save()
	return JsonResponse({"data":"DOne"})
