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


class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=['user']
        widgets={
            'gender':forms.RadioSelect
        }

class ApplicantForm(UserProfileForm):
    class Meta(UserProfileForm.Meta):
        exclude=UserProfileForm.Meta.exclude + ['company_name']

class InterviewerForm(UserProfileForm):
    company_name=forms.CharField(max_length=100,required=True)

class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password']
        widgets={
            'password':forms.PasswordInput()
        }
        
class Photoform(forms.ModelForm):
    class Meta:
        model=Photo
        exclude=['user']

class Jobform(forms.ModelForm):
    class Meta:
        model=Job
        exclude=['posted_by']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.TextInput(attrs={'class': 'input'}),
            'company': forms.TextInput(attrs={'class': 'input'}),
            'location': forms.TextInput(attrs={'class': 'input'}),
            'requirements': forms.TextInput(attrs={'class': 'input','placeholder':'E:g. Python,Django,SQL,Git'}),
            'responsibilities': forms.TextInput(attrs={'class': 'input'}),
            'availability': forms.Select(attrs={'class': 'input'}),
            'salary': forms.NumberInput(attrs={'class': 'input', 'step': '0.01'}),
        }
    def clean_requirements(self):
        data=self.cleaned_data['requirements']
        if len(data.split(',')) <2:
            raise forms.ValidationError("Please enter skills seperated by comma")
        skill=[s.strip() for s in data.split(',')]
        #data.split(',') runs first. It splits the string wherever a comma appears
        cleaned=', '.join(skill)
        return cleaned


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'maxlength': 2000,
                'placeholder': 'Tell us what went well or what we can improve...',
            }),
        }