from django.db import models
from django.urls import reverse
from django.utils.timezone import now as dajngo_datetime
from django.contrib.auth.models import User
from ENSApp.models import Total_Expense,EmployeeProfile


# Create your models here.
class Approved_monthly_expenses(models.Model):
    approved_on = models.DateField(default=dajngo_datetime)
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT,related_name='approved_by')
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.PROTECT,related_name='employee')
    approvedExpenses = models.ManyToManyField(Total_Expense, related_name='Total_Expense')
    remark = models.CharField(max_length=200,blank=True,null=True)
    total_expense_allocated = models.IntegerField(default=0)
    approved = models.BooleanField(default=True)
    approved_For_Month_Year = models.DateField(blank=False,null=False,default=dajngo_datetime)
    def __str__(self):
        return self.employee.user.first_name



class ExpenseChangeLog(models.Model):
    expense = models.ForeignKey(Total_Expense, on_delete=models.CASCADE, related_name='change_logs')
    field_name = models.CharField(max_length=100)
    old_value = models.CharField(max_length=255)
    new_value = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Change in {self.field_name} on {self.timestamp}"

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Total_Expense, ExpenseChangeLog

@receiver(pre_save, sender=Total_Expense)
def track_expense_changes(sender, instance, **kwargs):
    try:
        old_instance = Total_Expense.objects.get(pk=instance.pk)
    except Total_Expense.DoesNotExist:
        # Handle case where old_instance does not exist
        old_instance = None
    
    if old_instance:
        fields_to_track = [
            'vehicle_type', 'punchin_from', 'punchin_to', 'punchout_from', 'punchout_to',
            'morning_reading', 'evening_reading', 'ticket', 'd_a', 'lodging_boarding',
            'daily_km', 'toll_parkking', 'other_expenses', 'daily_cost'
        ]

        for field in fields_to_track:
            old_value = getattr(old_instance, field)
            new_value = getattr(instance, field)
            if old_value != new_value:
                ExpenseChangeLog.objects.create(
                    expense=instance,
                    field_name=field,
                    old_value=str(old_value),
                    new_value=str(new_value)
                )
    else:
        # Handle new instance creation or other scenarios
        pass
