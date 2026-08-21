from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth

def homefn(request):
    return render(request,'dashboard.html')

# def dashboardfn(request):
#     return render(request,'dashboard.html')

def jobfn(request):
    return render(request,'job.html')

def registerfn(request):
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        e=request.POST['em']
        u=request.POST['uname']
        p1=request.POST['psw1']
        p2=request.POST['psw2']
        if p1==p2:
            if User.objects.filter(username=u).exists():
                return render(request,'register.html',{'er':'username taken'})
            elif User.objects.filter(email=e).exists():
                return render(request,'register.html',{'er':'email taken'})        
            else:
                User.objects.create_user(username=u,email=e,first_name=f,last_name=l,password=p1)
                return redirect('/login/')
        else:
            return render(request,'register.html',{'er':'password not matching'})
    else:
        return render(request,'register.html')

def loginfn(request):
    if request.method=='POST':
        u=request.POST['uname']
        p1=request.POST['psw1']
        x=auth.authenticate(username=u,password=p1)
        if x:
            auth.login(request,x)
            return redirect('/')
        else:
            return render(request,'login.html',{'er':'invalid credentials'})
    else:
        return render(request,'login.html')

