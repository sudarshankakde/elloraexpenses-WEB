from django import forms
from .models import EmployeeProfile

class DateInput(forms.DateInput):
    input_type = 'date'
    

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ('profile_picture','department','designation','vehicle_number','phone_number','birth_date','address','work_location')

#Punch In form
from .models import Punch_In

class PunchInForm(forms.ModelForm):
    ticket_amount=forms.IntegerField(required=False)
    ticket_photo =forms.ImageField(required=False)
    meter_photo=forms.ImageField(required=False)
    manual_reading=forms.IntegerField(required=False)
    class Meta:
        model = Punch_In
        fields = ['date','vehicle_type','from_location', 'to_location', 'meter_photo', 'manual_reading','ticket_amount','ticket_photo', 'todays_work']
        
        widgets = {
            'date':DateInput(),
            'todays_work': forms.Textarea(attrs={'rows': 4}),
        }


    
#Punch Out form
from .models import Punch_Out
class PunchOutForm(forms.ModelForm):
    meter_photo=forms.ImageField(required=False)
    manual_reading=forms.IntegerField(required=False)
    ticket_amount=forms.IntegerField(required=False)
    ticket_photo =forms.ImageField(required=False)
    daily_allounce = forms.IntegerField(required=False)
    lodging = forms.IntegerField(required=False)
    lodging_photo = forms.ImageField(required=False)
    
    class Meta:
        model = Punch_Out
        fields = ['date','from_location', 'to_location', 'meter_photo', 'manual_reading','ticket_amount','ticket_photo','daily_allounce','lodging','lodging_photo' ,'toll_parkking','other_expenses','todays_work']
        labels = {
            'For Which Date':'date',
            'from_location': 'From Location',
            'to_location': 'To Location',
            'meter_photo': 'Meter Photo',
            'manual_reading': 'Manual Reading',
            'todays_work': "Work Status",
            'toll_parkking':"Toll/FastTag/Parking",
            'other_expenses':"Other Expenses"
        }
        widgets = {
            'date':DateInput(),
            'todays_work': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meter_photo'].widget.attrs.update({'accept': 'image/*'})


#Punch In form
from .models import Punch_In

class PunchInForm_API(forms.ModelForm):
    ticket_amount=forms.IntegerField(required=False)
    ticket_photo =forms.ImageField(required=False)
    meter_photo=forms.ImageField(required=False)
    manual_reading=forms.IntegerField(required=False)
    class Meta:
        model = Punch_In
        fields = ['vehicle_type','from_location', 'to_location', 'meter_photo', 'manual_reading','ticket_amount','ticket_photo', 'todays_work']
        
        widgets = {
            'todays_work': forms.Textarea(attrs={'rows': 4}),
        }


    
#Punch Out form
from .models import Punch_Out
class PunchOutForm_API(forms.ModelForm):
    meter_photo=forms.ImageField(required=False)
    manual_reading=forms.IntegerField(required=False)
    ticket_amount=forms.IntegerField(required=False)
    ticket_photo =forms.ImageField(required=False)
    daily_allounce = forms.IntegerField(required=False)
    lodging = forms.IntegerField(required=False)
    lodging_photo = forms.ImageField(required=False)
    
    class Meta:
        model = Punch_Out
        fields = ['from_location', 'to_location', 'meter_photo', 'manual_reading','ticket_amount','ticket_photo','daily_allounce','lodging','lodging_photo' ,'toll_parkking','other_expenses','todays_work']
        labels = {
            'from_location': 'From Location',
            'to_location': 'To Location',
            'meter_photo': 'Meter Photo',
            'manual_reading': 'Manual Reading',
            'todays_work': "Work Status",
            'toll_parkking':"Toll/FastTag/Parking",
            'other_expenses':"Other Expenses"
        }
        widgets = {
            'todays_work': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meter_photo'].widget.attrs.update({'accept': 'image/*'})

