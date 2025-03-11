from django.shortcuts import render,redirect
# Create your views here.
from dotenv import load_dotenv
import os
from dashboard.models import *
from .middleware import check_session
from django.contrib.auth.hashers import check_password,make_password
from .models import user_table,FeedBack
load_dotenv()

def landing_page(request):
    return render(request,'credentials/landing_page.html')

def register(request):
    if request.method == "POST":
        print('inside register')
        user = request.POST
        data = {
            'first_name': user.get('FirstName'),
            'last_name': user.get('LastName'),
            'email': user.get('Email'),
            'password': make_password(user.get('Password'))
        }
        try:
            user_instance = user_table.objects.create(**data)
            user_instance.save()
            print('Registeration Done')
            request.session['is_authenticated'] = True 
            request.session['user_id'] = user_instance.id 
            return redirect('complete_profile:basic_detail')
        except Exception as e:
            render(request, 'credentials/register.html', {'error': 'Invalid credentials'})
    return render(request, 'credentials/register.html',)

@check_session
def login(request):
    if request.method == "POST":
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        # Validate email and password
        try:
            user = user_table.objects.get(email=email.strip())
            # Check if the provided password matches the hashed password in the database
            print(user.password)
            print('Password is :',check_password(password.strip(), user.password))
            if check_password(password.strip(), user.password):
                print('Employer authenticated')
                request.session['is_authenticated'] = True
                request.session['user_id'] = user.id        # Store user ID in session (optional)
                # print(user.id)
                request.session.set_expiry(604800)
                return redirect('dashboard:home')  # Redirect to dashboard after login
            else:
                return render(request, 'credentials/login.html', {'error': 'Invalid credentials'})

        except user_table.DoesNotExist:
            return render(request, 'credentials/login.html', {'error': 'Invalid credentials'})
    return render(request, 'credentials/login.html')

def logout(request):
    request.session.flush()
    return render(request, 'credentials/login.html')

def feedback(request):
    
    if request.method == "POST":
        feedback = request.POST
        data = {
            'name': feedback.get('name'),
            'email': feedback.get('email'),
            'feedback': feedback.get('feedback')
        }
        print(data)
        feedback_instance = FeedBack.objects.create(**data)
        feedback_instance.save()
        return render(request, 'credentials/landing_page.html')
    return render(request, 'credentials/landing_page.html')

