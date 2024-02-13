from django.shortcuts import render, redirect
from django.contrib import messages
from Inlingua_app.models import User, Languages, TrainerQualifications

def language_view(request,name):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_staff and  user.is_superuser:
            try:
                languages = Languages.objects.get(Name = name)
                trainers = TrainerQualifications.objects.filter(LanguageID=languages.ID)
            except Languages.DoesNotExist:
                errormess = f'Invalid Language! Create a language: {name}'
                messages.error(request, errormess)
                return redirect('tables')
            Trainers = TrainerQualifications.objects.filter(LanguageID = languages.ID)
            context = {'User': user,
                        'Trainers':'active',
                        'languages':languages, 
                        'Trainer':Trainers}
            return render(request, "inlingua/language_page.html",context)
        else:
            messages.error(request, 'Sorry')
            return redirect('home')
    else:
        messages.error(request, 'First you login')
        return redirect('login')