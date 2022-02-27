from django.forms import modelformset_factory
from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from user_profile.forms import UserRegistrationForm, ProfileImageForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, ProfileImage


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


def create_profile(request):
    """
    Create a formset to allow for multiple profile photos to be uploaded
    Assistance from
    https://stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django
    """
    ImageFormSet = modelformset_factory(ProfileImage, form=ProfileImageForm, extra=6, max_num=6, help_texts=None)
    
    # If user has submitted profile form
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        image_form = ProfileImageForm(request.POST, request.FILES)
        
        formset = ImageFormSet(request.POST, request.FILES,
                              queryset=ProfileImage.objects.filter(user_id=request.user.id).all())
        
        # Update profile and change profile to 'to be approved'
        if profile_form.is_valid() and formset.is_valid():
            instance = profile_form.save(commit=False)
            instance.user_id = request.user.id
            instance.is_verified = 'TO BE APPROVED'
            instance.save()
            
            # Get images requested to be deleted and delete them
            deleted_images = request.POST.getlist('delete')
            for image in deleted_images:
                if not image == "None":
                    ProfileImage.objects.get(pk=image).delete()
                    
            # Save submitted images
            for form in formset:
                if form.is_valid() and form.has_changed():
                    instance_image = form.save(commit=False)
                    instance_image.user = request.user
                    instance_image.is_verified = False
                    instance_image.save()

            return redirect(reverse('verification_message'))
            
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        image_form = ProfileImageForm(instance=request.user.profile)
        initial_images = [{'image_url': i.image} for i in ProfileImage.objects.filter(user_id=request.user.id).all() if i.image]
        formset = ImageFormSet(queryset=ProfileImage.objects.filter(user_id=request.user.id).all(), initial=initial_images)
        
    context = {
        'page_ref':'create_profile',
        'profile_form':profile_form,
        'image_form':image_form,
        'formset': formset
    }
        
    return render(request, 'user_profile/create_profile.html', context)    