from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os, os.path

User = get_user_model()

@login_required
def view_profile(request):
    # If PUT request made, update the content of the profile
    if request.method == "PUT":
        # Get the data form data
        form = request.PUT
        birth_date = form.get('birth_date')
        address = form.get('address')
        postal_code = form.get('postal_code')
        city = form.get('city')
        country = form.get('country')
        gender = form.get('gender')
        profile_pic = form.FILES.get('profile_pic')

        # TODO: update profile
        # Update user attributes with the form data
        user = User.objects.get(id=request.user.id)
        user.birth_date = birth_date
        user.address = address
        user.postal_code = postal_code
        user.city = city
        user.country = country
        user.gender = gender
        user.profile.image = profile_pic

        user.profile.save()
        user.save()

        # Redirect the user to home page after 
        # successfully updating the profile
        return redirect('home')
    return render(request, 'users/profile.html')
