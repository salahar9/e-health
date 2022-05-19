from django.shortcuts import render,redirect, get_object_or_404
from patient.models import Patient
from ordonnance.models import Ordonnance,Meds
from mutuelle.models import AllMutuelle
from doctor.models import Visite,Doctor,Appointement,Note
from django.core import serializers
from django.views.decorators.http import require_POST
from  django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q    
from django.contrib.auth.decorators import login_required
from .decorators import check_patient

from landing.models import Person 
from django.contrib import messages
import datetime,logging
from django.db.models.aggregates import Count,Sum
from django.core.paginator import Paginator
PAGINATION_COUNT=10
def register(request):
	if request.method=="POST":

		params=request.POST
		change={}
		if params.get("immatriculation") != "":
			change["immatriculation"]=params.get("immatriculation") 
		if params.get("privacy") != "":
			change["permission_privacy"]=(True if params.get("privacy").strip()=="on" else False) 
		if params.get("n_affiliation") != "":
			change["n_affiliation"]=params.get("n_affiliation") 
		if params.get("date_adhesion") != "":
			change["date_adhesion"]=params.get("date_adhesion") 
		
		if (len(change)==0) :
			return JsonResponse({"error":"no changes done"})
		obj=Patient.objects.update_or_create(
				person_id=request.user.person,
				defaults=change)
		
		messages.add_message(request, messages.ERROR,"Good job")
		return JsonResponse({"done":"done"})
	else:
		return render(request,"patient/edit.html",{"title":"Settings & Privacy","profile_settings":True})
@check_patient
@login_required
def get_patient_visites_history(request):

	pat=request.user.person.patient.id
	visites = Visite.objects.filter( patient_id=request.user.person.patient.id)
	filt=datetime.date.today()-datetime.timedelta(days=7)
	doc_stat=Doctor.objects.filter(visites__patient_id=pat,visites__date_created__gte=filt).aggregate(
							tot=Count("INP",distinct=True),visites_sum=Count("visites",filter=Q(visites__patient_id=pat),distinct=True),
							appoint_count=Count("appointements",filter=Q(appointements__patient_id=pat),distinct=True)
						)
	
	paginator=Paginator(visites, PAGINATION_COUNT)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	return render(request, "doctor/visites.html", {"data":page_obj,'visite_seek':True,"title":"My Consultations","num_doc":doc_stat["tot"],"num_visite":doc_stat["visites_sum"],"num_appointement":doc_stat["appoint_count"]})

@login_required
def get_other_visites_history(request,pk):
	pat=Patient.objects.get(pk=pk)
	if pat.permission_privacy or request.user.person.pk==pat.person_id.pk:
		visites = Visite.objects.filter( patient_id=pk)
		filt=datetime.date.today()-datetime.timedelta(days=7)
		doc_stat=Doctor.objects.filter(visites__patient_id=pat,visites__date_created__gte=filt).aggregate(
							tot=Count("INP",distinct=True),visites_sum=Count("visites",filter=Q(visites__patient_id=pat),distinct=True),
							appoint_count=Count("appointements",filter=Q(appointements__patient_id=pat),distinct=True)
						)
		allowed=True
		return render(request, "doctor/visites.html", {"patient":pat,"data":visites,"allowed":allowed,'other_visite_seek':True,"title":f"{pat.person_id.nom} {pat.person_id.prenom} Consultations","num_doc":doc_stat["tot"],"num_visite":doc_stat["visites_sum"],"num_appointement":doc_stat["appoint_count"]})

	else:
		visites=[]
		allowed=False
	logging.warning(pat.permission_privacy)
	return render(request, "patient/profile.html", {"patient":pat})

@check_patient
@login_required
def get_visite_details(request,visite):
	show_notes=False

	visite=Visite.objects.get(pk=visite)
	if visite.patient_id==request.user.person.patient:
		traitements=Ordonnance.objects.filter(id_visite=visite,le_type="Traitement")
		meds=Ordonnance.objects.filter(id_visite=visite,le_type="Medicaments").select_related("id_medicament")
		show_notes=True
		notes=Note.objects.filter(id_visite=visite)
		return render(request,"doctor/visite_details.html",{
					"show_notes":show_notes,
					"visite":visite,
					"profile":True,
					"notes":notes,
					"traitements":traitements,
					"meds":meds
			})
	else:
		return render(request,"patient/profile.html",{"patient":pat,"title":f"{pat.person_id.nom} {pat.person_id.prenom}" })
@check_patient
@login_required
def dashboard(request):
	
	pat=request.user.person.patient
	count_visites = Visite.objects.filter( patient_id=request.user.person.patient.pk).count()
	pres=Visite.objects.filter( patient_id=request.user.person.patient).annotate(count=Count("ordonnance",filter=Q(ordonnance__le_type="Medicaments"))).filter(Q(count__gt=0)).select_related("medcin_id")[:3]
	doc_stat=Doctor.objects.filter(visites__patient_id=pat,).aggregate(
							drugs_sum=Count("visites__ordonnance",filter=Q(visites__patient_id=pat,visites__ordonnance__le_type="Medicaments"),distinct=True),
							visites_sum=Count("visites",filter=Q(visites__patient_id=pat),distinct=True),
							appoint_count=Count("appointements",filter=Q(appointements__patient_id=pat),distinct=True)
						)
		
	
	query_set = AllMutuelle.objects.filter(visite_id__patient_id=request.user.person.patient)[:3]
	visites=Appointement.objects.filter(patient_id=request.user.person.patient).select_related("medcin_id")[:6]
	total = AllMutuelle.objects.filter(visite_id__patient_id=request.user.person.patient).aggregate(total=Count("id"))

	return render(request,"patient/dashboard.html",{"count_visites":doc_stat["visites_sum"],"insurances_query":query_set,"insurances":total,"dashboard":True,"num_appointement":doc_stat["appoint_count"],"visites":visites,"title":"Dashoard","presc":pres,"ordon_num":doc_stat["drugs_sum"]})
@check_patient
@login_required
def get_doc(request):
	pat=request.user.person.patient
	filt=datetime.date.today()-datetime.timedelta(days=7)
	#visites = Visite.objects.filter(patient_id=pat.pk).order_by("-date_created")
	#visites1=visites.filter(date_created__gte=filt)
	visites = Visite.objects.filter(patient_id=pat).values('medcin_id')
	doc=Doctor.objects.filter(pk__in=visites)
	#doc=Doctor.objects.filter(visites__patient_id=pat).distinct().prefetch_related("person_id")
	logging.warning(visites)
	doc_stat=Doctor.objects.filter(visites__patient_id=pat,visites__date_created__gte=filt).aggregate(
							tot=Count("INP",distinct=True),visites_sum=Count("visites",filter=Q(visites__patient_id=pat),distinct=True),
							appoint_count=Count("appointements",filter=Q(appointements__patient_id=pat),distinct=True)
						)
	paginator=Paginator(doc, PAGINATION_COUNT)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	return render(request,"doctor/visites.html",{"data":page_obj,"title":"Doctors","get_patient":True,"num_doc":doc_stat["tot"],"num_visite":doc_stat["visites_sum"],"num_appointement":doc_stat["appoint_count"]})
@login_required
def profile(request,pk):
	pat=get_object_or_404(Patient,pk=pk)
	visites = Visite.objects.filter( patient_id=pat).select_related("medcin_id")[:2]
	pres=Visite.objects.filter( patient_id=pat).annotate(count=Count("ordonnance",filter=Q(ordonnance__le_type="Medicaments"))).filter(Q(count__gt=0)).select_related("medcin_id")[:3]
	appointements_waiting=Appointement.objects.filter(status="2",patient_id=pat).aggregate(count=Count("id"))
	appointements_done=Appointement.objects.filter(status="1",patient_id=pat).aggregate(count=Count("id"))
	meds=Meds.objects.filter(ordonnance__id_visite__patient_id=pat).order_by("-ordonnance__date_purchase")[:6]
	mutuelle=AllMutuelle.objects.filter(visite_id__patient_id=pat)
	if pat.permission_privacy or request.user.person.pk==pat.person_id.pk:
		return render(request,"patient/profile_active.html",{"profile":True,"pat":pat,"title":f"{pat.person_id.nom} {pat.person_id.prenom}","visites":visites,"meds":meds,"appointements_waiting":appointements_waiting,"appointements_done":appointements_done,"pres":pres,"mutuelle":mutuelle})
	else:
		return render(request,"patient/profile.html",{"patient":pat,"title":f"{pat.person_id.nom} {pat.person_id.prenom}" })
@login_required
def get_other_presc(request,pk):
	ords=[]
	pat=Patient.objects.get(pk=pk)
	if pat.permission_privacy or request.user.person.pk==pat.person_id.pk:
		visites = Visite.objects.filter( patient_id=pk)
		allowed=True
		for v in visites:
			ordo = Ordonnance.objects.filter( id_visite=v.pk)
			if len(ordo)>0:
				for i in ordo:
						ords.append(i)
	else:
		ords=[]
		allowed=False
	return render(request, "doctor/visites.html", {"data":ords,"allowed":allowed,'other_visite_seek':True,"title":f"{pat.person_id.nom} {pat.person_id.prenom} Consultations"})
@check_patient
@login_required
def book_appointement(request,doc):
	doc=Doctor.objects.get(pk=doc)
	if request.method=="POST":
		params=request.POST
	

		app=Appointement(status="2",medcin_id=doc,patient_id=request.user.person.patient,date=params["date"],heure=params["time"])
		app.save()
		return redirect("patient:dashboard")
	else:
		return render(request,"patient/book_doctor.html",{"doc":doc,"book":True})
@check_patient
@login_required
def search_doc(request):
	
	if request.method=="POST":
		params=request.POST
		name=params.get("nom",None)

		ville=params.get("ville",None)
		docs=[]
		if ville != None or name != None:
			filters={}
			if name:
				filters["person_id__nom__icontains"]=name
			if ville:
				filters["ville"]=ville

			logging.warning(filters)
			docs=Doctor.objects.filter(**filters)
		return render(request,"patient/search_result.html",{"book":True,"docs":docs})
	else:
		return render(request,"patient/search.html",{"book":True})


@check_patient
def prescriptions(request):
	doc_stat=Doctor.objects.filter(visites__patient_id=pat,visites__date_created__gte=filt).aggregate(
							tot=Count("INP",distinct=True),visites_sum=Count("visites",filter=Q(visites__patient_id=pat),distinct=True),
							appoint_count=Count("appointements",filter=Q(appointements__patient_id=pat),distinct=True)
						)
		
	meds=Meds.objects.filter(ordonnance__id_visite__patient_id=pat).order_by("-ordonnance__date_purchase").select_related("ordonnance")
	return render(request, 'patient/prescriptions.html', {"prescriptions": True,"meds":meds,"num_doc":doc_stat["tot"],"num_appointement":doc_stat["appoint_count"],"num_visite":doc_stat["visites_sum"]})
