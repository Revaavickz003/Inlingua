from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib import messages
from django.urls import reverse
from Inlingua_app.models import User, Level, Courses, TrainingBatches,TrainingStaff, Languages, Courses, TrainerQualifications

def table_page(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        if user.is_staff:
            if user.is_superuser:
                All_batches = TrainingBatches.objects.all()
                All_courses = Courses.objects.all()
                All_level = Level.objects.all()
                All_languages = Languages.objects.all()
                training_staff = TrainerQualifications.objects.all()
                context = {'courceandlevels':'active',
                           'User': user, 
                           'All_batches': All_batches, 
                           'All_courses':All_courses,
                           'All_level':All_level,
                           'All_languages':All_languages,
                           'training_staff':training_staff,
                           }
                return render(request, "inlingua/courceandlevels.html",context)

            else:
                pass
        else:
            pass
    else:
        pass

import datetime

def add_batchs(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        if user.is_staff and user.is_superuser:
            if request.method == 'POST':
                batchname = request.POST['batchname']
                Courses_Details = request.POST['Courses_Details']
                Trainer = request.POST['Trainer']
                gmeeturl = request.POST['gmeeturl']
                stardate = request.POST['satrdate']
                EndDate = request.POST['EndDate']
                classduraition = request.POST['classduraition']
                start_time = request.POST['start_time']
                end_time = request.POST['end_time']
                end_time = request.POST['end_time']
                if type(Courses_Details) != int:
                    messages.error(request,"Please Select Course")
                else:
                    Courses_Details = Courses.objects.get(ID = int(Courses_Details))
                if type(Trainer) != int:
                    messages.error(request,"Please Select Trainer")
                else:
                    Trainer = TrainingStaff.objects.get(ID = int(Trainer))
                try:
                    new_batch = TrainingBatches.objects.create(
                        Name = batchname,
                        Course_details = Courses_Details,
                        TrainerId = Trainer,
                        MeetingURL = gmeeturl,
                        StartDate = stardate,
                        EndDate = EndDate,
                        Duration = classduraition,
                        StartTime = start_time,
                        EndTime = end_time,
                        IsActive = True,
                        CreatedBy=user.name,
                        CreatedDate= datetime.datetime.now(),
                        UpdatedBy=user.name,
                        UpdatedDate= datetime.datetime.now(),
                        )
                    new_batch.save()
                    messages.success(request,"New Batch Added Successfully")
                    return redirect('courceandlevels_table')
                except Exception as e:
                    messages.error(request, f"{e}")
                    return redirect('courceandlevels_table')
            else:
                return redirect('courceandlevels_table')
        else:
            messages.error(request,'You do not have permission to add a new Batch!')
            return redirect('home')
    else:
        messages.error(request,  "Unauthorized User! Please Login or Register.")
        return redirect('login')
    

def edit_batchs(request,id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        if user.is_staff and request.user.is_superuser:
            if request.method == 'POST':
                batchname = request.POST['batchname']
                Courses_Details = request.POST['Courses_Details']
                Trainer = request.POST['Trainer']
                gmeeturl = request.POST['gmeeturl']
                classduraition = request.POST['classduraition']
                
                Courses_Details = Courses.objects.get(ID = int(Courses_Details))
                Trainer = TrainingStaff.objects.get(ID = int(Trainer))
                updatebatch = TrainingBatches.objects.get(ID = id)
                updatebatch.Name = batchname
                updatebatch.Course_details = Courses_Details
                updatebatch.TrainerId = Trainer
                updatebatch.MeetingURL = gmeeturl
                updatebatch.Duration = classduraition
                updatebatch.UpdatedBy=user.name
                updatebatch.UpdatedDate= datetime.datetime.now()
                updatebatch.save()
                
                messages.info(request,"The Batch has been updated successfully")
                return redirect('courceandlevels_table')
            else:
                batch_info = TrainingBatches.objects.get(ID=id)
                all_course = Courses.objects.all()
                all_Trainer = TrainingStaff.objects.all()
                print(user.name)
                context = {
                        'courceandlevels':'active',
                           'BatchInfo': batch_info, 
                           'all_course':all_course, 
                           'all_Trainer':all_Trainer}
                context['url_with_id'] = reverse('edit_batchs', kwargs={'id': id})
                return render(request, "inlingua/courceandlevels.html", context)
        else:
            messages.error(request,  "You do not have permission to view this page.")
            return redirect('login')
    else:
        messages.error(request,  "Please login first!")
        return redirect('home')





def add_course(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        if user.is_staff:
            if user.is_superuser:
                if request.method == 'POST':
                    course_name = request.POST['coursename']
                    level_details = request.POST['levelid']
                    language_details = request.POST['languageid']
                    course_duration = request.POST['duration']
                    cost = request.POST['cast']
                    start_date = request.POST['satrdate']
                    end_date = request.POST['EndDate']
                    start_time = request.POST['start_time']
                    end_time = request.POST['end_time']
                    course_metirials = request.POST['coursemetrials']
                    course_status = request.POST['coursestatus']
                    duscription = request.POST['Duscription']
                    
                    if type(language_details) != int:
                        messages.error(request, "Select language")
                    else:
                        language_details = Languages.objects.get(ID=int(language_details))

                    if type(level_details) != int:
                        messages.error(request, "Select level")
                    else:
                        level_details = Level.objects.get(ID=int(level_details))
                    try:
                        new_courses = Courses.objects.create(
                            Name = course_name,
                            Description = duscription,
                            Duration = course_duration,
                            LanguageID =language_details,
                            StartDate = start_date,
                            EndtDate = end_date,
                            StartTime = start_time,
                            EndTime = end_time,
                            LevelID = level_details,
                            Cost = cost,
                            Course_metirials = course_metirials,
                            Course_status = course_status,
                            CreatedBy=user.name,
                            CreatedDate= datetime.datetime.now(),
                            UpdatedBy=user.name,
                            UpdatedDate= datetime.datetime.now(),
                            )
                        new_courses.save()
                        messages.success(request,"New Course added successfully")
                        return redirect('courceandlevels_table')
                    except Exception as e:
                        messages.error(request,f"{e}")
                        return redirect('courceandlevels_table')
                else:
                    return redirect('courceandlevels_table')
            else:
                messages.error(request,'You do not have permission to add a new co!')
                return redirect('home')
        else:
            messages.error(request,'You do not have permission to add a new Cource!')
            return redirect('home')
    else:
        messages.error(request,"Pls Enter you correct Email and Password")
        return redirect('login') 
                    
def edit_cources(request,id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_staff and request.user.is_superuser:
            if request.method == 'POST':
                coursename = request.POST['batchname']
                level = request.POST['Level_Details']
                language = request.POST['language_details']
                level = Level.objects.get(ID = int(level))
                language = Languages.objects.get(ID = int(language))
                updatecorse = Courses.objects.get(ID = id)
                updatecorse.Name = coursename
                updatecorse.LevelID = level
                updatecorse.LanguageID = language
                updatecorse.UpdatedBy=user.name
                updatecorse.UpdatedDate= datetime.datetime.now()
                updatecorse.save()
                messages.info(request,"Course has been updated Successfully.")
                return redirect('courceandlevels_table')
            else:
                try:
                    course_info = Courses.objects.get(ID=id)
                except:
                    messages.warning(request,"No such Course exists in the database.")
                    return redirect('courceandlevels_table')
                all_language = Languages.objects.all()
                all_level = Level.objects.all()
                context = {'User':user,
                           'courceandlevels':'active',
                           'course_info': course_info, 
                           'all_language':all_language, 
                           'all_level':all_level}
                context['url_with_id'] = reverse('edit_cources', kwargs={'id': id})
                return render(request, "inlingua/courceandlevels.html", context)
        else:
            return redirect('login_page')
    else:
        messages.error(request,"Plz Login")
        return redirect('login')   
        
def add_level(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        if user.is_staff:
            if user.is_superuser:
                if request.method == 'POST':
                    if Level.objects.filter(Name=request.POST['levelname']).exists():
                        messages.warning(request,"Level already exists in the database.")
                        return redirect('courceandlevels_table')
                    level_name = request.POST['levelname']
                    level_code = request.POST['levelcode']
                    if level_name !='' and level_code != '':
                        new_level = Level.objects.create(
                            Name=level_name, 
                            Code=level_code,
                            CreatedBy=user.name,
                            CreatedDate= datetime.datetime.now(),
                            UpdatedBy=user.name,
                            UpdatedDate= datetime.datetime.now(),
                            )
                        new_level.save()
                        messages.success(request,"New level added successfully")
                        return redirect('courceandlevels_table')
                    else:
                        messages.error(request, 'Fill all fields')
                        return redirect('courceandlevels_table')
                else:
                    return redirect('courceandlevels_table')
            else:
                messages.error(request,'You do not have permission to add a new level!')
                return redirect('home')
        else:
            messages.error(request,'You do not have permission to add a new level!')
            return redirect('home')
    else:
        messages.error(request,"Pls Enter you correct Email and Password")
        return redirect('login') 
                    
def edit_level(request,id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        if user.is_staff:
            if request.user.is_superuser:
                if request.method == 'POST':
                    level_name = request.POST['batchname']
                    level_code = request.POST['gmeeturl']

                    level_updated = Level.objects.get(ID=id)
                    level_updated.Name = level_name
                    level_updated.Code = level_code
                    level_updated.UpdatedBy = user.name
                    level_updated.UpdatedDate = datetime.datetime.now()
                    level_updated.save()
                    messages.success(request,"Level has been updated Successfully")
                    return redirect('courceandlevels_table')
                else:
                    try:
                        level_info = Level.objects.get(ID=id)
                    except:
                        messages.warning(request,"Level does not exist.")
                        return redirect('courceandlevels_table')
                    
                    context = {'courceandlevels':'active', 
                               'level_info': level_info}
                    context['url_with_id'] = reverse('edit_level', kwargs={'id': id})
                    return render(request, "inlingua/courceandlevels.html", context)
            else:
                return redirect('login_page')
        else:
            pass