from django.shortcuts import render
from .models import Analyse ,Medecin ,GroupSanguin,Patient , Profil , Staff_Admin
from django.contrib.auth.models import User,Group
import json 
from random import randint , choice
from django.http import JsonResponse
from login.service import check_user_group
from login.views import logout
from django.contrib.auth.decorators import login_required
from whasapp import whatsapp_auth , send_msg
from datetime import date


def random_with_N_digits(l):
    n = choice(l)
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

@login_required
def get_dashboard(request):
    today = date.today()
    #print("Today's date:", today)
    context = {}
    context['analyses']= Analyse.objects.all().order_by('-date_analyse')[:15]
    context['analyses_24h']= len(Analyse.objects.filter(date_analyse=today))
    context['total_analyses']= len(Analyse.objects.all())
    context['total_patients']= len(Patient.objects.all())
    context['total_medecins']= len(Medecin.objects.all())
    return render(request,'analyse/dashboard.html',context=context)

@login_required
def get_analyses(request):
    context = {}
    context['analyses']= Analyse.objects.all().order_by('-date_analyse')
    context['medecins']= Medecin.objects.all().order_by('nom')
    context['grpSanguins'] = GroupSanguin.objects.all().order_by('nom')
    context['patients'] = Patient.objects.all().order_by('nom')
    context['role'] = check_user_group(request,['Admin','Doctor','Patient'])
    return render(request,'analyse/analyses.html',context=context)

@login_required
def get_analyses_patient(request,id):
    context = {}
    patient = Patient.objects.get(id=id)
    context['analyses']= Analyse.objects.filter(patient = patient).order_by('-date_analyse')
    context['role'] = check_user_group(request,['Admin','Doctor','Patient'])
    return render(request,'analyse/analyses.html',context=context)

@login_required
def get_analyses_medecin(request,id):
    context = {}
    medecin = Medecin.objects.get(id=id)
    context['analyses']= Analyse.objects.filter(medecin = medecin).order_by('-date_analyse')
    context['role'] = check_user_group(request,['Admin','Doctor','Patient'])
    return render(request,'analyse/analyses.html',context=context)

def add_analyse(request):
    form=request.POST['data']
    data=json.loads(form)
    ###
    patient = Patient(nom=data['name_nom'],nni=data['name_nni'],tel=data['name_tel'],email=data['name_email'],adresse=data['name_adresse'])
    patient.age = data['name_age'] if data['name_age'] !="" else None
    patient.taille=data['name_taille'] if data['name_taille'] !="" else None
    patient.poids=data['name_poids'] if data['name_poids'] !="" else None
    patient.group_sanguin = GroupSanguin.objects.get(id=data['grpSanguin_id'])
    ###
    patient.user_created = request.user.username
    patient.date_creation = patient.date_modifcation
    patient.save()

    ### compte patient
    patient_group = Group.objects.get(name='Patient') 
    user = User.objects.create_user(username = patient.tel , first_name=patient.nom , password='pswd12345@')
    patient_group.user_set.add(user)
    profil = Profil(user=user , with_account=patient.id, description='Patient')
    profil.save()

    ###
    analyse = Analyse(date_analyse=data['name_date'])
    analyse.user_created = request.user.username
    analyse.date_creation = analyse.date_modifcation 
    analyse.medecin = Medecin.objects.get(id=data['medecin_id'])
    analyse.patient = patient
    analyse.save()

    return get_analyses(request)

def existant_analyse(request):
    form=request.POST['data']
    data=json.loads(form)
    ###
    analyse = Analyse(date_analyse=data['name_date'])
    analyse.user_created = request.user.username
    analyse.date_creation = analyse.date_modifcation 
    analyse.medecin = Medecin.objects.get(id=data['medecin_id'])
    analyse.patient = Patient.objects.get(id=data['patient_id'])
    analyse.save()
    return get_analyses(request)

def edit_analyse(request):
    form=request.POST['data']
    data=json.loads(form)
    ###
    analyse = Analyse.objects.get(id=data['analyse_id'])
    analyse.medecin = Medecin.objects.get(id=data['medecin_id'])
    analyse.patient = Patient.objects.get(id=data['patient_id'])
    analyse.date_analyse = data['name_date']

    analyse.user_modified = request.user.username # !!
    analyse.save()
    return get_analyses(request)

def delete_analyse(request , id):
    analyse = Analyse.objects.get(id=id)
    analyse.delete()
    return get_analyses(request)

#########
@login_required
def get_medecins(request):
    context = {}
    context['medecins']= Medecin.objects.all().order_by('nom')
    context['role'] = check_user_group(request,['Admin','Doctor','Patient'])
    return render(request,'analyse/medecins.html',context=context)

def add_medecin(request):
    form=request.POST['data']
    data=json.loads(form)
    ###
    medecin = Medecin(nom=data['name_nom'],nni=data['name_nni'],tel=data['name_tel'],email=data['name_email'],adresse=data['name_adresse'])
    medecin.specialite = data['name_specialite'] 
    medecin.clinique = data['name_clinique'] 
    ###
    medecin.user_created = request.user.username
    medecin.date_creation = medecin.date_modifcation
    medecin.save()
    
    ###
    medecin_group = Group.objects.get(name='Doctor') 
    #username = 'Medecin'+ str(random_with_N_digits([4,5])).zfill(5)
    user = User.objects.create_user(username = medecin.email , first_name=medecin.nom , password='pswd12345@')
    medecin_group.user_set.add(user)
    profil = Profil(user=user , with_account=medecin.id, description='Doctor')
    profil.save()

    return get_medecins(request)

def edit_medecin(request):
    form=request.POST['data']
    data=json.loads(form)
    ###
    medecin = Medecin.objects.get(id=data['medecin_id'])
    medecin.nom = data['name_nom']
    sync_first_name(medecin , 'Doctor' ,data['name_nom'])
    ##
    medecin.nni = data['name_nni']
    medecin.tel = data['name_tel']
    medecin.email = data['name_email']
    medecin.adresse = data['name_adresse']
    medecin.specialite = data['name_specialite'] 
    medecin.clinique = data['name_clinique'] 
    ###
    medecin.user_modified = request.user.username # !!
    medecin.save()
    return get_medecins(request)

def delete_medecin(request , id):
    profil = Profil.objects.get(with_account=id, description='Doctor')
    user = User.objects.get(id=profil.user.id)
    user.delete()
    ###
    medecin = Medecin.objects.get(id=id)
    medecin.delete()
    return get_medecins(request)


def medecin_user_json(request , id):
    p = Profil.objects.get(with_account=id , description='Doctor')
    user = User.objects.values().get(id=p.user.id)
    return JsonResponse(user, safe=False)

#########
@login_required
def get_patients(request):
    context = {}
    context['patients']= Patient.objects.all().order_by('nom')
    context['grpSanguins'] = GroupSanguin.objects.all().order_by('nom')
    context['role'] = check_user_group(request,['Admin','Doctor','Patient'])
    return render(request,'analyse/patients.html',context=context)

@login_required
def get_patients_medecin(request, id):
    context = {}
    medecin = Medecin.objects.get(id=id)
    analyses = Analyse.objects.filter(medecin = medecin)
    analyse_ids = list(set([a.patient.id for a in analyses]))
    ###
    context['patients']= Patient.objects.filter(id__in = analyse_ids).order_by('nom')
    context['grpSanguins'] = GroupSanguin.objects.all().order_by('nom')
    context['role'] = check_user_group(request,['Admin','Doctor','Patient'])
    return render(request,'analyse/patients.html',context=context)

def add_patient(request):
    form=request.POST['data']
    data=json.loads(form)
    ###
    patient = Patient(nom=data['name_nom'],nni=data['name_nni'],tel=data['name_tel'],email=data['name_email'],adresse=data['name_adresse'])
    patient.age = data['name_age'] if data['name_age'] !="" else None
    patient.taille = data['name_taille'] if data['name_taille'] !="" else None
    patient.poids = data['name_poids'] if data['name_poids'] !="" else None
    patient.group_sanguin = GroupSanguin.objects.get(id=data['grpSanguin_id']) 
    ###
    patient.user_created = request.user.username
    patient.date_creation = patient.date_modifcation
    patient.save()
    
    ###
    patient_group = Group.objects.get(name='Patient') 
    user = User.objects.create_user(username = patient.tel , first_name=patient.nom , password='pswd12345@')
    patient_group.user_set.add(user)
    profil = Profil(user=user , with_account= patient.id , description='Patient')
    profil.save()

    return get_patients(request)

def edit_patient(request):
    form=request.POST['data']
    data=json.loads(form)
    ###
    patient = Patient.objects.get(id=data['patient_id'])
    patient.nom = data['name_nom']
    sync_first_name(patient , 'Patient' ,data['name_nom'])
    ##
    patient.nni = data['name_nni']
    patient.tel = data['name_tel']
    patient.email = data['name_email']
    patient.adresse = data['name_adresse']
    patient.age = data['name_age'] if data['name_age'] !="" else None
    patient.taille = data['name_taille'] if data['name_taille'] !="" else None
    patient.poids = data['name_poids'] if data['name_poids'] !="" else None
    patient.group_sanguin = GroupSanguin.objects.get(id=data['grpSanguin_id'])
    ###
    patient.user_modified = request.user.username # !!
    patient.save()
    return get_patients(request)


def delete_patient(request , id):
    profil = Profil.objects.get(with_account=id,description='Patient')
    user = User.objects.get(id=profil.user.id)
    user.delete()
    ###
    patient = Patient.objects.get(id=id)
    patient.delete()
    return get_patients(request)


def patient_user_json(request , id):
    p = Profil.objects.get(with_account=id,description='Patient')
    user = User.objects.values().get(id=p.user.id)
    return JsonResponse(user, safe=False)
###
@login_required
def get_admin(request):
    context = {}
    context['admins']= Staff_Admin.objects.all().order_by('nom')
    context['role'] = check_user_group(request,['Admin','Doctor','admin'])
    return render(request,'analyse/admins.html',context=context)

def add_admin(request):
    form=request.POST['data']
    data=json.loads(form)
    ###
    admin = Staff_Admin(nom=data['name_nom'],nni=data['name_nni'],tel=data['name_tel'],email=data['name_email'],adresse=data['name_adresse'])
    admin.poste = data['name_poste'] 
    ###
    admin.user_created = request.user.username
    admin.date_creation = admin.date_modifcation
    admin.save()
    
    ###
    admin_group = Group.objects.get(name='Admin') 
    user = User.objects.create_user(username = admin.email , first_name=admin.nom , password='pswd12345@')
    admin_group.user_set.add(user)
    profil = Profil(user=user , with_account=admin.id, description='Admin')
    profil.save()

    return get_admin(request)

def edit_admin(request):
    form=request.POST['data']
    data=json.loads(form)
    ###
    admin = Staff_Admin.objects.get(id=data['admin_id'])
    admin.nom = data['name_nom']
    sync_first_name(admin , 'Admin' ,data['name_nom'])
    ##
    admin.nni = data['name_nni']
    admin.tel = data['name_tel']
    admin.email = data['name_email']
    admin.adresse = data['name_adresse']
    admin.poste = data['name_poste'] 
    ###
    admin.user_modified = request.user.username # !!
    admin.save()
    return get_admin(request)

def delete_admin(request , id):
    profil = Profil.objects.get(with_account=id, description='Admin')
    user = User.objects.get(id=profil.user.id)
    user.delete()
    ###
    admin = Staff_Admin.objects.get(id=id)
    admin.delete()
    return get_admin(request)


def admin_user_json(request , id):
    p = Profil.objects.get(with_account=id , description='Admin')
    user = User.objects.values().get(id=p.user.id)
    return JsonResponse(user, safe=False)

###
@login_required
def get_profil_medecin(request):
    context = {}
    profil = Profil.objects.get(user=request.user)
    medecin = Medecin.objects.get(id=profil.with_account)
    context['medecin'] = medecin
    context['user'] = profil.user
    return render(request,'analyse/profil-medecin.html',context=context)

def check_username_exist(name):
    users = User.objects.all()
    usernames = [u.username for u in users]
    if name in usernames :
        return True
    else:
        return False

def sync_first_name(entity , role , name):
    profil = Profil.objects.get(with_account=entity.id, description=role)
    user = User.objects.get(id=profil.user.id)
    user.first_name = name
    user.save()

def edit_profil_medecin(request):
    form=request.POST['data']
    data=json.loads(form)

    medecin = Medecin.objects.get(id=data['medecin_id'])
    medecin.nom = data['name_nom']
    sync_first_name(medecin , 'Doctor' ,data['name_nom'])
    ##
    medecin.nni = data['name_nni']
    medecin.tel = data['name_tel']
    medecin.email = data['name_email']
    medecin.adresse = data['name_adresse']
    medecin.specialite = data['name_specialite'] 
    medecin.clinique = data['name_clinique'] 
    ###
    medecin.user_modified = request.user.username # !!
    medecin.save()

    ###
    if not check_username_exist(data['name_username']):
        print(' saved new username ...')
        request.user.username = data['name_username']
        request.user.save()
    
    if data['toogle']:
        request.user.set_password(data['name_mdp1'])
        request.user.save()
        logout(request) #!!

    return get_profil_medecin(request)

@login_required
def get_profil_patient(request):
    context = {}
    profil = Profil.objects.get(user=request.user)
    patient = Patient.objects.get(id=profil.with_account)
    context['patient'] = patient
    context['grpSanguins'] = GroupSanguin.objects.all().order_by('nom')
    context['user'] = profil.user
    return render(request,'analyse/profil-patient.html',context=context)

def edit_profil_patient(request):
    form=request.POST['data']
    data=json.loads(form)

    patient = Patient.objects.get(id=data['patient_id'])
    patient.nom = data['name_nom']
    sync_first_name(patient , 'Patient' ,data['name_nom'])
    ##
    patient.nni = data['name_nni']
    patient.tel = data['name_tel']
    patient.email = data['name_email']
    patient.adresse = data['name_adresse']
    patient.age = data['name_age'] if data['name_age'] !="" else None
    patient.taille = data['name_taille'] if data['name_taille'] !="" else None
    patient.poids = data['name_poids'] if data['name_poids'] !="" else None
    patient.group_sanguin = GroupSanguin.objects.get(id=data['grpSanguin_id'])
    ###
    patient.user_modified = request.user.username # !!
    patient.save()

    ###
    if not check_username_exist(data['name_username']):
        print(' saved new username ...')
        request.user.username = data['name_username']
        request.user.save()
    
    if data['toogle']:
        request.user.set_password(data['name_mdp1'])
        request.user.save()
        logout(request) #!!

    return get_profil_patient(request)

###
@login_required
def get_profil_admin(request):
    context = {}
    profil = Profil.objects.get(user=request.user)
    admin = Staff_Admin.objects.get(id=profil.with_account)
    context['admin'] = admin
    context['user'] = profil.user
    return render(request,'analyse/profil-admin.html',context=context)


def edit_profil_admin(request):
    form=request.POST['data']
    data=json.loads(form)

    admin = Staff_Admin.objects.get(id=data['admin_id'])
    admin.nom = data['name_nom']
    sync_first_name(admin , 'Admin' ,data['name_nom'])
    ##
    admin.nni = data['name_nni']
    admin.tel = data['name_tel']
    admin.email = data['name_email']
    admin.adresse = data['name_adresse']
    admin.poste = data['name_poste'] 
    ###
    admin.user_modified = request.user.username # !!
    admin.save()

    ###
    if not check_username_exist(data['name_username']):
        print(' saved new username ...')
        request.user.username = data['name_username']
        request.user.save()
    
    if data['toogle']:
        request.user.set_password(data['name_mdp1'])
        request.user.save()
        logout(request) #!!

    return get_profil_admin(request)

###
def get_send_analyse(request):
    context={}
    context['analyses'] = Analyse.objects.exclude(patient__tel__exact='')
    context['analyses'] = context['analyses'].exclude(analyse_pdf__exact='').order_by('-date_analyse')
    return render(request,'analyse/send_analyse.html',context=context)

def json_patient(request,id):
    analyse = Analyse.objects.values().get(id=id)
    patient = Patient.objects.values().get(id=analyse['patient_id'])
    return JsonResponse([analyse,patient], safe=False)

def sent_analyse(request):
    context={}
    form=request.POST['data']
    data=json.loads(form)
    client =  whatsapp_auth('AC02a1bc09a2a167a3db1a9340467e5e8f','3511f2a0a22f1025d567927bc45e331b') 
    
    analyses = Analyse.objects.filter(id__in = data['data'])
    success_sent = []
    failed_sent = []
    for a in analyses :
        msg = send_msg(client,a.patient.tel,data['link']+'media/'+a.analyse_pdf.name)
        if not msg :
            failed_sent.append(a)
        else :
            success_sent.append(a)
    
    context['success_sent'] = success_sent
    context['failed_sent'] = failed_sent
    context['total_success'] = len(success_sent)
    context['total_failed'] = len(failed_sent)
    context['total_send'] = len(analyses)
    return render(request,'analyse/send_analyse_notif.html',context=context)