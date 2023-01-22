import re
from django.db import models 
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        error = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        password_regex =re.compile(r'^[a-zA-Z0-9.+_-]')
        special_symbols = ['$','@','#','%','^','&']
        if len(postData['first_name']) < 3 :
            error['first_name'] = "first name should be at least 3 characters"
        if len(postData['last_name']) < 3 :
            error['last_name'] = "last name should be at least 3 characters"
        if not email_regex.match(postData['email']) :
            error['email'] = "invaild email"
        if len(postData['password']) < 6:
            error['password_less_than'] = "Password must have atleast 6 characters"
        if len(postData['password']) > 20 :
            error['password_grather_than'] = "'Password cannot have more than 20 characters"
        if not any(characters.isupper() for characters in postData['password']):
            error['password_notInclude_upper'] = "Password must have at least one uppercase character"
        if not any(characters.islower() for characters in postData['password']):
            error['password_notInclude_lower'] = "Password must have at least one lowercase character"
        if not any(characters.isdigit() for characters in postData['password']):
            error['password_notInclude_number'] = "Password must have at least one numeric character."
        if not any(characters in special_symbols for characters in postData['password']):
            error['password_symbol'] = "Password should have at least one of the symbols $@#%^&"
        
        return error

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = UserManager()




class Teams(models.Model):
    teamname = models.CharField(max_length=255)
    teamicon = models.CharField(max_length=255)
    teamcountry = models.CharField(max_length=255)
    user = models.ManyToManyField(User, related_name="teams")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



def Register(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
    if (request.POST['confirm_password'] == password):
        return User.objects.create(first_name = first_name , last_name = last_name, email = email , password = pw_hash )

def Login(request):
    user = User.objects.filter(email = request.POST['email'])
    if user:
        loged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), loged_user.password.encode()):
            request.session['userid'] = loged_user.id
            return True
        

def create_user(first_name,last_name,email):
    return User.objects.create(first_name=first_name,last_name=last_name,email=email)


def get_all_users():
    return User.objects.all()


def get_user_by_id(id):
    return User.objects.get(id=id)



def delete_user(id):
    return User.objects.get(id=id).delete()


def update_user(id, first_name, last_name, email):
    user = User.objects.get(id=id)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.save()


def add_fav(user_id,team_id):
    
    print(id)
    this_user = User.objects.get(id =user_id )
    this_team = Teams.objects.get(id=team_id)
    print(this_team)
    this_user.teams.add(this_team)
   


def create_team(teamname,teamicon,teamcountry):
    Teams.objects.create(teamname=teamname,teamicon=teamicon,teamcountry=teamcountry)