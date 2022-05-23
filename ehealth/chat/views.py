from django.shortcuts import render
from chat.models import Message
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.db.models.aggregates import Count
from django.db.models import Case,When,Value
from landing.models import Person
import json
import datetime
def chats(request):
	chats=Message.objects.filter(Q(sender=request.user.person) | Q(to=request.user.person)).annotate(unread=Count("seen",filter=Q(seen=False)),
		holder=Case(
			When(sender_id=request.user.person,then=1),

			When(to_id=request.user.person,then=0)
		))
	
		
	return render(request,"chat/chats.html",{"chat":True,"chats":chats,})
def chat(request,pk):

	other=Person.objects.get(pk=pk)
	chats=Message.objects.filter(Q(sender=request.user.person) | Q(to=request.user.person)).annotate(unread=Count("seen",filter=Q(seen=False)),
		holder=Case(
			When(sender_id=request.user.person,then=1),

			When(to_id=request.user.person,then=0)
		))
	messages=Message.objects.filter(Q(sender=request.user.person) & Q(to=other)  | Q(sender=other) & Q(to=request.user.person)).annotate(unread=Count("seen",filter=Q(seen=False)),
		holder=Case(
			When(sender_id=request.user.person,then=1),

			When(to_id=request.user.person,then=0)
		)).order_by("timestamp")
		
	return render(request,"chat/chats.html",{"chat":True,'other':other,"chats":chats,"messages":messages})
@require_POST
@csrf_exempt
def send_message(request):
	body=json.loads(request.body)
	sender=body["sender"]
	to=body["to"]
	message=rbody["message"]
	msg=Message(sender=sender,to=to,msg=body)
	msg.save()
def fetch(request,pk):
	other=Person.objects.get(pk=pk)
	messages=Message.objects.filter(Q(sender=request.user.person) & Q(to=other)  | Q(sender=other) & Q(to=request.user.person)).annotate(unread=Count("seen",filter=Q(seen=False)),
		holder=Case(
			When(sender_id=request.user.person,then=1),

			When(to_id=request.user.person,then=0)
		)).order_by("timestamp")[:15]
	messages = list(messages.values())
	return JsonResponse(messages,safe=False)
	


