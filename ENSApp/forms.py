from django import forms
from .models import EmployeeProfile




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
        fields = ['vehicle_type','from_location', 'to_location', 'meter_photo', 'manual_reading','ticket_amount','ticket_photo', 'todays_work']

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
        fields = ['from_location', 'to_location', 'meter_photo', 'manual_reading','ticket_amount','ticket_photo','daily_allounce','lodging','lodging_photo' ,'todays_work']
        labels = {
            'from_location': 'From Location',
            'to_location': 'To Location',
            'meter_photo': 'Meter Photo',
            'manual_reading': 'Manual Reading',
            'todays_work': "Work Status",
        }
        widgets = {
            'todays_work': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meter_photo'].widget.attrs.update({'accept': 'image/*'})

