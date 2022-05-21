from django.shortcuts import render
from chat.models import Message
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.db.models.aggregates import Count
from django.db.models import Case,When,Value
from landing.models import Person
def chats(request,pk):
	other=Patient.objects.get(pk=pk)
	chats=Message.objects.filter(Q(sender=request.user.person) | Q(to=request.user.person)).annotate(unread=Count("seen",filter=Q(seen=False)),
		holder=Case(
			When(sender_id=request.user.person,then=1),

			When(to_id=request.user.person,then=0)
		))
	
		
	return render(request,"chat/chats.html",{"chats":chats,})
def chat(request,pk):
	other=Patient.objects.get(pk=pk)
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
		
	return render(request,"chat/chats.html",{"chats":chats,"messages":messages})
@require_POST
@csrf_exempt
def send_message(request):
	sender=request.POST["sender"]
	to=request.POST["to"]
	message=request.POST["message"]
	msg=Message(sender=sender,to=to,msg=body)
	msg.save()

