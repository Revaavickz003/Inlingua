import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from Inlingua_app.models import User, TrainingStaff, TrainerQualifications, TrainingBatches, StudentDetails,UserRoles, Languages
from django.urls import reverse


def language_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        if user.is_staff:
            if user.is_superuser:
                roles = UserRoles.objects.all()
                languages = Languages.objects.all()
                context = {'User': user, 'roles': roles, 'languages':languages,'showcontainer':'d-block'}
                return render(request, "inlingua/tables.html",context)

            else:
                pass
        else:
            pass
    else:
        pass


def add_language(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_staff and user.is_superuser:
            if request.method == 'POST':
                name = request.POST.get('language')
                if name:
                    if not Languages.objects.filter(Name=name).exists():
                        language = Languages.objects.create(Name=name, CreatedBy=request.user.username, UpdatedBy=request.user.username)
                        language.save()
                        
                        messages.success(request,"Language added successfully!")
                        return redirect('tables')  

                    else:
                        messages.error(request,"This Language already exists.")
                else:
                    messages.warning(request,"Please fill out all fields.")
            return redirect('tables') 
        messages.error(request,"You dont add language")
        return redirect('home')
    else:
        messages.error(request,"Please login to continue")
        return redirect('login')    

from django.http import Http404

def edit_lang(request, id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        if user.is_staff and user.is_superuser:
            if request.method == 'POST':
                role_name = request.POST.get('RoleName')
                if not Languages.objects.filter(Name=role_name).exists():
                    update_langu = Languages.objects.get(ID=id)

                    update_langu.Name = role_name
                    update_langu.UpdatedBy = request.user.username
                    update_langu.UpdatedDate = datetime.datetime.now()

                    update_langu.save()
                    messages.info(request,'Language has been updated')
                    return redirect('tables')
                else:
                    messages.error(request,"This Language already exists.")
                    return redirect('tables')
            else:
                try:
                    get_data = Languages.objects.get(ID=id)
                except UserRoles.DoesNotExist:
                    raise Http404("Role does not exist")


                roles = UserRoles.objects.all()
                languages = Languages.objects.all()
                context = {
                    'User': user,
                    'tables':'active',
                    'roles': roles,
                    'languages': languages,
                    'get_data': get_data,
                    'showlangcontainer': 'd-block',
                }
                return render(request, "inlingua/tables.html", context)
    else:
        pass  # Handle authentication failure if needed

def delete_langu(request, id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        if user.is_staff and user.is_superuser:
            try:
                update_langu = Languages.objects.get(ID=id)
                update_langu.IsActive = False
                update_langu.UpdatedBy = request.user.username
                update_langu.UpdatedDate = datetime.datetime.now()
                update_langu.save()

                messages.success(request, f"{update_langu.Name} has been deleted successfully from the system.")
                return redirect('tables')
            except UserRoles.DoesNotExist:
                raise Http404("Role does not exist")
            
            
        else:
            messages.error(request, 'You do not have permission to perform this action!')
            return redirect('home')
    else:
        pass  # Handle authentication failure if needed