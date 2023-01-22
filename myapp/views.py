from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from . import models

def form_page(request):
    return render(request,'index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0 :
        for key,value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        if request.method == "POST":
            Register(request)
        return redirect('/')

def login(request):
    # models.create_team(teamname="Real Madrid",teamicon="No Icon",teamcountry="Spain")
    # models.create_team(teamname="FC Barcelona",teamicon="No Icon",teamcountry="Spain")
    # models.create_team(teamname="MAN CITY",teamicon="No Icon",teamcountry="England")
    # models.create_team(teamname="PSG",teamicon="No Icon",teamcountry="France")
    # models.create_team(teamname="PORTO F.C",teamicon="No Icon",teamcountry="Portugal")

    if request.method == "POST":
        if Login(request):
            id = request.session['userid'] 
            user = User.objects.get(id=id)
            context = {
                'user' : user,
                'teams' : models.Teams.objects.all()
            }
            return render(request,'result.html',context)

    return redirect('/')


def allusers(request):  
    context = {
        'users': models.get_all_users()
    }
    return render(request, 'all_users.html', context)


def addteam(request):
    id = request.session['userid'] 
    
    models.add_fav(id,request.POST['select_team'])
    return redirect('/login')

def edit(request,id):  

        user = models.get_user_by_id(id)
        
        context = {
            'id':id,
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'email' : user.email,
        
        }
        return render(request,"edit_sh.html",context)


def editshow(request,id):  
    users=request.POST
    users=models.update_user(id,users['first_name'],users['last_name'],users['email'])
    return redirect('/login')

def delete(request,id):   
        models.delete_user(id)
        return redirect('/allusers')