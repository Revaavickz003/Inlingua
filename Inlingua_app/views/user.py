from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from Inlingua_app.models import (User, TrainingStaff, StudentDetails, 
                                 UserRoles, StudentDetails, TrainingBatches, 
                                 Payments,)
import datetime
from itertools import zip_longest
from django.db.models import Max

def user_page(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        Student_details = StudentDetails.objects.all()
        Training_staff = TrainingStaff.objects.all()
        latest_payments = Payments.objects.values('StudentDetails').annotate(last_updated=Max('UpdatedDate'))
        latest_payment_details = Payments.objects.filter(
            StudentDetails__in=[payment['StudentDetails'] for payment in latest_payments],
            UpdatedDate__in=[payment['last_updated'] for payment in latest_payments]
        )
        
        zipped_data = zip_longest(Student_details, latest_payment_details)
        context = {'User': user,
                'Student_details':Student_details,
                'Training Staff': Training_staff,
                'zipped_data': zipped_data,
                'Students':'active'}
        return render(request, "inlingua/user.html",context)

def student_details(request,id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        try:
            student_details = StudentDetails.objects.get(ID = id)
            batches =  TrainingBatches.objects.all()
        except:
            messages.error(request,  'No such student details found')
            return redirect('students')
        context = {
            'Students':'active',
            'User':user,
            'batches':batches,
            'student_details':student_details,
        }
    return render(request, "inlingua/student_details.html",context)

def addstudent(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_staff and user.is_staff and user.is_superuser:
            if request.method == 'POST':
                name = request.POST.get('name')
                firstname = request.POST.get('fname')
                lasttname = request.POST.get('lname')
                Email = request.POST.get('gmail')
                mobilenumber = request.POST.get('mobilenumber')
                studentphoto = request.FILES.get('studentphoto')
                password1 = Email
                Batchid = request.POST.get('Batchid')
                studentid = request.POST.get('studentid')
                address = request.POST.get('Address')
                Batchid = TrainingBatches.objects.get(ID = Batchid)
                if not StudentDetails.objects.filter(userid = studentid).exists():
                    if not User.objects.filter(email=Email).exists():
                        try:
                            role_id = UserRoles.objects.get(Name ='Student'),
                        except:
                            messages.error(request,  "Role not found")
                            return redirect('students')
                        
                        newstudent = User.objects.create(
                            name = name,
                            first_name = firstname,
                            last_name = lasttname,
                            Mobile_Number = mobilenumber,
                            email = Email,
                            username = Email,
                            Address = address,
                            user_img = studentphoto,
                            created_by = user.name,
                            updated_by = user.name,
                            updated_date = datetime.datetime.now(),
                            role_id = UserRoles.objects.get(Name ='Student'),
                        )
                        newstudent.set_password(password1)
                        newstudent.save()
                    
                        lastuser = User.objects.last()
                        new_student_details = StudentDetails.objects.create(
                            StudentID = lastuser,
                            BatchID = Batchid,
                            userid = studentid,
                        )
                        new_student_details.save()
                        messages.success(request, "Registration successful. You can now log in.")
                        return redirect('students')
                    else:
                        messages.warning(request,"This email is already registered! Please login instead of registration.")
                        return redirect('addstudent')
                else:
                    messages.warning(request,"This student ID already exists.")
                    return redirect('addstudent')
            else:
                batches = TrainingBatches.objects.all()
                context = {
                    'User':user,
                    'Students':'active',
                    'batches':batches,
                    }
                return render(request, 'inlingua/addstudent.html',context)
        else:
            messages.error(request, "Sorry Your not a admin so plz login admin cridanceals.")
            return redirect('logout')
    else:
        messages.error(request,  "Please fill out the form correctly")
        return redirect('login')

def profileupdate(request, id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_staff and user.is_staff and user.is_superuser:
            if request.method == 'POST':
                profile = request.FILES.get('changeimg')
                if profile:
                    changeprofile = User.objects.get(id = id)
                    changeprofile.user_img =  profile
                    changeprofile.save()
                    messages.success(request,  f"Profile picture updated successfully!")
                    return redirect('students')
                else:
                    messages.error(request,  "Image field is empty! Please select an image to update your profile picture.")
                    return redirect('students')
            else:
                user_detail = get_object_or_404(User, id=id)
                context={'User':user,'Users':user_detail}
                return render(request,'inlingua/admin-editProfile.html',context)
        else:
            messages.error(request, "You are not authorized to view this page ")
            return redirect('home')
    else:
        messages.info(request, "Please Login first!")
        return redirect('login')  
                
def basic_details_update(request, id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_staff and user.is_staff and user.is_superuser:
            if request.method == 'POST':
                studentname = request.POST.get('studentname')
                mobilenumber = request.POST.get('mobilenumber')
                fname = request.POST.get('fname')
                lname = request.POST.get('lname')
                email = request.POST.get('email')
                Location = request.POST.get('Location')
                
                if studentname and mobilenumber and email and Location :
                    getuser = User.objects.get(id = id)
                    getuser.name = studentname
                    getuser.Mobile_Number = mobilenumber
                    getuser.first_name = fname
                    getuser.last_name = lname
                    getuser.Address =  Location
                    if getuser.email ==  email:
                        pass
                    else:
                        if not User.objects.filter(email=email).exists():
                            getuser.email = email
                            getuser.save()
                        else:
                            messages.warning(request,"Email already exists.")
                            return redirect('students')
                    getuser.save()
                    messages.success(request,  f"Basic impermation details updated successfully")
                    return redirect('students')
                else:
                    messages.error(request,  "All fields must be filled out correctly.")
                    return redirect('students')
            else:
                user_detail = get_object_or_404(User, id=id)
                context={'User':user,'Users':user_detail}
                return render(request,'inlingua/admin-editProfile.html',context)
        else:
            messages.error(request, "You are not authorized to view this page ")
            return redirect('home')
    else:
        messages.info(request, "Please Login first!")
        return redirect('login')  
    
def studentbatchdetals(request, id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_staff and user.is_staff and user.is_superuser:
            if request.method == 'POST':
                batch = request.POST['Batchid']
                try:
                    getbatch = TrainingBatches.objects.get(ID = int(batch))
                except:
                    messages.error(request, "Invalid Batch ID")
                    return redirect('students')

                if getbatch:
                    updatestudent = StudentDetails.objects.get(StudentID=id)
                    updatestudent.BatchID = getbatch
                    updatestudent.StudentID.updated_by =  user.name
                    updatestudent.StudentID.updated_date =  datetime.datetime.now()
                    updatestudent.save()
                    messages.success(request,  f"Course details updated successfully")
                    return redirect('students')
                else:
                    messages.warning(request, 'Sorry Select a corrct Course')
                    return redirect('students')
            else:
                messages.error(request, "You are not authorized to view this page ")
                return redirect('home')
        else:
            messages.error(request, "You are not authorized to view this page ")
            return redirect('home')
    else:
        messages.info(request, "Please Login first!")
        return redirect('login')  