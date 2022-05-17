from django.shortcuts import render

def chat(request,pk):
	return render(request,"chat/chats.html",{})
