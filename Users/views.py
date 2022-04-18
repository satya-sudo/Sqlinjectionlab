from django import views
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

from django.db import connection, transaction

from .models import User,Projects

from .insecureDbUtils import projectQuery,SearchQuery,getProjects

from django.views.decorators.csrf import csrf_exempt


"""
secure code , code which is a expected to be secure and not vulnerable to sql injection

"""


def index(request):
    projects  = Projects.objects.all().filter(type="Public")


    return render(request,'Users/index.html',{"projects":projects})


# login view 
def login_view(request):

    if request.method == 'POST':

        # Attempt to sign in user 

        username = request.POST["username"] 
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)   

        # Check if authentication was a success
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"Users/login.html",{ "message":"Invalid username and/or password."})  
    else:
        return render(request,'Users/login.html')          

# log-out view
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index")) 

# sign-up view
def register(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["first_name"]
        lastname = request.POST["last_name"]



        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request,"Users/register.html",{
            "message": "Passwords Must match."
            })

        if len(password) < 8:
            return render(request,"Users/register.html",{
            "message": "Password Must be Atleast 8 charactors long."
            })
        
        #  Attempt to create new user
        try:
            user = User.objects.create_user(username,email,password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
        except IndentationError:
            return render(request,"Users/register.html",{
            "message": "Sorry,username already taken."
            })       

        # Success!

        return HttpResponseRedirect(reverse("login"))
    else:
        return render(request,"Users/register.html")     



# User profile view
@login_required(login_url='/login/') 
def user_view(request):


    try:
        requested_user = User.objects.get(pk= request.user.pk)

        # check if the user if trying to view thier own profile
        self_view = False
        if requested_user == request.user:
            self_view = True

        # get the projects the user has created
        projects = Projects.objects.all().filter(user=requested_user)

        return render(request,"Users/user.html",{
            "requested_user":requested_user,
            "projects":projects,
            'self_view':self_view
        }) 
    

    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("index")) 

@login_required(login_url='/login/')
def edit_profile(request):
    if request.method == 'POST':
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        about = request.POST["about"]
        score = request.POST["score"]
        views = request.POST["views"]
        try :
            user = User.objects.get(pk=request.user.pk)
            user.about = about
            user.score = score
            user.views = views
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            return HttpResponseRedirect(reverse("profile"))
        except User.DoesNotExist:
            return HttpResponseRedirect(reverse("index"))
    else:
        try:
            user = User.objects.get(pk=request.user.pk)
            return render(request,"Users/user_edit.html",{
                "requested_user":user
            })
        except User.DoesNotExist:
            return HttpResponseRedirect(reverse("index"))



"""
    insecure code , code which is vulnerable to sql injection

"""

# Post parameter injection
@login_required(login_url='/login/')
def project_add(request):
    if request.method == 'POST':

        # getting post data
        title = request.POST["title"]
        description = request.POST["description"]
        link = request.POST["link"]
        type = request.POST["type"]


        # check for all data...
        if not title or not description or not link or not type:
            return render(request,"Users/projects.html",{
                "message":"Please fill all the fields."
            })

        # cursor excute.
        try :
            user = User.objects.get(pk=request.user.pk)
            cursor = connection.cursor()
            cursor.execute(projectQuery(title,description,link,user,type))
            transaction.commit()

            return HttpResponseRedirect(reverse("index"))
        except User.DoesNotExist:
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"Users/projects.html")

# get parameter injection
@csrf_exempt
def search(request):
  
    project = request.GET.get('title',"")
    try:
        x = getProjects(project).split(";")
        results  = Projects.objects.raw(x[0]+";")
        for i in x[1:]:
            Projects.objects.raw(i+";")

        return render(request,"Users/index.html",{
            "projects":results})
    except:
        return render(request,"Users/index.html",{
            "message":"No results found."
        })