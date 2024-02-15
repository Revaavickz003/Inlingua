from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from io import BytesIO
from Inlingua_app.models import StudentDetails, Payments

def GenerateReport(request, id):
    # Fetch student details
    student_details = StudentDetails.objects.get(ID=id)
    
    # Fetch payment history for the student
    history = Payments.objects.filter(StudentDetails=student_details).order_by('-PaymentDate')

    # Calculate total payment
    total_payment = student_details.BatchID.Course_details.Cost

    # Calculate total paid amount
    total_paid_amount = sum(payment.Amount for payment in history)

    # Calculate pending amount
    pending_amount = total_payment - total_paid_amount

    # Render HTML template with student details and payment history
    html_content = render_to_string('inlingua/report.html', {
        'student_details': student_details,
        'history': history,
        'total_payment': total_payment,
        'total_paid_amount': total_paid_amount,
        'pending_amount': pending_amount,
    })

    # Create PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="student_report_{student_details.StudentID.name}.pdf"'

    # Create PDF using ReportLab
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, "Student Transaction Report")
    p.drawString(100, 730, f"Welcome to {student_details.StudentID.name} transactions")
    p.drawString(100, 710, f"Total Payment: Rs. {total_payment}")
    p.drawString(100, 690, f"Total Paid Amount: Rs. {total_paid_amount}")
    p.drawString(100, 670, f"Pending Amount: Rs. {pending_amount}")
    p.drawString(100, 650, "Payment History:")
    y = 630
    for i, data in enumerate(history, start=1):
        p.drawString(100, y, f"{i}. Transaction ID: {data.TransactionId}")
        p.drawString(300, y, f"Mode: {data.PaymentTypeId}")
        p.drawString(500, y, f"Date and Time: {data.PaymentDate.strftime('%b. %d, %Y, %I:%M %p')}")
        p.drawString(700, y, f"Amount: Rs. {data.Amount}")
        p.drawString(900, y, f"Payment Status: {data.PaymentStatus}")
        y -= 20
    p.showPage()
    p.save()

    # Return PDF response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
