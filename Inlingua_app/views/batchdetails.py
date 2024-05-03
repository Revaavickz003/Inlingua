from django.shortcuts import render, redirect
from django.contrib import messages
from Inlingua_app.models import User, TrainingStaff, TrainerQualifications, TrainingBatches, Message
import datetime
from django.urls import reverse

def batches(request, id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        if user.is_staff:
            Training_Batches = TrainingBatches.objects.get(ID=id)
            if request.method == 'POST':
                print("Yes")
                Class_completed = request.POST.get('Class_completed')
                Study_Material = request.FILES.get('Study_Material')
                Recorded_Session = request.FILES.get('Recorded_Session')
                Assessment = request.FILES.get('Assessment')

                print(Class_completed)
                print(Study_Material)
                print(Recorded_Session)
                print(Assessment)
                
                update_course = Training_Batches.Course_details
                print(update_course.Name)

                if Class_completed:
                    update_course.Course_status = Class_completed
                    update_course.save()
                    print("Class completed:", Class_completed)

                if Study_Material:
                    update_course.Course_status = Study_Material
                    update_course.save()
                    print("Study Material uploaded")

                if Recorded_Session:
                    update_course.Course_status = Recorded_Session
                    update_course.save()
                    print("Recorded Session uploaded")

                if Assessment:
                    update_course.Course_status = Assessment
                    print("Assessment uploaded")
                    update_course.save()


                print("Success")

                return redirect(reverse('batches', kwargs={'id': id}))
            else:
                trainer_details = TrainingStaff.objects.get(LoginId=user)
                trainer_qualifications = TrainerQualifications.objects.get(ID=trainer_details.ID)
                training_batches = TrainingBatches.objects.filter(TrainerId=trainer_details.ID)
                return render(request, 'inlingua/index.html', {
                    'user': user,
                    'trainer_details': trainer_details,
                    'trainer_qualifications': trainer_qualifications,
                    'training_batchess': training_batches,
                    'Training_Batches': Training_Batches,
                    'Notifcaions': Message.objects.filter(receiver=user, created_date__date=datetime.datetime.today())
                })
    else:
        messages.error(request, "Your account has been logged out. Please login.")
        return redirect('login')
