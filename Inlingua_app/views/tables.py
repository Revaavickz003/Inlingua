from django.shortcuts import render, redirect
from django.contrib import messages
from Inlingua_app.models import User, TrainingStaff, TrainerQualifications, TrainingBatches, StudentDetails,UserRoles, Languages

def table_page(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        if user.is_staff:
            if user.is_superuser:
                roles = UserRoles.objects.all()
                languages = Languages.objects.all()
                context = {'User': user, 'roles': roles, 'languages':languages, 'tables':'active'}
                return render(request, "inlingua/tables.html",context)

            else:
                pass
        else:
            pass
    else:
        pass