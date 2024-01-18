from django.db import models
from django.contrib.auth.models import User
class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='images/', default='default.png')
    department = models.CharField(max_length=100)
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
    date = models.DateField(auto_now_add=True,null=True)
    time=models.TimeField(auto_now_add=True, null=True)
    vehicle_type = models.CharField(max_length=9, choices=VEHICLE_CHOICES)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    meter_photo = models.ImageField(upload_to='meter_photos/',verbose_name = "Meter Photo",null=True)
    manual_reading = models.IntegerField(verbose_name = "Manual Reading",default=0,null=True)
    ticket_amount = models.IntegerField(null=True)
    ticket_photo = models.ImageField(upload_to='meter_photos/',null=True)
    todays_work = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.user.first_name} {self.user.last_name}'

    class Meta:
         verbose_name_plural = "Punch In"


#Punch Out
class Punch_Out(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True,null=True)
    time=models.TimeField(auto_now_add=True, null=True)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    meter_photo = models.ImageField(upload_to='meter_photos/',verbose_name = "Meter Photo",null=True)
    manual_reading = models.IntegerField(verbose_name = "Manual Reading",default=0, null=True)
    ticket_amount = models.IntegerField(default=0,null=True)
    ticket_photo = models.ImageField(upload_to='meter_photos/',null=True)
    daily_allounce = models.IntegerField(default=0,verbose_name = "DA",null=True)
    lodging = models.IntegerField(default=0,verbose_name = "Lodging/Boarding",null=True)
    lodging_photo = models.ImageField(upload_to='meter_photos/',null=True,blank=True)
    todays_work = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.user.first_name} {self.user.last_name}'

    class Meta:
         verbose_name_plural = "Punch Out"

class Total_Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_type=models.CharField(max_length=10)
    date = models.DateField(auto_now_add=True)
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
    daily_cost = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.daily_km} - {self.daily_cost}"
    class Meta:
     verbose_name_plural = "Total Expense"


class Daily_Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    intime=models.TimeField(null=True)
    outtime=models.TimeField(null=True)
    date = models.DateField(auto_now_add=True)
    present = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user.username} - {self.user.first_name} {self.user.last_name}'

    class Meta:
         verbose_name_plural = "Daily Attendance"