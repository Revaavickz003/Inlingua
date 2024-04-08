from django.shortcuts import render, redirect
from django.urls import reverse
from Inlingua_app.models import Courses

def classstart(request,id):
    if request.user.is_authenticated:
        try:
            Course = Courses.objects.get(ID=id)
            Course.class_active=True
            Course.save()
            return redirect(reverse('batches', kwargs={'id': id}))
        except Exception as e:
            print("Error in ClassStart view",e)
    else:
        pass


def classend(request,id):
    if request.user.is_authenticated:
        try:
            Course = Courses.objects.get(ID=id)
            Course.class_active=False
            Course.save()
            return redirect(reverse('batches', kwargs={'id': id}))
        except Exception as e:
            print("Error in ClassStart view",e)
    else:
        pass