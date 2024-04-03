from django.shortcuts import render, redirect
from django.urls import reverse
from Inlingua_app.models import User, Payments, Courses, StudentDetails, PaymentMethod, PaymentTypes, PaymentStatus, Discount
import datetime
from django.db.models import Sum
from django.contrib  import messages

def addpaymenttypes(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_staff and user.is_superuser:
            if request.method == 'POST':
                PaymentTypesName = request.POST['PaymentTypes']
                if PaymentTypesName:
                    if not  PaymentTypes.objects.filter(Name=PaymentTypesName).exists():
                        new_type = PaymentTypes.objects.create(
                            Name = PaymentTypesName,
                            CreatedBy =  user.name,
                            UpdatedBy = user.name
                        )
                        new_type.save()
                        messages.success(request,  "New payment type added successfully")
                        return redirect('home')
                    else:
                        messages.warning(request,"This payment type already exists.")
                        return redirect('home')
                else:
                    messages.error(request, "Please enter a valid name for the payment type.")
                    return redirect('home')
            else:
                messages.error(request,  "Invalid Request! Please use POST method to add a new payment type.")
                return redirect('home')
        else:
            messages.info(request, "You do not have permission to view this page.")
            return redirect('login')
    else:
        messages.info(request, "Please login to access this feature.")
        return redirect('login')

def addpaymentmethod(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_staff and user.is_superuser:
            if request.method == 'POST':
                Paymentmethod = request.POST.get('PaymentMethod')
                if Paymentmethod:
                    if not PaymentMethod.objects.filter(Name=Paymentmethod).exists():
                        new_type = PaymentMethod.objects.create(
                            Name=Paymentmethod,
                            CreatedBy=user.name,
                            UpdatedBy=user.name
                        )
                        new_type.save()
                        messages.success(request, "New payment type added successfully")
                        return redirect('home')
                    else:
                        messages.warning(request, "This payment type already exists.")
                        return redirect('home')
                else:
                    messages.error(request, "Please enter a valid name for the payment type.")
                    return redirect('home')
            else:
                messages.error(request, "Invalid Request! Please use POST method to add a new payment type.")
                return redirect('home')

        else:
            messages.info(request, "You do not have permission to view this page.")
            return redirect('login')
    else:
        messages.info(request, "Please login to access this feature.")
        return redirect('login')

def payment_view(request,id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        if user.is_staff and user.is_superuser:
            paymentmethod = PaymentMethod.objects.all()
            paytypes = PaymentTypes.objects.all()
            paymentstatus = PaymentStatus.objects.all()
            history = Payments.objects.filter(StudentDetails=id)
            student_details = StudentDetails.objects.get(ID = id)
            total_amount = history.aggregate(Sum('Amount'))['Amount__sum'] or 0
            Course_cost = student_details.BatchID.Course_details.Cost
            pending_amountprint = float(student_details.BatchID.Course_details.Cost)-float(total_amount)

            try:
                discountprice = Discount.objects.get(StudentDetails=id)
                discount = discountprice.DiscountedPayment
            except Exception as e:
                discount = 0
                
                                                                                 
            if request.method == 'POST':
                PaymentTypeId = request.POST.get('PaymentTypeId')
                PaymentMethodId   = request.POST.get('PaymentMethodId')
                TransactionId  = request.POST.get('TransactionId')
                Amount  = request.POST.get('Amount')
                IsDiscountApplied  = request.POST.get('Discount')
                DiscountedPayment  = request.POST.get('DiscountedPayment')
                Description  = request.POST.get('Description')

                studentdetails = StudentDetails.objects.get(ID = id)
                course = Courses.objects.get(ID = int(studentdetails.BatchID.Course_details.ID))
                PaymentTypeId = PaymentTypes.objects.get(ID = int(PaymentTypeId))
                PaymentMethodId = PaymentMethod.objects.get(ID = int(PaymentMethodId))

                if float(Amount) + float(total_amount) + float(discount) == int(Course_cost):
                    Paymentstatus = PaymentStatus.objects.get(StatusName = 'Completed')
                    
                else:
                    Paymentstatus = PaymentStatus.objects.get(StatusName = 'Pending')
                
                if float(Amount) <= int(Course_cost) and int(pending_amountprint) >= float(Amount):
                    messages.warning(request,'The amount should be less than or equal to the course cost.')
                    pass
                else:
                    messages.warning(request,"Invalid transaction details entered!")
                    return render(request,'inlingua/payment.html')
                                               
                if IsDiscountApplied == "on":
                    new_discount = Discount.objects.create(
                        StudentDetails = studentdetails,
                        IsDiscountApplied = True,
                        DiscountedPayment = DiscountedPayment,
                        Description = Description,
                        CreatedBy = user.name,
                    )
                    new_discount.save()

                new_payment = Payments.objects.create(
                StudentDetails = studentdetails,
                PaymentTypeId = PaymentTypeId,
                PaymentMethodId = PaymentMethodId ,
                CourseId = course,
                TransactionId = TransactionId,
                Amount = float(Amount),
                PaymentStatus = Paymentstatus,
                CreatedBy = user.name,
                UpdatedBy = user.name,
                )
                new_payment.save()
                messages.success(request, f'Hello  {user.username}, {studentdetails.StudentID.name} payment {Amount} has been added successfully!')
                return redirect('students')
        context ={
            'User': user,
            'Students':'active',
            'student_details':student_details,
            'paymentmethod':paymentmethod,
            'paytypes':paytypes,
            'paymentstatus':paymentstatus,
            'discount':discount,
        }
        return render(request,'inlingua/payment.html',context)

def history_view(request,id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        history = Payments.objects.filter(StudentDetails=id)
        try:
            discount = Discount.objects.get(StudentDetails=id)
        except Exception as e:
            discount = None
        student_details = StudentDetails.objects.get(ID = id)
        total_amount = history.aggregate(Sum('Amount'))['Amount__sum'] or 0
        pending_amountprint = float(student_details.BatchID.Course_details.Cost)-float(total_amount)
        if discount != None:
            pending_amountprint = float(student_details.BatchID.Course_details.Cost)-float(total_amount)-float(discount.DiscountedPayment)
        try:
            last_history = history.last()
        except:
            pass
        context = {
            'User': user,
            'Students':'active',
            'history':history,
            'student_details':student_details,
            'last_history':last_history,
            'total_amount': total_amount,
            'discount':discount,
            'pending_amountprint':pending_amountprint,
        }
        return render (request, 'inlingua/history.html', context)

def payment_type(request, id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_staff:
            if user.is_superuser and user.is_active:
                paymenttypes = PaymentTypes.objects.get(ID=id)
                context={'User':user,
                         'Dashboard':'active',
                         'paymenttypes':paymenttypes}
                return render(request,'inlingua/paymenttype.html', context)
        
def payment_method(request, id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_staff:
            if user.is_superuser and user.is_active:
                paymentmethod = PaymentMethod.objects.get(ID=id)
                context={'User':user,
                         'Dashboard':'active',
                         'paymentmethod':paymentmethod}
                return render(request,'inlingua/paymentmethod.html', context)