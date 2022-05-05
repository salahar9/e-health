from django.http import HttpResponse
from django.shortcuts import redirect
def check_doctor(f):
	def wrapper(request,*args,**kwargs):
		d={"patient":1,"medecin":2,"pharmacist":3}
		role=request.session["role"]
		if role =="medecin": 
			return f(request,*args,**kwargs)
		else:
			return redirect('landing:redirect',loginp=d[role])
		
	return wrapper
def check_activated(f):
	def wrapper(request,*args,**kwargs):
		doctor=request.user.person.doctor
		if doctor.activated:
			return f(request,*args,**kwargs)
		else:
			return redirect('doctor:register')
	return wrapper
