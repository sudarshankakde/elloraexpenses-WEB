import datetime
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
# import django.utils.datetime_safe as datetime_djnago
from django.utils.timezone import now as dajngo_datetime

class EmployeeProfile(models.Model):
    DEPARTMENT_CHOICES = [
        ('Account', 'Account'),
        ('Admin', 'Admin'),
        ('Biotech', 'Biotech'),
        ('Construction', 'Construction'),
        ('Electrical', 'Electrical'),
        ('FWD', 'FWD'),
        ('General', 'General'),
        ('HR', 'HR'),
        ('International Business Unit (IBU)', 'International Business Unit (IBU)'),
        ('IT', 'IT'),
        ('Logistics', 'Logistics'),
        ('Production(Onion)', 'Production(Onion)'),
        ('Production(Veg)', 'Production(Veg)'),
        ('Production(Maize)', 'Production(Maize)'),
        ('MD', 'MD'),
        ('Purchase', 'Purchase'),
        ('QA', 'QA'),
        ('R&D', 'R&D'),
        ('Security', 'Security'),
        ('SPT', 'SPT'),
        ('Vehicle', 'Vehicle'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='images/', default='default.png')
    department = models.CharField(max_length=100,choices=DEPARTMENT_CHOICES)
    designation = models.CharField(max_length=100)
    vehicle_number=models.CharField(max_length=15)
    phone_number = models.CharField(max_length=20)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=200)
    work_location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.department})"
    
    
    

#Punch In

class Punch_In(models.Model):
    VEHICLE_CHOICES = [
        ('2 wheeler', 'Two Wheeler'),
        ('4 wheeler', 'Four Wheeler'),
        ('By Train', 'By Train'),
        ('By Bus','By Bus'),
        ('By Auto','By Auto')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=dajngo_datetime)
    time=models.TimeField(auto_now_add=True, null=True,blank=True)
    vehicle_type = models.CharField(max_length=9, choices=VEHICLE_CHOICES)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    meter_photo = models.ImageField(upload_to='meter_photos/',verbose_name = "Meter Photo",null=True,blank=True)
    manual_reading = models.IntegerField(verbose_name = "Manual Reading",default=0,null=True,blank=True)
    ticket_amount = models.IntegerField(null=True,blank=True)
    ticket_photo = models.ImageField(upload_to='meter_photos/',null=True,blank=True)
    todays_work = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.user.first_name} {self.user.last_name}'

    class Meta:
         verbose_name_plural = "Punch In"


#Punch Out
class Punch_Out(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=dajngo_datetime)
    time=models.TimeField(auto_now_add=True, null=True)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    meter_photo = models.ImageField(upload_to='meter_photos/',verbose_name = "Meter Photo",null=True,blank = True)
    manual_reading = models.IntegerField(verbose_name = "Manual Reading",default=0, null=True)
    ticket_amount = models.IntegerField(default=0,null=True,blank = True)
    ticket_photo = models.ImageField(upload_to='meter_photos/',null=True,blank = True)
    daily_allounce = models.IntegerField(default=0,verbose_name = "DA",null=True,blank = True)
    lodging = models.IntegerField(default=0,verbose_name = "Lodging/Boarding",null=True,blank = True)
    lodging_photo = models.ImageField(upload_to='meter_photos/',null=True,blank=True)
    toll_parkking = models.IntegerField(default=0,verbose_name = "Toll/Fastag/Parking",null=True,blank = True)
    other_expenses = models.IntegerField(default=0,verbose_name = "other_expenses",null=True,blank = True)
    todays_work = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.user.first_name} {self.user.last_name}'


        
    class Meta:
         verbose_name_plural = "Punch Out"

class Total_Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_type=models.CharField(max_length=10)
    date = models.DateField(default=dajngo_datetime)
    punchin_from=models.CharField(max_length=200)
    punchin_to=models.CharField(max_length=200)
    punchout_from=models.CharField(max_length=200)
    punchout_to=models.CharField(max_length=200)
    morning_reading = models.IntegerField(default=0,verbose_name = "Manual Reading")
    evening_reading = models.IntegerField(default=0,verbose_name = "Manual Reading")
    ticket = models.IntegerField(default=0)
    d_a = models.IntegerField(default=0,verbose_name = "DA")
    lodging_boarding = models.IntegerField(default=0,verbose_name = "Lodging/Boarding")
    daily_km = models.IntegerField(default=0)
    toll_parkking = models.IntegerField(default=0,verbose_name = "Toll/Fastag/Parking",null=True,blank = True)
    other_expenses = models.IntegerField(default=0,verbose_name = "other_expenses",null=True,blank = True)
    daily_cost = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.daily_km} - {self.daily_cost}"
 
    class Meta:
     verbose_name_plural = "Total Expense"


class Daily_Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    intime=models.TimeField(null=True)
    outtime=models.TimeField(null=True)
    date = models.DateField(default=dajngo_datetime)
    present = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user.username} - {self.user.first_name} {self.user.last_name}'

        
    class Meta:
         verbose_name_plural = "Daily Attendance"
    
from django.core.validators import FileExtensionValidator
from django.core.files.storage import FileSystemStorage

def validate_apk_file(value):
    if not value.name.endswith('.apk'):
        raise ValidationError('Only APK files are allowed.')

class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # Overwrite the file if it already exists
        return name

custom_storage = CustomFileSystemStorage(location='media/app_updates_files/')

class AppUpdate(models.Model):
    version_code = models.CharField(help_text='Version code= 1.0.0',max_length=10)
    release_date = models.DateField(auto_now_add=True)
    update_description = models.TextField()
    apk_file = models.FileField(
        upload_to='',
        validators=[validate_apk_file],
        storage=custom_storage
    )
    
    def __str__(self):
        return f'{self.version_code} ({self.release_date})'