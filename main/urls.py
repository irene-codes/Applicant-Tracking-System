from django.urls import path
from main.views import *
urlpatterns=[
   path('',homefn),
   
   path('jobs/',jobfn),
   path('register/',registerfn),
   path('login/',loginfn)

]