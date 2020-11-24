from django.contrib.auth.decorators import login_required
from django.shortcuts import render , get_object_or_404
from django.contrib.auth.models import User,Group
from django.utils.safestring import mark_safe
import json
from django.http import JsonResponse
from .models import Chat , Message
from analyse.models import Profil ,Medecin , Patient, Analyse
from itertools import chain
from login.service import check_user_group

@login_required
def index(request):
    context = {}
    user = request.user
    context['chats'] = get_chats(user)
    context['username'] = request.user.username
    context['contacts']  = Profil.objects.exclude(user=request.user)

    role = check_user_group(request,['Admin','Doctor','Patient'])
    profil = get_object_or_404(Profil,user=user)
    context['contacts'] = get_contactByRole(profil,role,context['contacts'])

    senders = []
    for c in context['chats']:
        if c.user_to.user == request.user :
            senders.append(c.user_from.user)
        else :
            senders.append(c.user_to.user)

    context['contacts'] = context['contacts'].exclude(user__in = senders).order_by('user__first_name')
    context['add_chat'] = False
    return render(request, 'chat/chat-index.html', context=context)

def get_contactByRole(profil,role,contacts):
    result = None
    #context['role'] = check_user_group(request,['Admin','Doctor','Patient'])
    if role =='Admin':
        result = contacts
    elif role =='Doctor':
        medecin = Medecin.objects.get(id=profil.with_account)
        analyses = Analyse.objects.filter(medecin = medecin)
        patients_ids = list(set([a.patient.id for a in analyses]))
        result = contacts.filter(with_account__in = patients_ids, description='Patient')
    elif role =='Patient':
        patient = Patient.objects.get(id=profil.with_account)
        analyses = Analyse.objects.filter(patient = patient)
        medecin_ids = list(set([a.medecin.id for a in analyses]))
        result = contacts.filter(with_account__in = medecin_ids, description='Doctor')
    return result 
    
def get_chats(user):
    if user is not None:
        profil = get_object_or_404(Profil, user=user)
        chats_userTo = Chat.objects.filter(user_to=profil).order_by('-last_message__timestamp')
        chats_userFrom = profil.chats.order_by('-last_message__timestamp').all()
        chats = list(chain(chats_userTo, chats_userFrom))
        #print(chats)
    else :
        chats = []
    return chats

@login_required
def show_chat_msg(request , id):
    context = {}
    chat = get_object_or_404(Chat, id=id)
    context['messages'] = chat.messages.order_by('timestamp').all()
    context['username'] = request.user.username
    context['chat'] = chat
    context['lastMsg_time'] = chat.last_message.timestamp.strftime("%d.%m.%Y, %H:%M") 
    #print(context['messages'])
    return render(request, 'chat/messages-container.html', context=context)

@login_required
def add_message_json(request):
    #print(request.POST)
    data=request.POST
    #data=json.loads(form)
    chat = get_object_or_404(Chat, id=data['chat_id'])
    profil = get_object_or_404(Profil, user__username=request.user.username)
    msg = Message(sender = profil , content = data['message'])
    msg.save()
    ##
    chat.messages.add(msg)
    chat.last_message = msg
    chat.save()
    ##
    date = msg.timestamp.strftime("%d.%m.%Y, %H:%M") 
    json_data = Message.objects.values().get(id=msg.id)
    return JsonResponse([json_data,date], safe=False)

@login_required
def add_chat(request,id):
    user_to = get_object_or_404(Profil,id=id)
    user_from = get_object_or_404(Profil,user=request.user)
    msg = Message(sender=user_from,content ='')
    msg.save()
    chat = Chat(user_to=user_to,user_from=user_from,last_message=msg)
    chat.save()
    ###

    context = {}
    user = request.user
    context['chats'] = get_chats(user)
    context['username'] = request.user.username
    context['contacts']  = Profil.objects.exclude(user=request.user)

    role = check_user_group(request,['Admin','Doctor','Patient'])
    profil = get_object_or_404(Profil,user=user)
    context['contacts'] = get_contactByRole(profil,role,context['contacts'])
    
    senders = []
    for c in context['chats']:
        if c.user_to.user == request.user :
            senders.append(c.user_from.user)
        else :
            senders.append(c.user_to.user)

    context['contacts'] = context['contacts'].exclude(user__in = senders).order_by('user__first_name')
    context['add_chat'] = chat.id

    return render(request, 'chat/chat-index.html', context=context)


'''
def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Contact, user=user)


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)
'''

'''
def listen_message_json(request):
    data = request.POST
    #print(data)
    chats = get_chats(request.user)

    chats_new =[]
    for c in chats :
        if c.id not in json.loads(data['chats']).keys():
            chats_new.append(c.id)
    
    list_Chat = []
    for chatId in json.loads(data['chats']).keys():
        last_date = Message.objects.get(id=json.loads(data['chats'])[chatId]['last_msgId']).timestamp
        ##
        temp ={}
        temp['chat_id'] = chatId
        temp['message'] = get_last_messages(chatId,last_date,request.user)
        temp['count'] = len(temp['message'])
        if len(temp['message']) !=0 :
            temp['message'] = temp['message'][-1] 
            temp['status'] = True
        else:
            temp['message'] = None 
            temp['status'] = False 

        list_Chat.append(temp)
    
    id_sender = json.loads(data['current_chat'])['last_msgId_sender']
    idChat_current = json.loads(data['current_chat'])['chat_id']
    if  id_sender != '':
        currentChat_date = Message.objects.get(id=id_sender).timestamp
    else :
        currentChat_date = Message.objects.get(id=json.loads(data['chats'])[str(idChat_current)]['last_msgId']).timestamp
    
    current_Chat = {'chat_id':idChat_current}
    current_Chat['message'] = get_last_messages(idChat_current,currentChat_date,request.user,True)

    ### 
    #print(list_Chat , current_Chat )
    return JsonResponse([list_Chat,current_Chat] , safe=False)
    
def get_last_messages(chatId,time,user,sender_only=False):
    chat = get_object_or_404(Chat, id=chatId)
    if not sender_only:
        return list(chat.messages.filter(timestamp__gt=time).values().order_by('timestamp'))
    else:
        res = chat.messages.filter(timestamp__gt=time)
        return list(res.exclude(sender__user = user).values().order_by('timestamp')) 
'''
'''
def get_contact_ajax(request,id):
    result = []
    #if id =='tout' or id== '' :
    contacts = Profil.objects.exclude(user=request.user).values()
    for c in contacts :
        temp = {}
        temp['profil'] = c
        temp['user'] = User.objects.values().get(id=c['user_id'])
        result.append(temp)

    #contacts = Profil.objects.filter(user__first_name__icontains=id).values()  
    return JsonResponse(result , safe=False)
'''

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })