from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import FileExtensionValidator
import datetime

class CustomUserManager(BaseUserManager):
    def _create_user(self, email=None, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

class Languages(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    IsActive = models.BooleanField(default=True)
    CreatedDate = models.DateTimeField(default=datetime.datetime.now())
    CreatedBy = models.CharField(max_length=255)
    UpdatedDate = models.DateTimeField(default=datetime.datetime.now())
    UpdatedBy = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

class Level(models.Model):
    ID = models.AutoField(primary_key=True)
    Code = models.CharField(max_length=2)
    Name = models.CharField(max_length=255)
    CreatedBy = models.CharField(max_length=255)
    CreatedDate = models.DateTimeField(default=datetime.datetime.now())
    UpdatedBy = models.CharField(max_length=255)
    UpdatedDate = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.Name

class Courses(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Description = models.TextField(max_length=255)
    Duration = models.IntegerField()
    LanguageID = models.ForeignKey(Languages, on_delete=models.CASCADE)
    LevelID = models.ForeignKey(Level, on_delete=models.CASCADE)
    StartDate = models.DateField(null=False, blank=False)
    EndtDate = models.DateField(null=False, blank=False)
    StartTime = models.TimeField(null=False, blank=False)
    EndTime = models.TimeField(null=False, blank=False)
    Course_link = models.URLField(null=False, blank=False)
    class_active = models.BooleanField(default=False)
    Cost = models.FloatField()
    Course_metirials = models.FileField(
        upload_to='Course/Study materials/',
        blank=True,
        null=True,
    )
    Assessment = models.FileField(
        upload_to='Course/Assessment/',
        blank=True,
        null=True,
    )
    Recorded_Session = models.FileField(
        upload_to='Course/Recorded_Session/',
        blank=True,
        null=True,
    )
    
    Course_status = models.IntegerField(default=0)
    CreatedDate = models.DateTimeField(default=datetime.datetime.now())
    CreatedBy = models.CharField(max_length=255)
    UpdatedDate = models.DateTimeField(default=datetime.datetime.now())
    UpdatedBy = models.CharField(max_length=255)
    
    def __str__(self):
        return self.Name
    
class PaymentStatus(models.Model):
    COMPLETED = 'Completed'
    PENDING = 'Pending'
    YET_TO_PAY = 'Yet to pay'

    STATUS_CHOICES = [
        (COMPLETED, 'Completed'),
        (PENDING, 'Pending'),
        (YET_TO_PAY, 'Yet to pay'),
    ]
    StatusName = models.CharField(max_length=255, choices=STATUS_CHOICES, default=YET_TO_PAY)
    CreatedDate = models.DateTimeField(default=datetime.datetime.now())
    CreatedBy = models.CharField(max_length=255)
    UpdatedDate = models.DateTimeField(default=datetime.datetime.now())
    UpdatedBy = models.CharField(max_length=255)

    def __str__(self):
        return self.StatusName

class Discount(models.Model):
    StudentDetails = models.ForeignKey('StudentDetails', on_delete=models.DO_NOTHING, null=True, blank=False)
    IsDiscountApplied = models.BooleanField()
    DiscountedPayment = models.FloatField(default=0)
    Description = models.TextField(null=True, blank=True)
    CreatedBy = models.CharField(max_length=255)
    CreatedDate = models.DateTimeField(default=datetime.datetime.now())
    UpdatedBy = models.CharField(max_length=255, null=True, blank=True)
    UpdatedDate = models.DateTimeField(null=True, blank=True)


class Payments(models.Model):
    GPay = 'G-Pay'
    PhonePay = 'Phone Pay'
    Paytm = 'Paytm'
    UPI = 'UPI'
    NetBank = 'NetBank'
    Creditcord = 'Credit Card'
    Debitcord = 'Debit Card'
    Sconer = 'Sconer'

    PAYMENT_TYPE = [
        (GPay, 'G-Pay'),
        (PhonePay, 'Phone Pay'),
        (Paytm, 'Paytm'),
        (UPI, 'UPI'),
        (NetBank, 'Net Bank'),
        (Creditcord, 'Credit Card'),
        (Debitcord, 'Debit Card'),
    ]

    Ready_Payment = 'Ready Payment'
    Parcial_Payment = 'Parcial Payment'
    PAYMENT_MENTHOD = [
        (Ready_Payment, 'Ready Payment'),
        (Parcial_Payment, 'Parcial Payment'),
    ]
    ID = models.AutoField(primary_key=True)
    StudentDetails = models.ForeignKey('StudentDetails', on_delete=models.CASCADE, null=False, blank=False)
    PaymentType = models.CharField(max_length=255, choices=PAYMENT_TYPE)
    PaymentMethod = models.CharField(max_length=255, choices=PAYMENT_MENTHOD)
    CourseId = models.ForeignKey(Courses, on_delete=models.CASCADE)
    PaymentDate = models.DateTimeField(default=datetime.datetime.now())
    TransactionId = models.CharField(max_length=100)
    Amount = models.DecimalField(max_digits=8, decimal_places=2,null=False, blank=False)
    PaymentStatus = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE,null=False, blank=False)
    CreatedBy = models.CharField(max_length=255)
    CreatedDate = models.DateTimeField(default=datetime.datetime.now())
    UpdatedBy = models.CharField(max_length=255, null=True, blank=True)
    UpdatedDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.StudentDetails)

class UserRoles(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Description = models.CharField(max_length=255)
    IsActive = models.BooleanField()
    CreatedBy = models.CharField(max_length=255)
    CreatedDate = models.DateTimeField(default=datetime.datetime.now())
    UpdatedBy = models.CharField(max_length=255)
    UpdatedDate = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.Name

class User(AbstractUser):
    name = models.CharField(max_length=225, blank=False, null=False)
    Mobile_Number = models.IntegerField(null=True, blank=True)
    user_img = models.ImageField(upload_to='Users/Profiles/', blank=True, null=True)
    Address = models.CharField(max_length=400, null=True, blank=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_staff_head = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role_id = models.ForeignKey(UserRoles, on_delete=models.CASCADE, null=True, blank=True)
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = datetime.datetime.now()
        self.updated_date = datetime.datetime.now()
        return super().save(*args, **kwargs)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name or self.email.split('@')[0]

class ManagementStaff(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    EmailID = models.CharField(max_length=200)
    IsSuperAdmin = models.BooleanField()
    IsAdmin = models.BooleanField()
    LoginId = models.ForeignKey(User, on_delete=models.CASCADE)
    IsActive = models.BooleanField()
    CreatedBy = models.CharField(max_length=255)
    CreatedDate = models.DateTimeField(default=datetime.datetime.now())
    UpdatedBy = models.CharField(max_length=255, null=True, blank=True)
    UpdatedDate = models.DateTimeField(null=True, blank=True)

class TrainingStaff(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    EmailID = models.CharField(max_length=200)
    LoginId = models.ForeignKey(User, on_delete=models.CASCADE)
    IsActive = models.BooleanField()
    CreatedBy = models.CharField(max_length=255)
    CreatedDate = models.DateTimeField(default=datetime.datetime.now())
    UpdatedBy = models.CharField(max_length=255, null=True, blank=True)
    UpdatedDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.Name

class TrainerQualifications(models.Model):
    userid = models.CharField(max_length=8, unique=True, blank=True, null=True)
    ID = models.AutoField(primary_key=True)
    LanguageID = models.ForeignKey(Languages, on_delete=models.CASCADE)
    LevelId = models.ForeignKey(Level, on_delete=models.CASCADE)
    CertificateNumber = models.CharField(max_length=255)
    CertifyingAuthority = models.CharField(max_length=255)
    CertificateValidTill = models.DateTimeField()
    TrainerHead = models.BooleanField(default = False)
    CreatedBy = models.CharField(max_length=255)
    CreatedDate = models.DateTimeField(default=datetime.datetime.now())
    UpdatedBy = models.CharField(max_length=255, null=True, blank=True)
    UpdatedDate = models.DateTimeField(null=True, blank=True)
    TrainerId = models.ForeignKey(TrainingStaff, on_delete=models.CASCADE)

class ProofOfIdentty(models.Model):
    ID = models.AutoField(primary_key=True)
    Type = models.CharField(max_length=255)
    Value = models.CharField(max_length=255)
    CreatedBy = models.CharField(max_length=255)
    CreatedDate = models.DateTimeField(default=datetime.datetime.now())
    UpdatedBy = models.CharField(max_length=255)
    UpdatedDate = models.DateTimeField(default=datetime.datetime.now())

class trainer_head_table(models.Model):
    trainer_head = models.ForeignKey(TrainingStaff, on_delete=models.CASCADE, related_name='trainer_head_allocations', null=True, blank=True)
    IsActive = models.BooleanField()
    CreatedBy = models.CharField(max_length=255)
    CreatedDate = models.DateTimeField(default=datetime.datetime.now())
    UpdatedDate = models.DateTimeField(default=datetime.datetime.now())
    UpdatedBy = models.CharField(max_length=255)

    def __str__(self):
        return self.trainer_head.Name

class TrainingBatches(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255, unique=True)
    Course_details = models.ForeignKey(Courses, on_delete=models.CASCADE, null=False, blank=False)
    TrainerId = models.ForeignKey(TrainingStaff, on_delete=models.CASCADE, null=False, blank=False)
    trainer_head = models.ForeignKey(trainer_head_table, on_delete=models.CASCADE, related_name='training_batches_as_head', null=True, blank=True)
    CreatedBy = models.CharField(max_length=255)
    CreatedDate = models.DateTimeField(default=datetime.datetime.now())
    UpdatedDate = models.DateTimeField(default=datetime.datetime.now())
    UpdatedBy = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

class StudentBatchAllocation(models.Model):
    ID = models.AutoField(primary_key=True)
    TrainerID = models.ForeignKey(TrainingStaff, on_delete=models.CASCADE)
    Student_Details = models.ManyToManyField("StudentDetails")
    BatchID = models.ForeignKey(TrainingBatches, on_delete=models.CASCADE)
    CreatedBy = models.CharField(max_length=255)
    CreatedDate = models.DateTimeField(default=datetime.datetime.now())
    UpdatedBy = models.CharField(max_length=255, null=True, blank=True)
    UpdatedDate = models.DateTimeField(null=True, blank=True)

class StudentDetails(models.Model):
    userid = models.CharField(max_length=8, blank=True, null=True)
    ID = models.AutoField(primary_key=True)
    StudentID = models.ForeignKey(User, on_delete=models.CASCADE)
    certificate = models.ImageField(upload_to='Students/Certificate/', null=True, blank=True)
    BatchID = models.ForeignKey(TrainingBatches, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    PaymentDetails = models.ForeignKey(Payments, on_delete=models.CASCADE, null=True, blank=True)
    Language_Id = models.ForeignKey(Languages, on_delete=models.CASCADE, null=True)
    CreatedBy = models.CharField(max_length=255)
    CreatedDate = models.DateTimeField(default=datetime.datetime.now())
    UpdatedBy = models.CharField(max_length=255, null=True, blank=True)
    UpdatedDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.StudentID.name)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_messages')

    def __str__(self):
        return self.content