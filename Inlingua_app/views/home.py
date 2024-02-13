from django.shortcuts import render, redirect
from django.contrib import messages
from Inlingua_app.models import User, TrainingStaff, TrainerQualifications, TrainingBatches, StudentDetails, PaymentTypes

def home(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        if user.is_staff:
            if user.is_superuser and user.is_active:
                paymenttypes = PaymentTypes.objects.all()
                context={'User':user,
                         'Dashboard':'active',
                         'paymenttypes':paymenttypes}
                return render(request, 'inlingua/index.html',context)
            else:
                trainer_details = TrainingStaff.objects.get(LoginId=user)
                training_batches = TrainingBatches.objects.filter(TrainerId=trainer_details.ID)
                try:
                    trainer_qualifications = TrainerQualifications.objects.get(ID=trainer_details.ID)
                except:
                    pass

                start_times = training_batches.filter(TrainerId=trainer_details.ID).values_list('StartTime', flat=True)
                if start_times:
                    min_start_time = min(start_times)
                    today_first_batch = training_batches.filter(StartTime=min_start_time).first()

                else:
                    today_first_batch = None
                return render(request, 'inlingua/index.html', {
                    'user': user,
                    'trainer_details': trainer_details,
                    'training_batches': training_batches,
                    'today_first_batch':today_first_batch,
                })
        elif user.is_active:
            student_details = StudentDetails.objects.get(StudentID=user.id)
            training_batches = TrainingBatches.objects.get(ID = student_details.BatchID.ID)
            return render(request, 'inlingua/index.html', {
                'user': user,
                'student_details': student_details,
                'training_batches':training_batches,
            })
        else:
            messages.error(request, "Account is inactive.")
            return render(request, 'inlingua/index.html')
    else:
        messages.error(request, "Your account has been logged out. Please log in.")
        return redirect('login')
