from django.shortcuts import render
from chat.models import MessageModel
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def chat(request):
	return render(request,"chat/chats.html",{})
@require_POST
@csrf_exempt
def send_message(request):
	sender=request.POST["sender"]
	to=request.POST["to"]
	message=request.POST["message"]
	msg=MessageModel(sender=sender,to=to,msg=body)
	msg.save()

