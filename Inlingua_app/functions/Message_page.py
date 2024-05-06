from django.shortcuts import render,redirect
from django.urls import reverse
from Inlingua_app.models import User, Message
from django.contrib import messages
import datetime

# Create your views here.
def message_view(request):

    context = {
        'Message_page': 'active',
        'Users' : User.objects.filter(is_superuser=False),
    }
    return render(request, 'inlingua/Message_page.html', context)

def Message_for_user(request, username):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        sender = request.user  
        created_by = request.user  
        receiver = User.objects.get(username=username)
        
        # Save message to the database
        message = Message.objects.create(sender=sender, receiver=receiver, content=message_content, created_by=created_by, created_date=datetime.datetime.now())
        
        return redirect(reverse('Message_for_user', kwargs={'username': username}))
    else:
        try:
            message_for_user = User.objects.get(username=username)
        except:
            messages.error(request, 'User not found')
            return redirect('Message_page')
        
        if message_for_user.is_superuser == False:
            message_for_user =  User.objects.get(username=username)
            all_messages = Message.objects.filter(receiver = message_for_user )
        else:
            messages.error(request, 'This user is admin, You don`t message in admin' )
            return redirect('Message_page')
        context = {
            'Message_page': 'active',
            'Users' : User.objects.filter(is_superuser=False),
            'message_for_user': message_for_user,
            'all_messages': all_messages,
        }
        return render(request, 'inlingua/Message_page.html', context)

