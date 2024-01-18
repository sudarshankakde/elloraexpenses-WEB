from rest_framework import serializers
from .models import EmployeeProfile, Punch_In, Punch_Out, Total_Expense, Daily_Attendance, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',"username","first_name","last_name","email"]

class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = '__all__'

class PunchInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Punch_In
        fields = '__all__'

class PunchOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Punch_Out
        fields = '__all__'

class TotalExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Total_Expense
        fields = '__all__'

class DailyAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Daily_Attendance
        fields = '__all__'
