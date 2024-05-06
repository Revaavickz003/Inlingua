from django.shortcuts import render
from django.contrib import messages
from Inlingua_app.models import User, TrainingStaff, TrainerQualifications, StudentDetails, Message
import datetime
def students(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_staff_head and user.is_active:
            trainer_details = TrainingStaff.objects.get(LoginId=user)
            Trainer_Qualifications = TrainerQualifications.objects.get(TrainerId=trainer_details)
            students = StudentDetails.objects.filter(Language_Id=Trainer_Qualifications.LanguageID)
                        
            return render(request, 'inlingua/index.html', {
                'user': user,
                'trainer_details': trainer_details,
                'Trainer_Qualifications': Trainer_Qualifications,
                'students': students,
                'student':'active',
                'Notifcaions': Message.objects.filter(receiver=user, created_date__date=datetime.datetime.today()),
            })

def Batchlist(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_staff_head and user.is_active:
            trainer_details = TrainingStaff.objects.get(LoginId=user)
            Trainer_Qualifications = TrainerQualifications.objects.get(TrainerId=trainer_details)
            trainers = TrainerQualifications.objects.filter(LanguageID=Trainer_Qualifications.LanguageID).exclude(userid=Trainer_Qualifications.userid)
            return render(request, 'inlingua/index.html', {
                'batchlist':'active',
                'user': user,
                'trainer_details': trainer_details,
                'Trainer_Qualifications': Trainer_Qualifications,
                'Notifcaions': Message.objects.filter(receiver=user, created_date__date=datetime.datetime.today()),
                'trainers': trainers,})