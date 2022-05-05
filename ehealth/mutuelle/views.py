from django.shortcuts import render
from django.db.models.aggregates import Count
from .models import AllMutuelle
from django.db.models import Q    
from patient.decorators import check_patient
from django.contrib.auth.decorators import login_required

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
