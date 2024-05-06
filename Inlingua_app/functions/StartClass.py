from django.shortcuts import  redirect
from django.urls import reverse
from Inlingua_app.models import Courses
from django.contrib import messages

def classstart(request,id, classid):
    if request.user.is_authenticated:
        try:
            Course = Courses.objects.get(ID=classid)
            Course.class_active=True
            Course.save()
            return redirect(reverse('batches', kwargs={'id': id}))
        except Exception as e:
            messages.error(request, "Error in Class start view",e)
            return redirect(reverse('batches', kwargs={'id': id}))
    else:
        pass


def classend(request,id, classid):
    if request.user.is_authenticated:
        try:
            Course = Courses.objects.get(ID=classid)
            Course.class_active=False
            Course.save()
            return redirect(reverse('batches', kwargs={'id': id}))
        except Exception as e:
            messages.error(request, "Error in Class start view",e)
            return redirect(reverse('batches', kwargs={'id': id}))
    else:
        pass