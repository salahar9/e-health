from django.shortcuts import render
from chat.models import MessageModel
def chat(request,pk):
	return render(request,"chat/chats.html",{})
@require_POST
@csrf_exempt
def send_message(request):
	sender=request.POST["sender"]
	to=request.POST["to"]
	message=request.POST["message"]
	msg=MessageModel(sender=sender,to=to,msg=body)
	msg.save()

