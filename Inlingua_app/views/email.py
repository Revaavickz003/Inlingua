from django.core.mail import send_mail
from django.shortcuts import redirect

def send_welcome_email(request):
    subject = 'Welcome to My Site'
    message = 'Thank you for creating an account!'
    from_email = '<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="1776737a7e79577a6e647e63723974787a">[email&nbsp;protected]</a>'
    recipient_list = [request.user.email]
    send_mail(subject, message, from_email, recipient_list)
    # print(subject)
    # print(message)
    # print(from_email)
    # print(recipient_list)
    return redirect('home')