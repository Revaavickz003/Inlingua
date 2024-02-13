# admin.py

from django.contrib import admin
from .models import (
    Languages, Level, Courses, PaymentTypes, Payments,
    UserRoles, User, ManagementStaff, TrainingStaff, TrainerQualifications,
    ProofOfIdentty, TrainingBatches, StudentBatchAllocation, CourseStatus,
    StudentDetails, StudentStudyMetirials, PaymentStatus, PaymentMethod
)
@admin.register(PaymentStatus)
class PaymentStatusAdmin(admin.ModelAdmin):
    list_display = ['StatusName',]
   

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display=['Name',]

@admin.register(Languages)
class LanguagesAdmin(admin.ModelAdmin):
    pass

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    pass

@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    pass

@admin.register(PaymentTypes)
class PaymentTypesAdmin(admin.ModelAdmin):
    pass

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    pass

@admin.register(UserRoles)
class UserRolesAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(ManagementStaff)
class ManagementStaffAdmin(admin.ModelAdmin):
    pass

@admin.register(TrainingStaff)
class TrainingStaffAdmin(admin.ModelAdmin):
    pass

@admin.register(StudentStudyMetirials)
class StudentStudyMetirialsAdmin(admin.ModelAdmin):
    list_display = ()

@admin.register(TrainerQualifications)
class TrainerQualificationsAdmin(admin.ModelAdmin):
    list_display = ('LanguageID',)

@admin.register(StudentDetails)
class StudentDetailsAdmin(admin.ModelAdmin):
    list_display = ('StudentID',)
    

@admin.register(ProofOfIdentty)
class ProofOfIdenttyAdmin(admin.ModelAdmin):
    pass

@admin.register(TrainingBatches)
class TrainingBatchesAdmin(admin.ModelAdmin):
    pass

@admin.register(StudentBatchAllocation)
class StudentBatchAllocationAdmin(admin.ModelAdmin):
    pass

@admin.register(CourseStatus)
class CourseStatusAdmin(admin.ModelAdmin):
    pass
