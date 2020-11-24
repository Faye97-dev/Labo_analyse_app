from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from analyse.models import Analyse , Profil
from .service import first_link , check_user_group

def login_form(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/app')
        else :
            print(' Recupeuration de la page login ')
            return render(request,'login/login.html',context={'message':False})
    if request.method =='POST':
        #print('get2')
        username = request.POST['username']
        password = request.POST['password']
        #print(username)
        user = authenticate(request, username=username, password=password)
        #print(user)
        if user is not None:
            print('Login reussi !')
            login(request, user)
            return redirect('/app')
        else:
            print('Login echec !')
            return render(request,'login/login.html',context={'message':True}) 

    return render(request,'login/login.html',context={'message':False})

def login_redirect_form(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/app')
        else :
            print(' Recupeuration de la page login ')
            return render(request,'login/login_redirect.html',context={'message':False})

    return render(request,'login/login_redirect.html',context={'message':False})

def logout_view(request):
    logout(request)
    return redirect('/login')

def index(request):
    
    if not request.user.is_authenticated:
        return redirect('/login')

    # change image of car
    user = request.user 
    print(user.last_login,user.username,user.is_superuser)
    context={}
    context['date_login'] = user.last_login.strftime("%d/%m/%Y, %H:%M:%S")
    context['username'] = user.username
    context['first_name'] = user.first_name
    context['role'] = check_user_group(request,['Admin','Doctor','Patient'])
    #context['is_superuser'] = user.is_superuser
    print(context)

    if request.method == 'POST':
        id_pdf = request.POST['name_id']
        if request.FILES != {} :
            analyse = Analyse.objects.get(id=id_pdf)
            print(request.FILES['name_pdf'].name ,id_pdf)
            ###
            myfile = request.FILES['name_pdf']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            #uploaded_file_url = fs.url(filename)
            analyse.analyse_pdf.name = filename
            print(analyse.analyse_pdf.path)
            analyse.save()
        print('Not selected analyse pdf  ... ')
        ##
        if context['role'] == 'Doctor' or context['role'] == 'Patient':
            profil = Profil.objects.get(user=request.user)
            context['first_link'] = first_link(context['role'],True)
            context['with_account']= profil.with_account
        else :
            context['first_link'] = first_link(context['role'],True)
           
        return render(request,'index.html',context=context)
    else:
        if context['role'] == 'Doctor' or context['role'] == 'Patient':
            profil = Profil.objects.get(user=request.user)
            context['first_link'] = first_link(context['role'],False)
            context['with_account']= profil.with_account
        else :
            context['first_link'] = first_link(context['role'],False)
            
        return render(request,'index.html',context=context)

def home(request):
    return render(request,'home.html')
