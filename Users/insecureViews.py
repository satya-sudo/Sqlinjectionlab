from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

from .insecureDbUtils import loginQuery,registerQuery
from django.db import connection, transaction
from .models import User

import datetime
# login view 
@csrf_exempt
def login_view(request):

    if request.method == 'POST':

        # Attempt to sign in user 

        username = request.POST["username"] 
        password = request.POST["password"]

        print(username,password)

        users =  User.objects.raw(loginQuery(username,password))
        try:
            user = users[0]
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        except Exception as e :

            # for users with proper hashed password 
            user  = authenticate(request, username=username, password=password)   
            if not user:
                return render(request,"Users/login.html",{ "message":"Invalid username and/or password."})  
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,'Users/login.html')          



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
            cursor = connection.cursor()
            cursor.execute(registerQuery(username,email,firstname,lastname,password,datetime.datetime.now()))
            transaction.commit()
        except IntegrityError:
            return render(request,"Users/register.html",{
            "message": "Sorry,username already taken."
            })       

        # Success!

        return HttpResponseRedirect(reverse("login"))
    else:
        return render(request,"Users/register.html")     

