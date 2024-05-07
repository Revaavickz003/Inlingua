from django.shortcuts import render, redirect
from Inlingua_app.models import User, Payments, Courses, StudentDetails, PaymentStatus, Discount
from django.db.models import Sum
from django.contrib  import messages

def payment_view(request,id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        if user.is_staff and user.is_superuser:
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
                try:
                    PaymentTypeId = request.POST.get('PaymentTypeId')
                    PaymentMethodId = request.POST.get('PaymentMethodId')
                    TransactionId = request.POST.get('TransactionId')
                    Amount = request.POST.get('Amount')
                    IsDiscountApplied = request.POST.get('Discount')
                    DiscountedPayment = request.POST.get('DiscountedPayment')
                    Description = request.POST.get('Description')

                    print(PaymentTypeId)
                    studentdetails = StudentDetails.objects.get(ID=id)
                    course = Courses.objects.get(ID=int(studentdetails.BatchID.Course_details.ID))
        
                    if float(Amount) + float(total_amount) + float(discount)  == int(Course_cost):
                        Paymentstatus, created = PaymentStatus.objects.get_or_create(StatusName='Completed', defaults={'CreatedBy': 'System', 'UpdatedBy': 'System'})
                    else:
                        Paymentstatus, created = PaymentStatus.objects.get_or_create(StatusName='Pending', defaults={'CreatedBy': 'System', 'UpdatedBy': 'System'})

                    if float(Amount) <= int(Course_cost) and int(pending_amountprint) >= float(Amount):
                        pass
                    else:
                        messages.warning(request, "Invalid transaction details entered!")
                        return render(request, 'inlingua/payment.html')

                    if IsDiscountApplied == "on":
                        new_discount = Discount.objects.create(
                            StudentDetails=studentdetails,
                            IsDiscountApplied=True,
                            DiscountedPayment=DiscountedPayment,
                            Description=Description,
                            CreatedBy=user.name,
                        )
                        new_discount.save()
                    if TransactionId != '' and PaymentMethodId != 'Select a payment' and PaymentTypeId != 'PaymentTypeId' :
                        new_payment = Payments.objects.create(
                            StudentDetails=studentdetails,
                            PaymentType=PaymentTypeId,
                            PaymentMethod=PaymentMethodId,
                            CourseId=course,
                            TransactionId=TransactionId,
                            Amount=float(Amount),
                            PaymentStatus=Paymentstatus,
                            CreatedBy=user.name,
                            UpdatedBy=user.name,
                        )
                        new_payment.save()
                        messages.success(request, f'Hello {user.username}, {studentdetails.StudentID.name} payment {Amount} has been added successfully!')
                        return redirect('students')
                    else:
                        messages.error(request, 'Fill all details ')
                        return redirect('students')
                except Exception as e:
                    messages.error(request, f'Hello {user.username},{e}')
                    return redirect('students')
        context ={
            'User': user,
            'Students':'active',
            'student_details':student_details,
            'paymentstatus':paymentstatus,
            'discount':discount,
            'payment_type_choices': Payments.PAYMENT_TYPE,
            'payment_method_choices': Payments.PAYMENT_MENTHOD,
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
