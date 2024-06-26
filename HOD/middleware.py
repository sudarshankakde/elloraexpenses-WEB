from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from ENSApp.models import EmployeeProfile

class HODGroupRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
      if request.user.is_authenticated:
            # Get the app name of the view
            app_name = resolve(request.path_info).app_name

            # Apply middleware check only for the 'hod' app
            if app_name == 'hod':
                # Check if the user is in the HOD group
                if not request.user.groups.filter(name='HOD').exists():
                    return HttpResponseForbidden('You do not have permission to view this page.')
      employee_id = view_kwargs.get('employeeId')
      if employee_id:
            # Access the user's profile based on the employeeId
            
        employee_profile = EmployeeProfile.objects.get(user__id=employee_id)
        HODDepartment = EmployeeProfile.objects.get(user__id=request.user.id)
              
          # Check if the employee's department is in the allowed departments
        if employee_profile.department != HODDepartment.department :
            # Redirect to a specific page or perform some action
            return HttpResponseForbidden(f"You are not allowed to access {employee_profile.department} department")
            
      # Only check for authenticated users
        

      # If the user is not authenticated, or the app is not 'hod', let the request pass
      return None
