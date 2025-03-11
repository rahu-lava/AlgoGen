import pandas as pd
from django.shortcuts import render , redirect
# import requests,json
from .middlewares import auth
from .models import Resume
from credentials.models import *
import re
import numpy as np
@auth
def home(request):
    # Retrieve user ID from session
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = user_table.objects.get(id=user_id)  # Get user instance
            u_resume = Resume.objects.filter(user=user).first()  # Get single resume if exists

            return render(request, 'dashboard/home.html', {'user': user, 'u_resume': u_resume})
        except user_table.DoesNotExist:
            return redirect('login')  # Redirect if user not found

    # If user_id not found in session, redirect to login
    return redirect('login')

# Load and preprocess the dataset once (to optimize performance)
file_path = r"E:\django\Re_assume\dashboard\employer_02.xlsx"
 # Change this to the actual file path
df = pd.read_excel(file_path)

# Preprocessing function
def clean_text(text):
    if isinstance(text, str):
        return re.sub(r'\W+', ' ', text.lower().strip())  # Remove special characters & lowercase
    return ""

df["Processed_Desc"] = df["Long Description"].astype(str).apply(clean_text)
df["Processed_Keyword"] = df["Primary Keyword"].astype(str).apply(clean_text)
df["Position"] = df["Position"].astype(str).str.lower()
df["Experience_Years"] = df["Exp Years"].fillna(0).astype(float)
df["English_Level"] = pd.to_numeric(df["English Level"], errors="coerce").fillna(0).astype(int)

# Function to calculate matching score
def calculate_matching_score(new_desc, new_keyword, position, new_exp, new_eng):
    position = position.lower()
    new_desc_list = [skill.strip().lower() for skill in new_desc.split(",")]
    new_keyword = clean_text(new_keyword)

    # Filter dataset for exact position match
    filtered_df = df[df["Position"] == position]

    if filtered_df.empty:
        return 0.0  # No matching jobs found

    matched_skills = sum(any(skill in desc for desc in filtered_df["Processed_Desc"]) for skill in new_desc_list)
    skill_match_percentage = (matched_skills / len(new_desc_list)) * 100 if new_desc_list else 0

    keyword_match = any(new_keyword in kw for kw in filtered_df["Processed_Keyword"])
    
    exp_sim = 1 - (np.abs(filtered_df["Experience_Years"] - new_exp).mean() / max(filtered_df["Experience_Years"].max(), 1))
    eng_sim = 1 - (np.abs(filtered_df["English_Level"] - new_eng).mean() / 5)

    exp_sim = max(0, exp_sim) * 100
    eng_sim = max(0, eng_sim) * 100

    final_score = (0.50 * skill_match_percentage) + (0.20 * (100 if keyword_match else 0)) + (0.20 * exp_sim) + (0.10 * eng_sim)

    return round(final_score, 2)  # Convert to percentage (0-100)

# Django View for Resume Submission
@auth
def resume_view(request):
    user = user_table.objects.get(id=request.session.get('user_id'))
    u_resume = Resume.objects.filter(user=user).first()  # Get user's resume if exists

    if request.method == 'POST':
        skills = request.POST.get('skills')
        experience = int(request.POST.get('experience', 0))
        position = request.POST.get('position')
        keywords = request.POST.get('keywords')
        english_level = int(request.POST.get('englishLevel', 0))

        if skills and experience and position and keywords:
            # Calculate new matching score
            current_rating = calculate_matching_score(skills, keywords, position, experience, english_level)

            if u_resume:
                # **Update existing resume**
                u_resume.skills = skills
                u_resume.experience = experience
                u_resume.position = position
                u_resume.keywords = keywords
                u_resume.english_level = english_level
                u_resume.current_rating = str(current_rating)  # Store rating
                u_resume.save()
            else:
                # **Create a new resume if none exists**
                u_resume = Resume.objects.create(
                    user=user,
                    skills=skills,
                    experience=experience,
                    position=position,
                    keywords=keywords,
                    english_level=english_level,
                    current_rating=str(current_rating)  # Store rating
                )

            return render(request, 'dashboard/home.html', {'user': user, 'u_resume': u_resume})

    return render(request, 'dashboard/resume_form.html', {'user': user, 'u_resume': u_resume})  # Render form if GET request
