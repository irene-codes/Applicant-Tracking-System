from django.urls import path
from main.views import *
urlpatterns=[
   path('',homefn),
   path('add/',addfn,name='profile'),
   path('jobs/',jobfn),
   path('register/',registerfn),
   path('login/',loginfn),
   path('logout/',logoutfn),
   path('experiance/',experiancefn,name='experiance'),
   path('education/',educationfn,name='education'),
   path('skills/',skillfn,name='skills'),
   path('summary/',summaryfn,name='summary'),
   path('interest/',interestfn,name='interest'),
]