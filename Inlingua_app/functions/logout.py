from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')
