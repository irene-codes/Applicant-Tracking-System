from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField



class Resume(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50,null=True,blank=True)
    middle_name=models.CharField(max_length=50,null=True,blank=True,verbose_name="Middle name (Optional)")
    last_name=models.CharField(max_length=50,null=True,blank=True)
    GENDER_CHOICES = [
        ('', 'Select'),
        ('men', 'Men'),
        ('women', 'Women'),
        ('others','Others'),
        ('prefer not to say','Prefer not to say')

    ]
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES,null=True,blank=True,verbose_name="Gender (Optional)")
    dob=models.DateField(null=True,blank=True,verbose_name="DOB (Optional)")
    
    MARITAL_CHOICES=[
        ('', 'Select'),
        ('single','Single'),
        ('married','Married'),
        ('divorced','Divorced'),
        ('widowed','Widowed'),
        ('empty','Empty')

    ]
    marital_status=models.CharField(max_length=15,choices=MARITAL_CHOICES,null=True,blank=True,verbose_name="Maritul Status (Optional)")
    profession=models.CharField(max_length=100,null=True,blank=True)
    address=models.CharField(max_length=400,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True)
    nationality=CountryField(null=True,blank=True,verbose_name="Nationality (Optional)")
    pin_code=models.CharField(max_length=10,null=True,blank=True,verbose_name="Pin code (Optional)")
    email=models.EmailField(null=True,blank=True)
    phone=models.CharField(max_length=14,null=True,blank=True)

    class Meta:
           db_table="profile"
   
class experiance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title=models.CharField(max_length=50)
    employer=models.CharField(max_length=50)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=50)
    start_date=models.DateField(null=True,blank=True)
    end_date=models.DateField(null=True,blank=True)
    class Meta:
        db_table = "experience"

class education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school_name=models.CharField(max_length=100)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    DEGREE_CHOICES = [
        ('', 'Select'),
        ('high_school_diploma', 'High School Diploma'),
        ('ssc', 'Senior Secondary School Certificate (SSCE)'),
        ('gcse', 'General Certificate of Secondary Education (GCSEs)'),
        ('ged', 'GED'),
        ('diploma', 'Diploma'),
        ('national_diploma', 'National Diploma'),
        ('higher_national_diploma', 'Higher National Diploma'),
        ('post_secondary_vocational', 'Post-secondary (Technical & Vocational)'),
        ('associate_arts', 'Associate of Arts'),
        ('associate_science', 'Associate of Science'),
        ('associate_applied_science', 'Associate of Applied Science'),
        ('bachelor_arts', 'Bachelor of Arts (BA)'),
        ('bachelor_science', 'Bachelor of Science (BSc)'),
        ('bachelor_technology', 'Bachelor of Technology (B.Tech)'),
        ('bachelor_engineering', 'Bachelor of Engineering (BE)'),
        ('bachelor_commerce', 'Bachelor of Commerce (B.Com)'),
        ('bachelor_business_admin', 'Bachelor of Business Administration (BBA)'),
        ('bachelor_computer_apps', 'Bachelor of Computer Applications (BCA)'),
        ('llb', 'Bachelor of Laws (LLB)'),
        ('mbbs', 'Bachelor of Medicine, Bachelor of Surgery (MBBS)'),
        ('master_arts', 'Master of Arts (MA)'),
        ('master_science', 'Master of Science (MSc)'),
        ('master_technology', 'Master of Technology (M.Tech)'),
        ('master_business_admin', 'Master of Business Administration (MBA)'),
        ('master_computer_apps', 'Master of Computer Applications (MCA)'),
        ('master_commerce', 'Master of Commerce (M.Com)'),
        ('llm', 'Master of Laws (LLM)'),
        ('phd', 'Doctor of Philosophy (PhD)'),
        ('md', 'Doctor of Medicine (MD)'),
        ('certificate', 'Certificate Course'),
        ('other', 'Other')

    ]
    select_a_degree=models.CharField(max_length=100,choices=DEGREE_CHOICES,null=True,blank=True)
    field_of_study=models.CharField(max_length=100)
    graduation_start_date=models.DateField(null=True,blank=True)
    graduation_end_date=models.DateField(null=True,blank=True)
    class Meta:
            db_table = "education"


class Skills(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill=models.CharField(max_length=20)
    SKILL_CHOICES=[
        ('','Select'),
        ('novice','Novice'),
        ('beginner','Beginner'),
        ('intermediate','Intermediate'),
        ('proficient','Proficient'),
        ('expert','Expert')
    ]
    level=models.CharField(max_length=15,choices=SKILL_CHOICES,null=True,blank=True)


    
class Interests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Hobbies=models.CharField(max_length=20,null=True,blank=True)


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photoup=models.ImageField(upload_to='photo',null=True,blank=True,verbose_name='Upload cv photo')
    linkedin=models.URLField(max_length=200,blank=True)   
    twitter=models.URLField(max_length=200,blank=True)   
    github=models.URLField(max_length=200,blank=True)   
    website=models.URLField(max_length=200,blank=True)   
    leetcode=models.URLField(max_length=200,blank=True)
    facebook=models.URLField(max_length=200,blank=True,null=True)   

class Expertise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    