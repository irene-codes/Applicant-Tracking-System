from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.forms import modelformset_factory

@login_required(login_url='/login')
def homefn(request):
    return render(request,'dashboard.html')

# def dashboardfn(request):
#     return render(request,'dashboard.html')
@login_required(login_url='/login')
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
            return render(request,'register.html',{'er':'Password not matching.'})
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
@login_required(login_url='/login')
def addfn(request):
    resume,_=Resume.objects.get_or_create(user=request.user)
    if request.method=='POST':
        form=ResumeForm(request.POST,instance=resume)
        if form.is_valid():
            form.save()

            #One-sentence summary: instance=resume isn't only "pre-fill with old data" — 
            # its real, constant job in both branches is "keep this form permanently tied to this exact one row," 
            # which matters every single time, not just when there's existing data to show.
    else:
        form=ResumeForm(instance=resume)
    return render(request,'addresume.html',{'form':form})


def logoutfn(request):
    auth.logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def experiancefn(request):
    
    # exp is a local variable holding one single row from the experiance table — specifically, the row that belongs to request.user
    exp,_=experiance.objects.get_or_create(user=request.user)
    if request.method=='POST':
        form=ExperianceForm(request.POST,instance=exp)
        if form.is_valid():
            form.save()
    else:
        form=ExperianceForm(instance=exp)
    return render(request,'experiance.html',{'form':form})


@login_required(login_url='/login')
def educationfn(request):
    edu,_=education.objects.get_or_create(user=request.user)
    if request.method=='POST':
        form=EducationForm(request.POST,instance=edu)
        if form.is_valid():
            form.save()
    else:
        form=EducationForm(instance=edu)
    return render(request,'education.html',{'form':form})

def skillfn(request):
    
    skill_set=modelformset_factory(Skills,exclude=['user'],extra=3,can_delete=True)
    #The result, skill_set, isn't a formset itself yet — it's a formset class, a blueprint you still need to actually "instantiate" (create a real usable version of) in the next lines.
    qs = Skills.objects.filter(user=request.user)
    #This fetches all existing Skills rows belonging to the current logged-in user — could be zero rows (new user), or several
    if request.method=='POST':
        formset=skill_set(request.POST,queryset=qs)
        #It tells the formset "these are the existing objects to edit." Django looks at how many rows are in qs and pre-fills that many forms with the existing data (one form per existing Skills row), then adds extra=3 blank forms on top for new entries. It's about which rows get loaded for editing, not about writing anything to the user column.
        if formset.is_valid():
            formset.save()
    else:
        formset=skill_set(queryset=qs)
    return render(request,'skills.html',{'formset':formset})
   
#instance=expects exactly one database row
#queryset=expects a collection of rows

def summaryfn(request):
    return render(request,'summary.html')

def interestfn(request):
    return render(request,'interest.html')