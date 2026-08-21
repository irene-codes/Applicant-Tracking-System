from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    email=models.EmailField()
    phoneno=models.CharField(max_length=14)
    location=models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=150)
    graduation_year = models.CharField(max_length=10)
    cgpa = models.CharField(max_length=5, blank=True, null=True)
    linkedin_url=models.URLField(blank=True,null=True)
    github_url=models.URLField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    summary = models.TextField(help_text="bio")
    skills=models.TextField(help_text="eg:python,web development...")

    