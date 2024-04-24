from django.http import HttpResponse
from django.contrib import messages
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from Inlingua_app.models import StudentDetails, Payments, TrainingBatches, Discount
from django.templatetags.static import static
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Image

def add_watermark(canvas, doc):
    watermark_path = "static/img/imgs/logo.png"
    watermark_width, watermark_height = 400, 400 

    page_width, page_height = doc.width, doc.height
    x = (page_width - watermark_width) / 0.7
    y = (page_height - watermark_height) / 1.5

    canvas.drawImage(watermark_path, x, y, width=watermark_width, height=watermark_height, preserveAspectRatio=True, mask='auto')

def GenerateReport(request, id):
    student_details = StudentDetails.objects.get(ID=id)
    strudent_batch = TrainingBatches.objects.get(Name = student_details.BatchID)
    payments = Payments.objects.filter(StudentDetails_id=id)
    try:
        discount = Discount.objects.get(StudentDetails =  student_details)
        discount = discount.DiscountedPayment
    except Exception as e:
        discount = 0
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Inlingua_international_language_center_student_report_{student_details.StudentID.name}_{student_details.userid}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    logo_path = "static/img/imgs/l1.png"
    logo_img = Image(logo_path, width=2*inch, height=0.5*inch) 
    elements.append(logo_img)

    data = [
        ["Student ID", str(student_details.userid)],
        ["Name", student_details.StudentID.name],
        ["Mobile Number", str(student_details.StudentID.Mobile_Number)],
        ["Gmail", str(student_details.StudentID.username)],
        ["Address", str(student_details.StudentID.Address)],
    ]
    table = Table(data, colWidths=[2*inch, 4*inch])
    red_heading_style = ParagraphStyle(
            "RedHeading",
            parent=getSampleStyleSheet()["Heading2"],
            textColor="#FF751A"
        )
    elements.append(Spacer(0, 20))
    elements.append(Paragraph("Student Details:", red_heading_style))
    elements.append(table)

    data2 = [
        ["Trainer Name", strudent_batch.TrainerId.Name],
        ["Mobile Number", strudent_batch.TrainerId.LoginId.Mobile_Number],
        ["Email ID", strudent_batch.TrainerId.LoginId.username],
        ["Batch Name", strudent_batch.Name],
        ["Duration", strudent_batch.Duration],
        ["Language Name", strudent_batch.Course_details.LanguageID.Name],
        ["Language Level", strudent_batch.Course_details.LevelID.Name],
        ["Start Date", strudent_batch.Course_details.StartDate],
        ["End Date", strudent_batch.Course_details.EndtDate],
        ["Start Time", strudent_batch.Course_details.StartTime],
        ["End Time", strudent_batch.EndTime],
        
    ]
    table = Table(data2, colWidths=[2*inch, 4*inch])
    elements.append(Spacer(0, 20))
    elements.append(Paragraph("Course Details:", red_heading_style))
    elements.append(table)
    total_payment = sum(item.Amount for item in payments)
    data3 = [
            ["Cast", strudent_batch.Course_details.Cost],
            ["-----------------------------------------------------------"],
            ["Payment", total_payment],
            ["Discount", discount],
            ['-----------------------------------------------------------'],
            ['Total  Amount to be Paid', float(total_payment)+float(discount)],
            ['-----------------------------------------------------------'],
            ["Pending Payment", strudent_batch.Course_details.Cost-float(total_payment)-float(discount)],
        ]
    table = Table(data3, colWidths=[2*inch, 4*inch])
    elements.append(Spacer(0, 20))
    elements.append(Paragraph("Payment Details:", red_heading_style))
    elements.append(table)

    if payments.exists():
        payments_data = [
            [str(i+1), item.PaymentDate.strftime("%B %d, %Y"), item.Amount, item.PaymentStatus]
            for i, item in enumerate(payments)
        ]
        payments_table_data = [["#", "Payment Date", "Amount", "Payment Status"]] + payments_data
        payments_table = Table(payments_table_data, colWidths=[0.5*inch, 2*inch, 1.5*inch, 1.5*inch])
        payments_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#FF751A")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ]))
        elements.append(Paragraph("Payment History:", red_heading_style))
        elements.append(payments_table)
    else:
        elements.append(Paragraph("Payment History:", red_heading_style))
        elements.append(Paragraph("No payment details found.", red_heading_style))

    doc.build(elements, onFirstPage=add_watermark, onLaterPages=add_watermark)
    messages.success(request, "Report Download success fully ...")
    return response
