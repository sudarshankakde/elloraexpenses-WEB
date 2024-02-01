from django.contrib import admin
from .models import EmployeeProfile, Punch_In, Punch_Out, Total_Expense, Daily_Attendance,AppUpdate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.db.models import Sum
from datetime import datetime
import os
from xhtml2pdf import pisa
from django.conf import settings
from django.contrib.auth.models import User

# Custom admin class for EmployeeProfile
class EmployeeProfileAdmin(admin.ModelAdmin):
    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    user_full_name.short_description = 'Employee Name'
    list_display = ('user_full_name','employee_id', 'department', 'designation','phone_number')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'department', 'designation')
 
    def employee_id(self, obj):
        return obj.user.username

    employee_id.short_description = 'Employee ID'
# Register EmployeeProfile model with the custom admin class
admin.site.register(EmployeeProfile, EmployeeProfileAdmin)

# Custom admin class for Punch_In
class PunchInAdmin(admin.ModelAdmin):
    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def employee_id(self, obj):
        return obj.user.username

    employee_id.short_description = 'Employee ID'
    user_full_name.short_description = 'Employee Name'
    list_display = ('user_full_name','employee_id', 'date', 'time', 'vehicle_type','ticket_amount','manual_reading','from_location', 'to_location','meter_photo','ticket_photo')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'date', 'vehicle_type', 'from_location', 'to_location')
    list_per_page = 30
    date_hierarchy = 'date'
# Register Punch_In model with the custom admin class
admin.site.register(Punch_In, PunchInAdmin)

# Custom admin class for Punch_Out
class PunchOutAdmin(admin.ModelAdmin):
    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def employee_id(self, obj):
        return obj.user.username

    employee_id.short_description = 'Employee ID'
    user_full_name.short_description = 'Employee Name'
    list_display = ('user_full_name','employee_id', 'date', 'time','manual_reading','ticket_amount','lodging','daily_allounce', 'from_location', 'to_location','meter_photo','ticket_photo','lodging_photo')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'date', 'from_location', 'to_location')
    list_per_page = 30
    date_hierarchy = 'date'
# Register Punch_Out model with the custom admin class
admin.site.register(Punch_Out, PunchOutAdmin)

# Custom admin class for Total_Expense
class TotalCostAdmin(admin.ModelAdmin):
    def download_pdf(self, request, queryset):
        # Assuming you want to generate the report for all selected users (or single user)
        # For simplicity, consider the first selected user if multiple users are selected
        selected_users = queryset.values_list('user', flat=True).distinct()
        
        for user_id in selected_users:
            user = User.objects.get(id=user_id)  # Assuming User model for simplicity
            current_month = datetime.now().month

            total = Total_Expense.objects.filter(user=user, date__month=current_month)
            punchin = Punch_In.objects.filter(user=user)
            punchout = Punch_Out.objects.filter(user=user)
            employeeprofile = EmployeeProfile.objects.filter(user=user).first()

            paginator = Paginator(total, 31)
            page_obj = paginator.get_page(1)  # Assuming page 1 for simplicity
            total_cost_current_page = page_obj.object_list.aggregate(total=Sum('daily_cost'))['total']

            template = get_template('total_expense_pdf.html')
            context = {'total': page_obj, 'punchin': punchin, 'punchout': punchout, 'total_cost': total_cost_current_page, 'employeeprofile': employeeprofile, 'user': user}
            rendered_html = template.render(context)

            pdf_file_path = os.path.join(settings.MEDIA_ROOT, f'total_expense_report_{user.id}.pdf')

            with open(pdf_file_path, 'w+b') as f:
                pisa_status = pisa.CreatePDF(rendered_html, dest=f)

            if not pisa_status.err:
                with open(pdf_file_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='application/pdf')
                    response['Content-Disposition'] = f'attachment; filename="total_expense_report_{user.id}.pdf"'
                os.remove(pdf_file_path)

        return response

    download_pdf.short_description = "Download Expense"

    actions = ['download_pdf']

    change_list_template = 'admin/change_list.html'
    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    def employee_id(self, obj):
        return obj.user.username

    employee_id.short_description = 'Employee ID'
    user_full_name.short_description = 'Employee Name'
    list_display = ('user_full_name','employee_id', 'date', 'daily_cost','daily_km','ticket','d_a','lodging_boarding', 'vehicle_type', 'punchin_from', 'punchin_to', 'punchout_from', 'punchout_to')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'date', 'vehicle_type', 'punchin_from', 'punchin_to', 'punchout_from', 'punchout_to')
    list_per_page = 30
    date_hierarchy = 'date'


# Register Total_Expense model with the custom admin class
admin.site.register(Total_Expense, TotalCostAdmin)

# Custom admin class for Daily_Attendance
class DailyAttendanceAdmin(admin.ModelAdmin):
    def employee_id(self, obj):
        return obj.user.username

    employee_id.short_description = 'Employee ID'
    list_display = ('get_user_full_name','employee_id', 'date', 'intime', 'outtime', 'present')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'date', 'present')

    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    get_user_full_name.short_description = 'Employee Name'
    date_hierarchy = 'date'
# Register Daily_Attendance model with the custom admin class
admin.site.register(Daily_Attendance, DailyAttendanceAdmin)


admin.site.register(AppUpdate)
