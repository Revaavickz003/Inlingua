from django.shortcuts import render, redirect
from django.contrib import messages
from Inlingua_app.models import User, TrainingStaff, TrainerQualifications, TrainingBatches

def batches(request,id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        if user.is_staff == True:
            trainer_details = TrainingStaff.objects.get(LoginId=user)
            trainer_qualifications = TrainerQualifications.objects.get(ID = trainer_details.ID)
            training_batches = TrainingBatches.objects.filter(TrainerId=trainer_details.ID)
            Training_Batches = TrainingBatches.objects.get(ID = id)
            return render(request, 'inlingua/index.html',
        {
        'user': user,
        'trainer_details':trainer_details,
        'trainer_qualifications':trainer_qualifications,
        'training_batches':training_batches,
        'Training_Batches':Training_Batches,
        })
    else:
        messages.error(request, "Your account as been logout Please login...!")
        return redirect('login')
