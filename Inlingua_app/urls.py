from django.urls import path
from Inlingua_app.functions import (
login, 
home, 
register, 
logout, 
batchdetails, 
user, 
tables, 
language as lng, 
trainers, 
language_page, 
courceandlevels,
payment, 
Generate_Report,
trainer_head,
StartClass,
Message_page,
)
from django.contrib.auth import views as password_views
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('crm/login/', login.custom_login, name="login"),
    path('logout/', logout.custom_logout, name="logout"),
    path('', home.home, name="home"),

    path('crm/start_class/<int:id>/<int:classid>/', StartClass.classstart, name="start_class"),
    path('crm/end_class/<int:id>/<int:classid>/', StartClass.classend, name="endclass"),

    path('crm/home/students_online_status/', trainer_head.students, name="student_online"),
    path('crm/home/Batchlist/',  trainer_head.Batchlist, name="Batchlist"),

    path('crm/students/', user.user_page, name="students"),
    path('crm/students/add/', user.addstudent, name="addstudent"),
    path('crm/student/<int:id>/', user.student_details, name="studentdetails"),
    path('crm/student/profileupdate/<int:id>/', user.profileupdate, name="profileupdate"),
    path('crm/student/studentbatchdetals/<int:id>/', user.studentbatchdetals, name="studentbatchdetals"),
    path('crm/student/basic_details_update/<int:id>/', user.basic_details_update, name="basicdetailsupdate"),

    path('crm/students/payment/<int:id>/', payment.payment_view, name='payment'),
    path('crm/students/payment/history/<int:id>/', payment.history_view, name='history'),
    path('crm/students/payment/history/report/<int:id>/', Generate_Report.GenerateReport, name='generatereport'),

    path('crm/trainers/', trainers.trainers_view, name="trainers"),
    path('crm/trainers/addtrainers/', trainers.add_trainers, name="addtrainers"),
    path('crm/trainers/<int:id>/', trainers.trainer_view, name="trainer"),
    path('crm/student/trainerprofile/<int:id>/', trainers.trainerprofileupdate, name="trainerprofile"),
    path('crm/student/trainerbasicdetails/<int:id>/', trainers.trainerbasicdetailsupdate, name="trainerbasicdetails"),
    path('crm/trainers/addhead/<int:id>/', trainers.add_trainer_head, name="addhead"),
    path('crm/trainers/removehead/<int:id>/', trainers.remove_trainer_head, name="removehead"),

    path('crm/tables/', tables.table_page, name="tables"),
    path('crm/tables/addlanguage/', lng.language_view, name="language"),
    path('crm/tables/addlanguage/add/', lng.add_language, name="add_language"),
    path('crm/tables/language/<int:id>/', lng.edit_lang, name="edit_lang"),
    path('crm/tables/language/delete/<int:id>/', lng.delete_langu, name="delete_langu"),

    path('crm/courceandlevels_table/', courceandlevels.table_page, name="courceandlevels_table"),
    path('crm/courceandlevels_table/batchs/<int:id>/', courceandlevels.edit_batchs, name="edit_batchs"),
    path('crm/courceandlevels_table/cources/<int:id>/', courceandlevels.edit_cources, name="edit_cources"),
    path('crm/courceandlevels_table/level/<int:id>/', courceandlevels.edit_level, name="edit_level"),

    path('crm/courceandlevels_table/add_level/', courceandlevels.add_level, name="add_level"),
    path('crm/courceandlevels_table/add_course/', courceandlevels.add_course, name="add_course"),
    path('crm/courceandlevels_table/add_batchs/', courceandlevels.add_batchs, name="add_batchs"),

    path('crm/language/<str:name>/', language_page.language_view, name="language_view"),

    path('crm/batch/<int:id>/', batchdetails.batches, name="batches"),
    path('crm/user/register/', register.register, name="register"),

    path('user/message/', Message_page.message_view, name="Message_page"),
    path('user/message/<str:username>/', Message_page.Message_for_user, name="Message_for_user"),

    # Reset the password urls

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)