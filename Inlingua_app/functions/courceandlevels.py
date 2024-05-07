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
                training_staff = TrainerQualifications.objects.filter(TrainerHead=False)
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
                if batchname == "":
                    batchname = None
                    messages.error(request, 'add batch name')
                   
                Courses_Details = request.POST['Courses_Details']
                if Courses_Details == '':
                    Courses_Details = None
                    messages.error(request, 'add courses details')
                   
                Trainer = request.POST['Trainer']
                if Trainer == '':
                    Trainer = None
                    messages.error(request, 'Trainer')
                   
                try:
                    Courses_Details = Courses.objects.get(ID = int(Courses_Details))
                    Trainer = TrainingStaff.objects.get(ID = int(Trainer))
                
                    new_batch = TrainingBatches.objects.create(
                        Name = batchname,
                        Course_details = Courses_Details,
                        TrainerId = Trainer,
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
                
                try:
                    Courses_Details = Courses.objects.get(ID = int(Courses_Details))
                except:
                    Courses_Details = None
                try:
                    Trainer = TrainingStaff.objects.get(ID = int(Trainer))
                except:
                    Trainer = None
                try:
                    updatebatch = TrainingBatches.objects.get(ID = id)
                except:
                    updatebatch = None
                if batchname != '' :
                    updatebatch.Name = batchname
                    updatebatch.Course_details = Courses_Details
                    updatebatch.TrainerId = Trainer
                    updatebatch.UpdatedBy=user.name
                    updatebatch.UpdatedDate= datetime.datetime.now()
                    updatebatch.save()
                    messages.info(request,"The Batch has been updated successfully")
                    return redirect('courceandlevels_table')
                else:
                    messages.error(request,"Please fill all the fields")
                    return redirect('courceandlevels_table')
            else:
                batch_info = TrainingBatches.objects.get(ID=id)
                all_course = Courses.objects.all()
                all_Trainer = TrainingStaff.objects.all()
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
                    if course_name == '':
                        course_name = None
                        messages.error(request,  "Please enter course name")
                    
                    language_details = request.POST['languageid']
                    if language_details == '':
                        language_details = None
                        messages.error(request,  "Please enter language name")
                    
                    course_duration = request.POST['duration']
                    if course_duration == '':
                        course_duration = None
                        messages.error(request,  "Please enter course duration")
                    
                    cost = request.POST['cast']
                    if cost == '':
                        cost = None
                        messages.error(request,  "Please enter course cost")

                    start_date = request.POST['satrdate']
                    if start_date == '':
                        start_date = None
                        messages.error(request,  "Please enter course start date")
                    
                    end_date = request.POST['EndDate']
                    if end_date == '':
                        end_date = None
                        messages.error(request,  "Please enter course end date")
                    
                    start_time = request.POST['start_time']
                    if start_time == '':
                        start_time = None
                        messages.error(request,  "Please enter course start time")
                    
                    end_time = request.POST['end_time']
                    if end_time == '':
                        end_time = None
                        messages.error(request,  "Please enter course end time")
                    
                    course_metirials = request.POST['coursemetrials']
                    if course_metirials == '':
                        course_metirials = None
                        messages.error(request,  "Please enter course metrials")
                    
                    
                    duscription = request.POST['Duscription']
                    if duscription == '':
                        duscription = None
                        messages.error(request,  "Please enter course duscription")

                    level_id = request.POST['levelid']
                    if level_id == '':
                        level_id = None
                        messages.error(request,  "Please enter course Level")

                    try:
                        language_details = Languages.objects.get(ID=int(language_details))
                        level_id = Level.objects.get(ID=int(level_id))
                    
                        new_courses = Courses.objects.create(

                            Name = course_name,
                            Description = duscription,
                            Duration = course_duration,
                            LanguageID =language_details,
                            LevelID = level_id,
                            StartDate = start_date,
                            EndtDate = end_date,
                            StartTime = start_time,
                            EndTime = end_time,
                            Cost = cost,
                            Course_link = course_metirials,
                            CreatedBy=user.username,
                            UpdatedBy=user.username,
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
                try:
                    level = Level.objects.get(ID = int(level))
                except:
                    messages.error(request, "Select Level")
                    return redirect('courceandlevels_table')
                try:
                    language = Languages.objects.get(ID = int(language))
                except:
                    messages.error(request, "Select Language")
                    return redirect('courceandlevels_table')

                if coursename != '':
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
                    messages.info(request,"Fill correct details...")
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
                            CreatedBy=request.user.name,
                            UpdatedBy=request.user.name,
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
                    if level_name != '' and level_code != '':
                        level_updated = Level.objects.get(ID=id)
                        level_updated.Name = level_name
                        level_updated.Code = level_code
                        level_updated.UpdatedBy = user.name
                        level_updated.UpdatedDate = datetime.datetime.now()
                        level_updated.save()
                        messages.success(request,"Level has been updated Successfully")
                        return redirect('courceandlevels_table')
                    else:
                        messages.success(request,"Fill all details")
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