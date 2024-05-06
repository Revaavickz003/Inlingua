# import datetime
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from Inlingua_app.models import User, TrainingStaff, TrainerQualifications, TrainingBatches, StudentDetails,UserRoles, Languages
# from django.urls import reverse


# # cipher_suite = Fernet('EM0C8xTuTbAomZ8DQVS7c3X4CMJyLZIfXor44smagws=')


# def role_view(request):
#     if request.user.is_authenticated:
#         user_id = request.user.id
#         user = User.objects.get(id=user_id)
        
#         if user.is_staff:
#             if user.is_superuser:
#                 roles = UserRoles.objects.all()
#                 languages = Languages.objects.all()
#                 context = {'User': user, 'roles': roles, 'languages':languages,'showcontainer_role':'d-block'}
#                 return render(request, "inlingua/tables.html",context)

#             else:
#                 pass
#         else:
#             pass
#     else:
#         pass


# def add_role(request):
#     if request.user.is_authenticated:
#         user_id = request.user.id
#         user = User.objects.get(id=user_id)
#         if request.method == 'POST':
#             Role_Name = request.POST.get('romeName')
#             Role_Description = request.POST.get("description")

#             if Role_Name:
#                 if not UserRoles.objects.filter(Name=Role_Name).exists():
#                     role = UserRoles.objects.create(
#                         Name=Role_Name,
#                         Description=Role_Description,
#                         IsActive = True,
#                         CreatedBy=request.user.username, 
#                         UpdatedBy=request.user.username)
#                     role.save()
                    
#                     messages.success(request,"Role added successfully!")
#                     return redirect('tables')  

#                 else:
#                     messages.error(request,"This Language already exists.")
#             else:
#                 messages.warning(request,"Please fill out all fields.")
#         return redirect('tables')
#     else:
#         messages.error(request,  "You are not logged in.")
#         return redirect('login')


# from Inlingua_app.forms import UserRolesForm
# from django.http import Http404

# def edit_view(request, id):
#     if request.user.is_authenticated:
#         user_id = request.user.id
#         user = User.objects.get(id=user_id)

#         if user.is_staff and user.is_superuser:
#             if request.method == 'POST':
#                 role_name = request.POST.get('RoleName')
#                 description = request.POST.get('Roledesc')

#                 update_role = UserRoles.objects.get(ID=id)

#                 update_role.Name = role_name
#                 update_role.Description = description
#                 update_role.UpdatedBy = request.user.username
#                 update_role.UpdatedDate = datetime.datetime.now()

#                 update_role.save()
#                 messages.info(request, "Role updated successfully.")
#                 return redirect('tables')  
#             else:
#                 get_data = None
#                 try:
#                     get_data = UserRoles.objects.get(ID=id)
#                 except UserRoles.DoesNotExist:
#                     messages.error(request,  "Userrole does not exist")
#                     return redirect('tables')


#                 roles = UserRoles.objects.all()
#                 languages = Languages.objects.all()
#                 context = {
#                     'tables':'active',
#                     'User': user,
#                     'roles': roles,
#                     'languages': languages,
#                     'get_data': get_data,
#                     'showdivcontainer': 'd-block',
#                 }
#                 return render(request, "inlingua/tables.html", context)
#     else:
#         pass  # Handle authentication failure if needed


# def delete_role(request, id):
#     if request.user.is_authenticated:
#         user_id = request.user.id
#         user = User.objects.get(id=user_id)

#         if user.is_staff and user.is_superuser:
#             try:
#                 update_role = UserRoles.objects.get(ID=id)
#                 update_role.IsActive = False
#                 update_role.UpdatedBy = request.user.username
#                 update_role.UpdatedDate = datetime.datetime.now()
#                 update_role.save()

#                 messages.success(request, f"{update_role.Name} has been deleted successfully from the system.")
#                 return redirect('tables')
#             except UserRoles.DoesNotExist:
#                 raise Http404("Role does not exist")
            
            
#         else:
#             messages.error(request, 'You do not have permission to perform this action!')
#             return redirect('home')
#     else:
#         pass  # Handle authentication failure if needed
