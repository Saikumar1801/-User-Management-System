# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import Profile

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            # Create User
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            user.save()

            # Create Profile
            profile = Profile(
                user=user,
                user_type=form.cleaned_data['user_type'],
                profile_picture=form.cleaned_data['profile_picture'],
                address_line1=form.cleaned_data['address_line1'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                pincode=form.cleaned_data['pincode']
            )
            profile.save()

            # Log the user in and redirect
            login(request, user)
            if profile.user_type == 'doctor':
                return redirect('doctor_dashboard')
            else:
                return redirect('patient_dashboard')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user type
                if user.profile.user_type == 'doctor':
                    return redirect('doctor_dashboard')
                else:
                    return redirect('patient_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def doctor_dashboard(request):
    # Make sure only doctors can access this page
    if request.user.profile.user_type != 'doctor':
        return redirect('patient_dashboard') # Or an error page
    return render(request, 'accounts/doctor_dashboard.html')


@login_required
def patient_dashboard(request):
    # Make sure only patients can access this page
    if request.user.profile.user_type != 'patient':
        return redirect('doctor_dashboard') # Or an error page
    return render(request, 'accounts/patient_dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('login')