from django.shortcuts import render,redirect
from .models import *
from .middleware import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password,make_password
from django.db.models import Q
from credentials.models import user_table
from django.template.loader import render_to_string
from django.http import JsonResponse,HttpResponse
from dashboard.models import *
# Create your views here.


def employer_register(request):
    if request.method == "POST":
        employer = request.POST
        Password = make_password(employer.get('Password'))
        data = {
            'first_name':employer.get('FirstName'),
            'last_name':employer.get('LastName'),
            'email':employer.get('Email'),
            'password':Password,
        }
        # Save theemployer instance
        employer_instant = employer_table.objects.create(**data)
        employer_instant.save()
        # Pass the user instance to the template
        return redirect('employer:employer_login')
    return render(request, 'credentials/employer_register.html')


def employer_login(request):
    if request.method == "POST":
        email =  request.POST.get('Email')
        password = request.POST.get('Password')
        print(email,password)
        try:
            employer = employer_table.objects.get(email=email.strip())
            # Check if the provided password matches the hashed password in the database
            print(employer.password)
            print(password.strip(), employer.password)
            if check_password(password.strip(), employer.password):
                print('Employer authenticated')
                request.session['is_emp_authenticated'] = True
                request.session['employer_id'] = employer.id
                return redirect('employer:employer_dashboard')  # Redirect to dashboard after login
            else:
                return render(request, 'credentials/employer_login.html', {'error': 'Invalid credentials'})
        except employer_table.DoesNotExist:
            print('Employer not found')
            return render(request, 'credentials/employer_login.html', {'error': 'Invalid credentials'})
    return render(request, 'credentials/employer_login.html')

def employer_logout(request):
    request.session.flush()
    return render(request, 'credentials/employer_login.html')


@auth
def employer_dashboard(request):
    return render(request, 'emp_dashboard/home.html')



def search_candidates(request):
    position = request.GET.get('position', '').strip()
    experience = request.GET.get('experience', '')
    english_level = request.GET.get('englishLevel', '')
    keywords = request.GET.get('keywords', '').lower().split(',')
    description = request.GET.get('description', '').lower()

    resumes = Resume.objects.all()

    if position:
        resumes = resumes.filter(position__icontains=position)

    if experience.isdigit():
        resumes = resumes.filter(experience__gte=int(experience))

    if english_level.isdigit():
        resumes = resumes.filter(english_level=int(english_level))

    if keywords:
        resumes = resumes.filter(skills__icontains=keywords[0])  # Matching at least one skill

    if description:
        resumes = resumes.filter(keywords__icontains=description)

    resumes = resumes.order_by('-current_rating')  # Order by rating

    resume_list = [
        {
            "first_name": resume.user.first_name,  # Assuming `user_table` has a `name` field
            "last_name": resume.user.last_name,  # Assuming `user_table` has a `name` field
            "position": resume.position,
            "experience": resume.experience,
            "skills": resume.skills.split(','),
            "english_level": dict(Resume.ENGLISH_LEVEL_CHOICES).get(resume.english_level, "Unknown"),
            "rating": resume.current_rating,
        }
        for resume in resumes
    ]

    return JsonResponse({"resumes": resume_list})
