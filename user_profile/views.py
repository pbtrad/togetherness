from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from user_profile.forms import UserRegistrationForm
from django.contrib import messages


def index(request):
    return render(request,'base.html')

def register(request):
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()
            
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
            
            if user:
                messages.success(request, "Your account had been created")
                auth.login(user=user, request=request)
                return redirect(reverse('create_profile'))
            else:
                messages.error(request, "Sorry, unable to create your account")
    else:
        registration_form = UserRegistrationForm()
        

    context = {
        'registration_form':registration_form
    }
    return render(request, 'user_profile/register.html', context)