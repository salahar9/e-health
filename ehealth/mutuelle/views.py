from django.shortcuts import render
from django.db.models.aggregates import Count,Sum
from .models import AllMutuelle
from django.db.models import Q    
from patient.decorators import check_patient
from django.contrib.auth.decorators import login_required
from doctor.models import Visite
from ordonnance.models import Ordonnance
@check_patient
@login_required
def all_mutuelles(request):
    query_set = AllMutuelle.objects.filter(visite_id__patient_id=request.user.person.patient.id)
    total = query_set.aggregate(total=Count("id",distinct=True),pending=Count('id',filter=Q(mutuelle_status__exact="P"),distinct=True),complete=Count('id',filter=Q(mutuelle_status__exact="C"),distinct=True))
   
    return render(request, 'mutuelle/all_mutuelles.html', { 'all_mutuelles': True, 'mutuelles': query_set, 'total_mutuelles': total['total'], 'pending': total['pending'], 'complete': total['complete']})
def get_other_mut(request,pk):
    query_set = AllMutuelle.objects.filter(visite_id__patient_id=pk)
    total = query_set.aggregate(total=Count("id",distinct=True),pending=Count('id',filter=Q(mutuelle_status__exact="P"),distinct=True),complete=Count('id',filter=Q(mutuelle_status__exact="C"),distinct=True))

    return render(request, 'mutuelle/all_mutuelles.html', { 'all_mutuelles': True, 'mutuelles': query_set, 'total_mutuelles': total['total'], 'pending': total['pending'], 'complete': total['complete']})
def add_mutuelle(request):
    pat=request.user.person.patient
    visite=Visite.objects.filter(patient_id=pat).annotate(tot=Sum("ordonnance__price")).filter(tot__gt=0)
    return render(request,'mutuelle/add_mutuelle.html',{"visites":visite})
