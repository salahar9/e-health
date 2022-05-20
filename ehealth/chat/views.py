from django.shortcuts import render
from chat.models import Message
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.db.models.aggregates import Count

def chat(request):
	chats=Message.objects.filter(Q(sender=request.user.person) | Q(to=request.user.person)).order_by("-timestamp").distinct("sender","to").annotate("unread"=Count("Seen",filter(Q(seen==False))))
	return render(request,"chat/chats.html",{"chats":chats})
@require_POST
@csrf_exempt
def send_message(request):
	sender=request.POST["sender"]
	to=request.POST["to"]
	message=request.POST["message"]
	msg=Message(sender=sender,to=to,msg=body)
	msg.save()

