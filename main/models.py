from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField



class Resume(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50,null=True,blank=True)
    middle_name=models.CharField(max_length=50,null=True,blank=True,verbose_name="Middle name (Optional)")
    last_name=models.CharField(max_length=50,null=True,blank=True)
    GENDER_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('others','Others'),
        ('prefer not to say','Prefer not to say')

    ]
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES,null=True,blank=True,verbose_name="Gender (Optional)")
    dob=models.DateField(null=True,blank=True,verbose_name="DOB (Optional)")
    
    MARITAL_CHOICES=[
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
    pin_code=models.CharField(null=True,blank=True,verbose_name=" Pin code(Optional)")
    email=models.EmailField()
    phone=models.CharField(max_length=14)

    class Meta:
           db_table="profile"
    
    # degree = models.CharField(max_length=100)
    # institution = models.CharField(max_length=150)
    # graduation_year = models.CharField(max_length=10)
    # cgpa = models.CharField(max_length=5, blank=True, null=True)
    # linkedin_url=models.URLField(blank=True,null=True)
    # github_url=models.URLField(blank=True,null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # summary = models.TextField(help_text="bio")
    # skills=models.TextField(help_text="eg:python,web development...")
   
