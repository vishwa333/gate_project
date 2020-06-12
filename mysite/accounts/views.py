from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from .models import my_user
# Create your views here.
def signup(request):
    if(request.method == 'POST'):
        fname = request.POST['fname']
        lname = request.POST["lname"]
        email = request.POST["email"]
        password = request.POST["pass"]
        #u1 = auth.authenticate(username=mail,password=password)
        try:
            u1 = my_user.objects.get(email=email)
            #print("success")
            return render(request, 'signup_fail.html')
        except:
            u1 = my_user()
            u1.fname = fname
            u1.lname = lname
            u1.email = email
            u1.set_password(password)
            u1.save()
            return render(request,"success.html")
    else:
        return render(request,'signup.html')

def login(request):
    if (request.method == 'POST'):
        email = request.POST["email"]
        password = request.POST["pass"]
        u1 = auth.authenticate(username=email,password=password)
        if(u1!= None):
            auth.login(request, u1)
            return redirect("/")
        else:
            return render(request, 'login.html')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')