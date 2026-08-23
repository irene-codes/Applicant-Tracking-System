from django import forms
from .models import *

class ResumeForm(forms.ModelForm):
    class Meta:
        model=Resume
        exclude=['user']
        db_table="profile"
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            

        }

class ExperianceForm(forms.ModelForm):
    class Meta:
        model=experiance
        exclude=['user']
        db_table = "experience"
        widgets ={
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date':forms.DateInput(attrs={'type':'date'})

        }
class EducationForm(forms.ModelForm):
    class Meta:
        model=education
        exclude=['user']
        db_table = "education"
        widgets ={
            'graduation_start_date':forms.DateInput(attrs={'type':'date'}),
            'graduation_end_date':forms.DateInput(attrs={'type':'date'})
        }
        




#"Row = horizontal line" — correct. row tells Bootstrap "arrange my direct children side-by-side, in a horizontal line,"
#"Each column means 1/3 of row's width" — correct, but only because you specifically chose col-md-4 three times. The 1/3 split isn't automatic just from using col — it comes from the number you pick. Since Bootstrap's grid always totals 12 units per row:

# col-md-4 three times → 4+4+4 = 12 → each takes exactly 1/3 of the row
# col-md-6 two times → 6+6 = 12 → each takes exactly 1/2 of the row
# col-md-3 four times → 3+3+3+3 = 12 → each takes exactly 1/4 of the row