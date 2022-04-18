from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os, os.path

User = get_user_model()

@login_required
def view_profile(request):

    return render(request, 'users/profile.html')
