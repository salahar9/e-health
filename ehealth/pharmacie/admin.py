from django.contrib import admin
from pharmacie.models import Pharmacie,Visite

class PharmacieAdmin(admin.ModelAdmin):
    list_display = ("INP",'nom',"ville","activated")
class PharmacieVisiteAdmin(admin.ModelAdmin):
    list_display = ("pharma_id",'patient_id',"date_created")
    
admin.site.register(Pharmacie, PharmacieAdmin) 
admin.site.register(Visite, PharmacieVisiteAdmin)
