#
# the following notation has been used :
# flag value of x denotes the leave iw with y
#
# x=1 means y= TA INSTRUCTOR
# x=2 means y = Supervisor
# x=4 means y= staff
# x=5 means y= HOD

from django.db import models
from django.contrib.auth.models import User
from users.models import CustomUser
from multiselectfield import MultiSelectField
from _datetime import datetime
from django.urls import reverse

# Create your models here.

HOSTEL_CHOICES = (
    ('Barak', 'Barak'),
    ('Bramhaputra', 'Bramhaputra'),
    ('Dhansiri', 'Dhansiri'),
    ('Dibang', 'Dibang'),
    ('Dihing', 'Dihing'),
    ('Kameng', 'Kameng'),
    ('Kapili', 'Kapili'),
    ('Lohit', 'Lohit'),
    ('Manas', 'Manas'),
    ('Siang', 'Siang'),
    ('Subansiri', 'Subansiri'),
    ('Umiam', 'Umiam'),
    ('Married_Scholar', 'Married_Scholar'),
    ('NA', 'NA'),

)

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

TYPEOFLEAVE = (
    ('Ordinary', 'Ordinary'),
    ('Medical', 'Medical'),
    ('Acedemic', 'Acedemic'),
    ('Maternity', 'Maternity'),
    ('Paternity', 'Paternity')
)
COURSE = (
    ('Mtech', 'Mtech'),
    ('Phd', 'Phd'),
    ('NA', 'NA')
)

ACADEMIC_YEAR = (
    (1, ("1")),
    (2, ("2")),
    (3, ("3")),
    (4, ("4")),
    (5, ("5")),
    (6, ("6")),
    (7, ("7")),
)

SEMESTER = (
    (1, ("1")),
    (2, ("2")),
    (3, ("3")),
    (4, ("4")),
    (5, ("5")),
    (6, ("6")),
    (7, ("7")),
)

SENT_TO = (('2', 'Supervisor'),
           ('1', 'TAinstructor'),
           ('3', 'DPPC'))

MONTHS = (
            ('January' , 'January' ),
            ('February','February'),
            ('March','March'),
            ('April','April'),
            ('May','May'),
            ('June','June'),
            ('July','July'),
            ('August','August'),
            ('September','September'),
            ('October','October'),
            ('November','November'),
            ('December','December'),
)

STATUS = (
    ('pending', 'pending'),
    ('approved', 'approved'),
    ('declined', 'declined'))

class Authorized(models.Model):
    name = models.CharField(max_length=200, blank=True, default="")
    profile_pic = models.ImageField(upload_to='faculty', blank=True, null=True, default=" ")
    webmail = models.CharField(max_length=128, blank=False)
    mob_num = models.CharField(max_length=128, blank=False)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse('leave_portal:dashboard')


    def __str__(self):
            return self.name

class Faculty(Authorized):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='faculty')
    faculty_id = models.CharField(max_length=128, blank=False)

class Dppc(Authorized):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='dpppc')
    dppc_id = models.CharField(max_length=128, blank=False)

class Hod(Authorized):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='hod')
    hod_id = models.CharField(max_length=128, blank=False)

class Staff(Authorized):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff')
    staff_id = models.CharField(max_length=128, blank=False)

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='students')
    name = models.CharField(max_length=200, blank=True, default="")
    profile_pic = models.ImageField(upload_to='student', blank=True, null=True)
    roll_no = models.CharField(max_length=128, blank=False, default=" ", unique=True)
    gender = models.CharField(max_length=30, choices=GENDER, blank=False)
    webmail = models.CharField(max_length=128, blank=False, unique=True)
    course = models.CharField(max_length=128, choices=COURSE, blank=True)
    acedemic_year = models.IntegerField(choices=ACADEMIC_YEAR, default=0)
    present_semester = models.IntegerField(choices=SEMESTER, null=True, blank=True)
    hostel_name = models.CharField(max_length=255, choices=HOSTEL_CHOICES, blank=True, default="")
    room_number = models.CharField(max_length=10, blank=True, default="")
    mob_number = models.CharField(max_length=15, blank=False, default=" ")
    emergency_mob_num = models.CharField(max_length=15, blank=True, default=" ")
    TA_instructor = models.ForeignKey(Faculty,max_length=200,on_delete=models.CASCADE , related_name='TA')
    Supervisor_1 = models.ForeignKey(Faculty, max_length=200,on_delete=models.CASCADE , related_name='Supervisor')
    Ordinary = models.IntegerField( blank=False, default=15)
    Ordinary1 = models.IntegerField( blank=False, default=15)
    Medical = models.IntegerField( blank=False, default=15)
    Acedemic = models.IntegerField( blank=False, default=30)
    Maternity = models.IntegerField( blank=False, default=135)
    Paternity = models.IntegerField( blank=False, default=15)

    class Meta:
        ordering =['roll_no']

    def get_absolute_url(self):
        return reverse('leave_portal:dashboard')

    def __str__(self):
        return self.name

class ApplyLeave(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applyleaves')
    LeaveFrom = models.DateField()
    LeaveTo = models.DateField()
    TypeOfLeave = models.CharField(max_length=255, choices=TYPEOFLEAVE, blank=False, default="")
    ReasonForLeave = models.CharField(max_length=200)
    Doc1 = models.FileField(upload_to='documents', blank=True, null=True)
    Doc2 = models.FileField(upload_to='documents', blank=True, null=True)
    AddressWhileOnLeave = models.CharField(max_length=200)
    PhoneNumberWhileOnLeave = models.CharField(max_length=20)
    DateOfApply = models.DateField(default=datetime.now)
    flag = models.IntegerField(default=0)
    SentTo = MultiSelectField(choices=SENT_TO)
    ApprovedStatus = models.CharField(max_length=100,choices=STATUS,default="pending")

    def __str__(self):
        return self.student.name

class Comments(models.Model):
    Leave = models.ForeignKey(ApplyLeave, on_delete=models.CASCADE, related_name='comments')
    Remark = models.CharField(max_length=200)
    Person = models.CharField(max_length=40)
    DateOfComment = models.DateField(default=datetime.now)

    def __str__(self):
        return self.Person

class TASlip (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taSlip')
    startingMonth = models.CharField(max_length=100 , choices = MONTHS)
    endingMonth = models.CharField(max_length=100 , choices = MONTHS)
    flag = models.IntegerField(default=0)
    ApprovedStatus = models.CharField(max_length=100,choices=STATUS,default="pending")
    DateOfApply = models.DateField(default=datetime.now)
