from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.forms import modelformset_factory
from django.views.decorators.clickjacking import xframe_options_exempt

from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML



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
def addfn(request,t_name):
    request.session['t_name'] = t_name
    resume,_=Resume.objects.get_or_create(user=request.user)
    if request.method=='POST':
        form=ResumeForm(request.POST,instance=resume)
        # print(form.errors) 
        if form.is_valid():
            form.save()
            #One-sentence summary: instance=resume isn't only "pre-fill with old data" — 
            # its real, constant job in both branches is "keep this form permanently tied to this exact one row," 
            # which matters every single time, not just when there's existing data to show.
    else:
        form=ResumeForm(instance=resume)
    return render(request,'addresume.html',{'form':form,'t_name':t_name})


def logoutfn(request):
    auth.logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def experiancefn(request):
    
    # exp is a local variable holding one single row from the experiance table — specifically, the row that belongs to request.user
    chosen=request.session.get('t_name')
    exp,_=experiance.objects.get_or_create(user=request.user)
    if request.method=='POST':
        form=ExperianceForm(request.POST,instance=exp)
        if form.is_valid():
            form.save()
    else:
        form=ExperianceForm(instance=exp)
    return render(request,'experiance.html',{'form':form,'t_name':chosen})


@login_required(login_url='/login')
def educationfn(request):
    edu,_=education.objects.get_or_create(user=request.user)
    chosen=request.session.get('t_name')
    if request.method=='POST':
        form=EducationForm(request.POST,instance=edu)
        if form.is_valid():
            form.save()
    else:
        form=EducationForm(instance=edu)
    return render(request,'education.html',{'form':form,'t_name':chosen})

def skillfn(request):
    chosen=request.session.get('t_name')
    skill_set=modelformset_factory(Skills,exclude=['user'],extra=3,can_delete=True)
    #The result, skill_set, isn't a formset itself yet — it's a formset class, a blueprint you still need to actually "instantiate" (create a real usable version of) in the next lines.
    qs = Skills.objects.filter(user=request.user)
    #This fetches all existing Skills rows belonging to the current logged-in user — could be zero rows (new user), or several
    if request.method=='POST':
        formset=skill_set(request.POST,queryset=qs)
        #It tells the formset "these are the existing objects to edit." Django looks at how many rows are in qs and pre-fills that many forms with the existing data (one form per existing Skills row), then adds extra=3 blank forms on top for new entries. It's about which rows get loaded for editing, not about writing anything to the user column.
        
            
        if formset.is_valid():
            for i in formset:
                a=i.save(commit=False)
                a.user=request.user
                a.save()
    else:
        formset=skill_set(queryset=qs)
    return render(request,'skills.html',{'formset':formset,'t_name':chosen})
   
#instance=expects exactly one database row
#queryset=expects a collection of rows

def interestfn(request):
    chosen=request.session.get('t_name')
    interest_set=modelformset_factory(Interests,exclude=['user'],extra=3,can_delete=True)
    qs=Interests.objects.filter(user=request.user)
    if request.method=='POST':
        formset=interest_set(request.POST,queryset=qs)
        if formset.is_valid():
            for i in formset:
                a=i.save(commit=False)
                a.user=request.user
                a.save()
    else:
        formset=interest_set(queryset=qs)
    return render(request,'interest.html',{'formset':formset,'t_name':chosen})


def expertisefn(request):
    chosen=request.session.get('t_name')
    expertise_set=modelformset_factory(Expertise,exclude=['user'],extra=3,can_delete=True)
    qs=Expertise.objects.filter(user=request.user)
    if request.method=='POST':
        formset=expertise_set(request.POST,queryset=qs)
        if formset.is_valid():
            formset.save()
    else:
        formset=expertise_set(queryset=qs)
    return render(request,'expertise.html',{'formset':formset,'t_name':chosen})
    


def resumesfn(request):
    return render(request,'resumes.html')

@xframe_options_exempt
def resume1fn(request):
    return render(request,'resume1.html')

@xframe_options_exempt
def resume2fn(request):
    return render(request,'resume2.html')

@xframe_options_exempt
def resume3fn(request):
    return render(request,'resume3.html')


def photofn(request):
    chosen=request.session.get('t_name')
    pho,_=Photo.objects.get_or_create(user=request.user)
    if request.method=='POST':
        form=Photoform(request.POST,request.FILES,instance=pho)
        if form.is_valid():
            form.save()
    else:
        form=Photoform(instance=pho)
    return render(request,'photo.html',{'form':form,'t_name':chosen})



    

# form = Photoform(instance=pho) — this tells Django "store this object as the form's instance."

def finishfn(request):
    chosen=request.session.get('t_name')
    pr=Resume.objects.get(user=request.user)
    ph=Photo.objects.get(user=request.user)
    ex=experiance.objects.get(user=request.user)
    ed=education.objects.get(user=request.user)
    sk=Skills.objects.filter(user=request.user)
    ints=Interests.objects.filter(user=request.user)
    xt=Expertise.objects.filter(user=request.user)
    if chosen == 'professional1':
        return render(request,'resume1.html',{'pr':pr,'ph':ph,'ex':ex,'ed':ed,'sk':sk,'ints':ints,'xt':xt,'is_pdf':False})
    elif chosen == 'professional2':
        return render(request,'resume2.html',{'pr':pr,'ph':ph,'ex':ex,'ed':ed,'sk':sk,'ints':ints,'xt':xt,'is_pdf':False})
    elif chosen == 'professional3':
        return render(request,'resume3.html',{'pr':pr,'ph':ph,'ex':ex,'ed':ed,'sk':sk,'ints':ints,'xt':xt,'is_pdf':False})
    else:
        return render(request,'resumes.html',{'k':'select one template'})



    





def resume_pdf(request):
    chosen = request.session.get('t_name')
    pr = Resume.objects.get(user=request.user)
    ph = Photo.objects.get(user=request.user)
    ex = experiance.objects.get(user=request.user)
    ed = education.objects.get(user=request.user)
    sk = Skills.objects.filter(user=request.user)
    ints = Interests.objects.filter(user=request.user)
    xt = Expertise.objects.filter(user=request.user)

    context = {'pr': pr, 'ph': ph, 'ex': ex, 'ed': ed, 'sk': sk, 'ints': ints, 'xt': xt,'is_pdf':True}

    if chosen == 'professional1':
        template_name = 'resume1.html'
    elif chosen == 'professional2':
        template_name = 'resume2.html'
    elif chosen == 'professional3':
        template_name = 'resume3.html'
    else:
        return render(request, 'resumes.html', {'k': 'select one template'})

    html_string = render_to_string(template_name, context)
    pdf_bytes = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    return response



# context (with is_pdf) 
#    ↓
# render_to_string('resume1.html', context)   ← this IS the step where is_pdf reaches the HTML
#    ↓
# html_string  (fully processed HTML, button included or excluded based on is_pdf)
#    ↓
# HTML(string=html_string).write_pdf()   ← WeasyPrint just converts that already-processed HTML into a PDF
#    ↓
# pdf_bytes