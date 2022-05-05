from django.http import HttpResponse
from django.shortcuts import redirect

def check_login(f):
	def wrapper(request,*args,**kwargs):
		d={"patient":1,"medecin":2,"pharmacist":3}
		if request.user.is_authenticated:
			role=request.session["role"]
			return redirect('landing:redirect',loginp=d[role])
		else:
			return f(request,*args,**kwargs)
		
	return wrapper


def check_doctor(f):
	def wrapper(request,*args,**kwargs):
		d={"patient":1,"medecin":2,"pharmacist":3}
		role=request.session["role"]
		if role =="doctor": 
			return f(request,*args,**kwargs)
		else:
			return redirect('landing:redirect',loginp=d[role])
		
	return wrapper

def check_pharmacist(f):
	def wrapper(request,*args,**kwargs):
		d={"patient":1,"medecin":2,"pharmacist":3}
		role=request.session["role"]
		if role =="pharmacist": 
			return f(request,*args,**kwargs)
		else:
			return redirect('landing:redirect',loginp=d[role])
		
	return wrapper