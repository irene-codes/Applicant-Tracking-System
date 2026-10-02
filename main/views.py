from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.forms import modelformset_factory
from django.views.decorators.clickjacking import xframe_options_exempt

from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST


@login_required(login_url='/login')
def homefn(request):
    return render(request,'home.html')


def editfn(request,e_id):
    job=Job.objects.get(id=e_id)
    if job.posted_by == request.user:
        if request.method == 'GET':
            form=Jobform(instance=job)
            return render(request,'jobinterviewer.html',{'form':form})
        else:
            form=Jobform(request.POST,instance=job)
            if form.is_valid():
                
                form.save()
                for application in Application.objects.filter(job=job):
                    match_percentage, recommended=calculate_score(application.applicant_id, job)
                    application.match_score=match_percentage
                    application.recommended=recommended
                    application.save()
                


                return redirect('/jobsearch/')
            else:
                return render(request,'jobinterviewer.html',{'form':form})
    else:
        return redirect('/jobs/')



@login_required(login_url='/login')
def jobfn(request):
    role=Usercat.objects.get(user=request.user).role
    if role == 'applicant':
        jobs=Job.objects.all()
        return render(request,'jobapplicant.html',{'job':jobs})
    else:    
        if request.method=='POST':
            form=Jobform(request.POST)   

            if form.is_valid():
                new_job=form.save(commit=False)
                new_job.posted_by=request.user
                new_job.save()
                return redirect('/jobsearch/')
        else:
            form=Jobform()
    return render(request,'jobinterviewer.html',{'form':form})


# Creating something new — you just do form = Photoform(request.POST), and submitting it creates a brand new row in the database.
# Editing something that already exists — you do form = Photoform(request.POST, instance=existing_object), which tells Django: "don't create a new row — take this specific existing row (existing_object) and update its fields with whatever was submitted."



def registerfn(request):
    if 'applicant' in request.path:
        if request.method=='POST':    
            u=UserForm(request.POST)
            p=ApplicantForm(request.POST)
            if u.is_valid() and p.is_valid():            
                a=u.save(commit=False)
                a.set_password(u.cleaned_data['password'])
                a.save()
                b=p.save(commit=False)
                b.user=a
                b.save()
                return redirect('/login/')
        else:
            u=UserForm()
            p=ApplicantForm()
        return render(request,'registerapplicant.html',{'u':u,'p':p})

    elif 'interviewer' in request.path:
        if request.method=='POST':
            u=UserForm(request.POST)
            p=InterviewerForm(request.POST)
            if u.is_valid() and p.is_valid():            
                a=u.save(commit=False)
                a.set_password(u.cleaned_data['password'])
                a.save()
                b=p.save(commit=False)
                b.user=a
                b.save()
                return redirect('/login/')    
        else:
            u=UserForm()
            p=InterviewerForm()
        return render(request,'registerinterviewer.html',{'u':u,'p':p})


def loginfn(request):   
    if request.method=='POST':
        u=request.POST['uname']
        p1=request.POST['psw1']
        x=auth.authenticate(username=u,password=p1)
        if x:
            auth.login(request,x)
            Usercat.objects.get_or_create(user=request.user,defaults={ 'role':request.POST.get('role')})
            return redirect('/')

            
        else:
            return render(request,'login.html',{'er':'invalid credentials'})
    else:
        # role = request.GET.get('role')
        return render(request,'login.html')




@login_required(login_url='/login')
def addfn(request,t_name):
    request.session['t_name'] = t_name
    resume,_=Resume.objects.get_or_create(user=request.user)
    missing_details = (
        resume_details_missing(resume)
        if request.session.get('pending_application') else []
    )
    if request.method=='POST':
        form=ResumeForm(request.POST,instance=resume)
        # print(form.errors) 
        if form.is_valid():
            form.save()
            pending_application = request.session.get('pending_application')
            if pending_application:
                missing_details = resume_details_missing(resume)
                if not missing_details:
                    job = Job.objects.filter(id=pending_application.get('job_id')).first()
                    template = pending_application.get('resume_template')
                    if job and template in dict(Application.RESUME_TEMPLATE_CHOICES):
                        create_application(request.user, job, template)
                        request.session.pop('pending_application', None)
                        return redirect('/jobsearch/')
                    request.session.pop('pending_application', None)
            else:
                missing_details = []

            #One-sentence summary: instance=resume isn't only "pre-fill with old data" — 
            # its real, constant job in both branches is "keep this form permanently tied to this exact one row," 
            # which matters every single time, not just when there's existing data to show.
    else:
        form=ResumeForm(instance=resume)
    return render(request,'addresume.html',{
        'form':form,
        't_name':t_name,
        'pending_application':request.session.get('pending_application'),
        'missing_details':missing_details,
    })


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
                if i.cleaned_data.get('DELETE'):
                    if i.instance.pk:
                        i.instance.delete()
                else:
                    a=i.save(commit=False)
                    a.user=request.user
                    a.save()
            formset=skill_set(request.POST,queryset=qs)
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
    return render(request,'resume1.html',{'is_pdf':True})

@xframe_options_exempt
def resume2fn(request):
    return render(request,'resume2.html',{'is_pdf':True})

@xframe_options_exempt
def resume3fn(request):
    return render(request,'resume3.html',{'is_pdf':True})


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
    ex=experiance.objects.filter(user=request.user)
    ed=education.objects.filter(user=request.user)
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



def dashboardfn(request):
    return render(request,'dashboard.html')


@login_required(login_url='/login')
def feedbackfn(request):
    submitted = request.GET.get('sent') == '1'
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('/feedback/?sent=1')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form, 'submitted': submitted})



def jobsearchfn(request):
    jobs = Job.objects.none()
    own_jobs = Job.objects.none()
    other_jobs = Job.objects.none()
    applied_job_ids = set()
    chosen_template = request.session.get('t_name')
    user_role = ''
    if request.user.is_authenticated:
        user_role = Usercat.objects.filter(user=request.user).values_list('role', flat=True).first() or ''
        if user_role == 'interviewer':
            own_jobs = Job.objects.filter(posted_by=request.user).order_by('-id')
            other_jobs = Job.objects.exclude(posted_by=request.user).order_by('-id')
        else:
            jobs = Job.objects.all().order_by('-id')
            applied_job_ids = set(
                Application.objects.filter(applicant=request.user).values_list('job_id', flat=True)
            )
    else:
        jobs = Job.objects.all().order_by('-id')
    return render(request,'jobposted.html',{
        'jobs':jobs,
        'own_jobs':own_jobs,
        'other_jobs':other_jobs,
        'applied_job_ids':applied_job_ids,
        'chosen_template':chosen_template,
        'user_role':user_role,
    })


def job_detail_fn(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applied = False
    chosen_template = request.session.get('t_name')
    if request.user.is_authenticated:
        applied = Application.objects.filter(applicant=request.user, job=job).exists()
    return render(request, 'job_detail.html', {
        'job': job,
        'applied': applied,
        'chosen_template': chosen_template,
    })

def deletefn(request,j_id):
    job = get_object_or_404(Job, id=j_id)
    if job.posted_by != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        job.delete()
    return redirect('/jobsearch/')

def calculate_score(a_id,job):
    sk=Skills.objects.filter(user_id=a_id)
    sk_name=sk.values_list('skill',flat=True)
    if not job.requirements or not job.requirements.strip():

    #if job.requirements is empty, return 0, False
# or if it contains only spaces, also return 0, False
        return 0, False
    j=[s.strip() for s in job.requirements.split(',') if s and s.strip()]
    #j is a list (e.g., ['Python', 'Django', 'SQL'])
    #sk_name is a QuerySet of strings (e.g., ['Python', 'Django'])

    #if j in sk_name checks whether the entire list j exists as a single element inside sk_name
    
    job_set=set(s.lower() for s in  j)
    applicant_set=set(k.strip().lower() for k in sk_name if k and k.strip())    
    matching_skills=job_set & applicant_set
    match_count=len(matching_skills)
    job_count=len(job_set)
    if(job_count==0):
        return(0,False)
    
    else:
        match_percentage=(match_count/job_count)*100
        recommended=match_percentage>=60
        return match_percentage, recommended
    
   

def resume_details_missing(resume):
    required_details = {
        'first_name': 'First name',
        'last_name': 'Last name',
        'email': 'Email',
        'phone': 'Phone number',
    }
    return [label for field, label in required_details.items() if not getattr(resume, field)]


def create_application(applicant, job, resume_template):
    match_percentage, recommended = calculate_score(applicant.id, job)
    return Application.objects.get_or_create(
        applicant=applicant,
        job=job,
        defaults={
            'match_score': match_percentage,
            'recommended': recommended,
            'resume_template': resume_template,
        },
    )


@login_required(login_url='/login')
@require_POST
def applicationfn(request,job_id):
    role = Usercat.objects.filter(user=request.user).values_list('role', flat=True).first()
    if role != 'applicant':
        raise PermissionDenied
    job = get_object_or_404(Job, id=job_id)
    resume_template = request.POST.get('resume_template', '')
    valid_templates = dict(Application.RESUME_TEMPLATE_CHOICES)
    if resume_template not in valid_templates:
        resume_template = request.session.get('t_name', '')
    if resume_template not in valid_templates:
        return redirect('/jobsearch/')

    if Application.objects.filter(applicant=request.user, job=job).exists():
        return redirect('/jobsearch/')
    resume = Resume.objects.filter(user=request.user).first()
    if not resume or resume_details_missing(resume):
        request.session['t_name'] = resume_template
        request.session['pending_application'] = {
            'job_id': job.id,
            'resume_template': resume_template,
        }
        return redirect('profile', t_name=resume_template)

    create_application(request.user, job, resume_template)
    return redirect('/jobsearch/')

@login_required(login_url='/login')
def candidatefn(request,job_id):
    job=get_object_or_404(Job, id=job_id)
    if job.posted_by == request.user:
        applications = Application.objects.filter(job=job).select_related('applicant').order_by('-applied_on')
        for application in applications:
            resume = Resume.objects.filter(user=application.applicant).first()
            photo = Photo.objects.filter(user=application.applicant).first()
            resume_name = ''
            if resume:
                resume_name = ' '.join(
                    name for name in (resume.first_name, resume.middle_name, resume.last_name) if name
                )
            application.display_name = (
                resume_name or application.applicant.get_full_name() or application.applicant.username
            )
            application.photo_url = photo.photoup.url if photo and photo.photoup else ''
        rec = [application for application in applications if application.recommended]
        nonrec = [application for application in applications if not application.recommended]
        return render(request,'candidates.html',{
            'recommended_candidates':rec,
            'non_recommended_candidates':nonrec,
            'job':job,
        })
    else:
        raise PermissionDenied


@login_required(login_url='/login')
@require_POST
def application_statusfn(request, application_id):
    application = get_object_or_404(
        Application.objects.select_related('job'), id=application_id
    )
    if application.job.posted_by != request.user:
        raise PermissionDenied
    new_status = request.POST.get('status')
    allowed_statuses = {choice[0] for choice in Application.STATUS_CHOICES}
    if new_status in allowed_statuses:
        application.status = new_status
        application.save(update_fields=['status'])
    return redirect(f'/candidates/{application.job_id}/')


@login_required(login_url='/login')
@require_POST
def bulk_reject_applications_fn(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    role = Usercat.objects.filter(user=request.user).values_list('role', flat=True).first()
    if role != 'interviewer':
        raise PermissionDenied

    selected_ids = []
    for value in request.POST.getlist('application_ids'):
        try:
            selected_ids.append(int(value))
        except (TypeError, ValueError):
            continue

    if selected_ids:
        Application.objects.filter(
            job=job,
            recommended=False,
            id__in=selected_ids,
        ).update(status='rejected')
    return redirect(f'/candidates/{job.id}/')


@login_required(login_url='/login')
def applicant_resume_fn(request, application_id):
    application = get_object_or_404(
        Application.objects.select_related('applicant', 'job'), id=application_id
    )
    if application.job.posted_by != request.user:
        raise PermissionDenied

    template_names = {
        'professional1': 'resume1.html',
        'professional2': 'resume2.html',
        'professional3': 'resume3.html',
    }
    template_name = template_names.get(application.resume_template)
    if not template_name:
        raise PermissionDenied('The applicant did not select a resume template.')

    applicant = application.applicant
    resume, _ = Resume.objects.get_or_create(user=applicant)
    photo, _ = Photo.objects.get_or_create(user=applicant)
    experience = experiance.objects.filter(user=applicant)
    education_rows = education.objects.filter(user=applicant)
    skills = Skills.objects.filter(user=applicant)
    interests = Interests.objects.filter(user=applicant)
    expertise = Expertise.objects.filter(user=applicant)
    context = {
        'pr': resume,
        'candidate_user': applicant,
        'ph': photo,
        'ex': experience,
        'ed': education_rows,
        'edu': education_rows,
        'sk': skills,
        'ints': interests,
        'xt': expertise,
        'is_pdf': True,
        'interviewer_view': True,
        'job': application.job,
    }
    return render(request, template_name, context)



    # return render(request,'candidates.html')
    
    



  
        



    
