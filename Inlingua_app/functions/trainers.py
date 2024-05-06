import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from Inlingua_app.models import (User, Languages, TrainerQualifications, TrainingBatches, 
                                 StudentDetails, UserRoles,TrainingStaff, Level, UserRoles)

def trainers_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        
        if user.is_staff and user.is_superuser:
            languages = Languages.objects.all()
            levels = Level.objects.all()
            training_Staff = TrainerQualifications.objects.all()
            trainer_heads = TrainerQualifications.objects.filter(TrainerHead = True)
            context = {'User': user,
                       'trainer_heads':trainer_heads,
                       'languages': languages, 
                       'training_Staff':training_Staff,
                       'levels':levels,
                       'Trainers':'active'}
            return render(request, "inlingua/trainers.html",context)
        else:
            messages.error(request,"You do not have permission to view this page.")
            return redirect('home')
    else:
        messages.error(request,  "Please login first")
        return redirect('login')
                     
def trainer_view(request,id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        if user.is_staff and user.is_superuser:
            try:
                training = TrainerQualifications.objects.get(ID=id)
            except:
                messages.warning(request, "No such trainer exists!")
                return redirect('trainers')
            training_batches = TrainingBatches.objects.filter(TrainerId = training.TrainerId.ID)
            Student_details = StudentDetails.objects.all()
            
            context = {'User': user,
                       'Trainers':'active',
                       'training':training,
                       'training_batches':training_batches,
                       'Student_details':Student_details,
                       }
            return render(request, "inlingua/trainers.html",context)
        else:
            messages.error(request,"You do not have permission to view this page.")
            return redirect('home')
    else:
        messages.error(request,  "Please login first")
        return redirect('login')

def add_trainer_head(request, id):
    if request.user.is_authenticated:
        user = request.user

        if user.is_staff and user.is_superuser:
            try:
                trainer_qualification = TrainerQualifications.objects.get(ID=id)
                training_batches = TrainingBatches.objects.filter(TrainerId = trainer_qualification.TrainerId)

                if not training_batches:
                    if TrainerQualifications.objects.filter(LanguageID=trainer_qualification.LanguageID, TrainerHead=True).exists():
                        messages.error(request, 'Already a Head Coach!')
                        return redirect('trainers')
                    else:
                        trainer_qualification.TrainerHead = True
                        trainer_qualification.TrainerId.LoginId.is_staff_head = True
                        trainer_qualification.TrainerId.LoginId.save()
                        trainer_qualification.save()

                        messages.success(request, 'Successfully made the Trainer as a Head Coach!')
                        return redirect('trainers')
                else:
                    messages.error(request, 'This trainer has a batch, so if you add this trainer to the head trainer, remove the batch and add the trainer.')
                    return redirect('trainers')
            except TrainerQualifications.DoesNotExist:
                messages.error(request, 'Trainer qualifications not found.')
                return redirect('trainers')
        else:
            messages.error(request, "You don't have permission for that action.")
            return redirect('home')
    else:
        messages.error(request, "Please log in first.")
        return redirect('login')
    
    

def remove_trainer_head(request,id):
    get_tainer_qualification = TrainerQualifications.objects.get(ID = id)
    get_tainer_qualification.TrainerHead = False
    get_tainer_qualification_loginid = User.objects.get(pk = get_tainer_qualification.TrainerId.LoginId.pk)
    get_tainer_qualification_loginid.is_staff_head = False
    get_tainer_qualification.save()
    get_tainer_qualification_loginid.save()
    return redirect('trainers')

def add_trainers(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        
        if user.is_staff and user.is_superuser:
            if request.method == 'POST':
                name = request.POST.get('trainername')
                if name == '':
                    name = None
                    messages.error(request, 'Enter the Name')

                firstname = request.POST.get('fname')
                if firstname == '':
                    firstname = None
                    messages.error(request, 'Enter the First Name')

                lasttname = request.POST.get('lname')
                if lasttname == '':
                    lasttname = None
                    messages.error(request, 'Enter the Last Name')

                email = request.POST.get('gmail')
                if email == '':
                    email = None
                    messages.error(request, 'Enter the mail')

                mobilenumber = request.POST.get('mobilenumber')
                if mobilenumber == '':
                    mobilenumber = None
                    messages.error(request, 'Enter the Mobile Number')

                trainer_photo = request.FILES.get('trainerphoto')
                password1 = email
                address = request.POST.get('Address')

                certificateNumber = request.POST.get('certificateNumber')
                if certificateNumber == '':
                    certificateNumber = None
                    messages.error(request, 'Enter the Certificate Number')

                certifyingAuthority = request.POST.get('certifyingAuthority')
                if certifyingAuthority == '':
                    certifyingAuthority = None
                    messages.error(request, 'Enter the Certifying Authority')

                certificateValidTill = request.POST.get('certificateValidTill')
                if certificateValidTill == '':
                    certificateValidTill = None
                    messages.error(request, 'Enter the Certificate Valid Till')

                language = request.POST.get('Language')
                if language == '':
                    language = None
                    messages.error(request, 'Enter the Language')

                level = request.POST.get('level')
                if level == '':
                    level = None
                    messages.error(request, '')
                    
                trainerid = request.POST.get('trainerid')

                try:
                    role = UserRoles.objects.get(Name='Trainer')
                except UserRoles.DoesNotExist:
                    role = UserRoles.objects.create(Name='Trainer',IsActive=True,CreatedBy=request.user,UpdatedBy=request.user)
                
                try:
                    new_trainer = User.objects.create(
                        name=name,
                        first_name=firstname,
                        last_name=lasttname,
                        Mobile_Number=mobilenumber,
                        email=email,
                        username=email,
                        user_img=trainer_photo,
                        Address=address,
                        created_by=request.user.username,
                        updated_by=request.user.username,
                        is_staff=True,
                        updated_date=datetime.datetime.now(),
                        role_id=role,
                    )
                    new_trainer.set_password(password1)
                    new_trainer.save()
                except Exception as e:
                    messages.error(request, f"{e}")
                    return redirect('trainers')
                try:
                    lastuser = User.objects.last()
                    new_trainer_details = TrainingStaff.objects.create(
                        Name = name,
                        EmailID = email,
                        LoginId = lastuser,
                        IsActive = True,
                        CreatedBy = user.name,
                        CreatedDate = datetime.datetime.now(),
                        UpdatedBy = user.name,
                        UpdatedDate = datetime.datetime.now(),
                    )
                    new_trainer_details.save()
                    Language = Languages.objects.get(ID = int(language))
                    level = Level.objects.get(ID = int(level))
                    lastuser = TrainingStaff.objects.last()
                    
                    new_trainer_qualification = TrainerQualifications.objects.create(
                        userid = trainerid,
                        LanguageID = Language,
                        LevelId = level,
                        CertificateNumber = certificateNumber,
                        CertifyingAuthority = certifyingAuthority,
                        CertificateValidTill = certificateValidTill,
                        TrainerId = lastuser,
                        CreatedBy = user.name,
                        CreatedDate = datetime.datetime.now(),
                        UpdatedBy = user.name,
                        UpdatedDate = datetime.datetime.now(),
                    )
                    new_trainer_qualification.save()
                except Exception as e:
                    messages.error(request, f"{e}")
                    return redirect('trainers')
                
                messages.success(request, "Registration successful Trainer "+ name +" Login to continue")
                return redirect('trainers')
            else:
                languages = Languages.objects.all()
                levels = Level.objects.all()
                context = {'User': user,
                           'languages': languages,
                           'levels':levels,
                           'Trainers':'active'}
                return render(request, 'inlingua/addtrainer.html', context)
        else:
            messages.error(request, "You do not have permission to add a trainer")
            return redirect('home')
    else:
        messages.warning(request, "Please login first!")
        return redirect('login')
    
def trainerprofileupdate(request, id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_staff and user.is_staff and user.is_superuser:
            if request.method == 'POST':
                profile = request.FILES.get('trainerprofile')
                if profile:
                    changeprofile = User.objects.get(id = id)
                    changeprofile.user_img =  profile
                    changeprofile.save()
                    messages.success(request,  f"Profile picture updated successfully!")
                    return redirect('trainers')
                else:
                    messages.error(request,  "Image field is empty! Please select an image to update your profile picture.")
                    return redirect('trainers')
            else:
                messages.error(request,  "No file selected.")
                return redirect('trainers')
        else:
            messages.error(request, "You are not authorized to view this page ")
            return redirect('home')
    else:
        messages.info(request, "Please Login first!")
        return redirect('login')  
    
def trainerbasicdetailsupdate(request,id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_staff and user.is_staff and user.is_superuser:
            if request.method == 'POST':
                trainername = request.POST.get('trainername')
                mobilenumber = request.POST.get('mobilenumber')
                email = request.POST.get('email')
                Location = request.POST.get('location')
                
                if trainername and mobilenumber and email and Location :
                    getuser = User.objects.get(id = id)
                    getuser.name = trainername
                    getuser.Mobile_Number = mobilenumber
                    getuser.Address =  Location
                    if getuser.email ==  email:
                        pass
                    else:
                        if not User.objects.filter(email=email).exists():
                            getuser.email = email
                            getuser.save()
                        else:
                            messages.warning(request,"Email already exists.")
                            return redirect('trainers')
                    getuser.save()
                    messages.success(request,  f"{trainername} Basic information details updated successfully")
                    return redirect('trainers')
                else:
                    messages.error(request,  "All fields must be filled out correctly.")
                    return redirect('trainers')
            else:
                messages.error(request,  "Invalid Request")
                return redirect('trainers')
        else:
            messages.error(request, "You are not authorized to view this page ")
            return redirect('home')
    else:
        messages.info(request, "Please Login first!")
        return redirect('login')  