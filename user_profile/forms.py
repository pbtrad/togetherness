from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from togetherness import settings
from .models import ProfileImage, Profile

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'maxlength':'12'}))
    password1 = forms.CharField(label="Enter Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].required = True

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        
    def cleaned_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u'Email address has already been used!')
    
        # Add cleaned username
    
        return email
    
    def cleaned_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if not password1 or password2:
            raise ValidationError("Password fields must be filled in")
            
        if password1 != password2:
            raise ValidationError("Passwords do not match. Please try again.")
            
        return password2    

class ProfileImageForm(forms.ModelForm):
    
    image = forms.ImageField(label='', required=False, error_messages = {'invalid':"Image files only"}, widget=forms.FileInput(attrs = {'class': "profile-photo-input"}))

    class Meta:
        model = ProfileImage
        fields = ('image', )


class ProfileForm(forms.ModelForm):
    
    HEIGHT_CHOICES = (
        ("152.4","5' 0"),
        ("154.94","5' 1"),
        ("157.48","5' 2"),
        ("160.02","5' 3"),
        ("162.56","5' 4"),
        ("165.1","5' 5"),
        ("167.64","5' 6"),
        ("170.18","5' 7"),
        ("172.72","5' 8"),
        ("175.26","5' 9"),
        ("177.8","5' 10"),
        ("180.34","5' 11"),
        ("182.88","6' 0"),
        ("185.42","6' 1"),
        ("187.96","6' 2"),
        ("190.5","6' 3"),
        ("193.04","6' 4"),
        ("195.58","6' 5"),
        ("198.12","6' 6"),
        ("200.66","6' 7"),
        ("203.2","6' 8"),
        ("205.74","6' 9"),
        ("208.28","6' 10"),
        ("210.82","6' 11")
    )
    
    
    CHILDREN_CHOICES = (
        (True, "Yes"),
        (False, "No")
        )
    
    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id':'autocomplete'}), required=True)
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'bio-field', 'maxlength': '200'}), required=True)
    children = forms.ChoiceField(choices = CHILDREN_CHOICES, initial='', widget=forms.Select(), required=True)
    height = forms.ChoiceField(choices = HEIGHT_CHOICES, initial='', widget=forms.Select(), required=True)
    
    class Meta:
        model = Profile
        fields = ( 'bio', 'gender', 'hair_colour', 'hair_length', 'body_type', 'relationship_status', 'looking_for', 'education', 'height', 'children', 'location', 'birth_date')
        widgets = {
            'date' : forms.DateInput(attrs={'type':'date'})
        } 

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

