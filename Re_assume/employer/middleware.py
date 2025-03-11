# authentication_middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from .models  import *
from django.contrib import messages
class   auth  :
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Redirect to login if accessing dashboard without being logged in
        if not request.session.get('is_emp_authenticated'):
            return redirect('employer:employer_login')

        response = self.get_response(request)
        return response
    
