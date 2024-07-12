import calendar
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import FileResponse, HttpResponse , HttpResponseNotFound, JsonResponse
from datetime import date, timedelta
from django.core import serializers 

def home_view(request):
    if request.user.is_authenticated:
        return redirect('profile')  # Redirect to the profile page
    else:
        return redirect('login')  # Redirect to the login page

#login's 
def authenticate_and_login(request, username, password):
    user_obj = User.objects.filter(username=username).first()
    if user_obj is None:
        return None, "User not found"
    
    user = authenticate(username=username, password=password)
    if user is None:
        return None, "Incorrect password"
    
    login(request, user)
    return user, None

def apiLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user, error = authenticate_and_login(request, username, password)
        
        if error:
            return HttpResponseNotFound(error)
        
        user_json = serializers.serialize('json', [get_object_or_404(User, username=username)])
        return HttpResponse(user_json, content_type='application/json')
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

class LogIn(LoginView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        rememberme = request.POST.get('rememberme')
        user, error = authenticate_and_login(request, username, password)
        
        if error:
            messages.error(request, error)
            return redirect('login')
        
        if not rememberme:
            request.session.set_expiry(0)
            request.session.modified = True
        messages.success(request, "Successfully logged in.")
        return redirect('profile')


#Registration
def create_user(username, email, first_name, last_name, password):
    if User.objects.filter(username=username).exists():
        return None, "A user with that username already exists."
    if User.objects.filter(email=email).exists():
        return None, "A user with that email already exists."
    
    user_obj = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
    user_obj.set_password(password)
    user_obj.save()
    return user_obj, None

def singUpApi(request):
    try:
        if request.method == "POST":
            username = request.POST.get('userName')
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            user, error = create_user(username, email, first_name, last_name, password)
            if error:
                return JsonResponse({'message': error}, status=400)
            
            return JsonResponse({'message': 'User saved successfully.'}, status=201)
        else:
            return JsonResponse({'message': 'Invalid request method'}, status=405)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)

class SignUp(CreateView):
    model = User
    fields = "__all__"
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        try:
            username = request.POST.get('username')
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 != password2:
                messages.error(request, 'The passwords do not match.')
                return redirect('signup')

            user, error = create_user(username, email, first_name, last_name, password1)
            if error:
                messages.error(request, error)
                return redirect('signup')

            messages.success(request, 'User registered successfully.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('signup')
        
def success(request):
    return render(request=request, template_name='success.html', context={})


def user_logout(request):
    logout(request)
    return redirect(to='login')


#For profile..
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import EmployeeProfile
from .forms import EmployeeProfileForm


@login_required
def profile(request):
    try:
        user = request.user
        user_profile = EmployeeProfile.objects.get(user=user)
    except EmployeeProfile.DoesNotExist:
        return render(request, 'profile.html',{'user_profile': False})
    return render(request, 'profile.html', {'user': user, 'user_profile': user_profile})

@login_required
def create_profile(request):
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile created successfully.')
            return redirect('profile')
    else:
        form = EmployeeProfileForm()
    return render(request, 'create_profile.html', {'form': form})

@login_required
def edit_profile(request):
    user_profile = get_object_or_404(EmployeeProfile, user=request.user)
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EmployeeProfileForm(instance=user_profile)
    return render(request, 'edit_profile.html', {'form': form})


#Punch In

from .forms import PunchInForm , PunchOutForm_API , PunchInForm_API
from .models import Punch_In 
from .models import Daily_Attendance
from .models import Total_Expense


@login_required
def show_punchin(request):
    user = request.user
    today=date.today()
    try:
        punchin = Punch_In.objects.filter(user=user).order_by('-date', '-time').first()
        return render(request, 'punch_in_details.html', {'punchin': punchin})
    except Punch_In.DoesNotExist:
        return HttpResponse("No record found")
    except Punch_In.MultipleObjectsReturned:
        return HttpResponse("Multiple records found")


#Punch In
from django.shortcuts import render, redirect
from .models import Punch_Out, Total_Expense


@login_required
def all_punchin(request):
    user = request.user
    punch_in=Punch_In.objects.filter(user=user).order_by('-date')
    return render(request, 'all_punchins.html',{'punch_in': punch_in})

@login_required
def punch_out_details(request):
    user = request.user
    punch_out = Punch_Out.objects.filter(user=user).order_by('-date', '-time').first()
    return render(request, 'punch_out_details.html', {'punch_out': punch_out})

@login_required
def all_punchout(request):
    user = request.user
    punch_out=Punch_Out.objects.filter(user=user).order_by('-date')
    return render(request, 'all_punchouts.html',{'punch_out': punch_out})

from django.core.paginator import Paginator
from django.db.models import Sum
from datetime import datetime

@login_required
def total_expense(request):
    if request.method == "GET":
      month=request.GET.get('month') or datetime.now().month
      year=request.GET.get('year') or datetime.now().year
      userInstance = get_object_or_404(User,id=request.user.id)
      punchin=Punch_In.objects.filter(user=request.user).order_by('date')
      punchout=Punch_Out.objects.filter(user=request.user).order_by('date')
      EmployyeInstance = EmployeeProfile.objects.get(user=userInstance)
      expenses = Total_Expense.objects.filter(user=userInstance,date__month=month,date__year=year).order_by('date')
      total_cost_current_page = expenses.aggregate(total=Sum('daily_cost'))['total']
      approval = Approved_monthly_expenses.objects.filter(employee__id=EmployyeInstance.id, approved_For_Month_Year__month=int(month), approved_For_Month_Year__year=int(year)).first()
      
      if approval:
        approval = approval
      else:
        False
      expenses_with_changes = []
      for expense in expenses:
        change_logs = expense.change_logs.all()
        changes = {log.field_name: log.new_value for log in change_logs}
        expenses_with_changes.append({
            'expense': expense,
            'changes': changes
        })
      return render(request,'daily_credits.html',{
          'expenses': expenses_with_changes,
          'total_cost': total_cost_current_page,
          'employeeprofile':EmployyeInstance,
          'employeeData':userInstance,
          'month':month,
          'year':year,
          'approved':approval or False,
          'punchin':punchin,
          'punchout':punchout,
        
      })
 
@login_required
def attendance(request):
    user = request.user
    attendance=Daily_Attendance.objects.filter(user=user).order_by('-date','-intime').values()
    total=Daily_Attendance.objects.filter(user=user,present='Present').count()
    return render(request, 'leave.html',{'attendance':attendance, 'total':total }) 


from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
import os
from xhtml2pdf import pisa
from datetime import datetime
from HOD.models import Approved_monthly_expenses
@login_required
def download_expenses_pdf(request):
    if request.GET.get('user'):
      user = get_object_or_404(User,id=int(request.GET.get('user')))
    else:
      user = request.user
    context = {}
    month = int(request.GET.get('month') or datetime.now().month)
    year = int(request.GET.get('year') or datetime.now().year)
    # Fetch employee profile
    employeeprofile = EmployeeProfile.objects.filter(user=user).first()
    if not employeeprofile:
        return JsonResponse({'message': 'Employee profile not found.'}, status=404)

    # Fetch punch-in and punch-out records
    punchin = Punch_In.objects.filter(user=user).order_by('date')
    punchout = Punch_Out.objects.filter(user=user).order_by('date')
    
    # Check for approved expenses
    approved_model_instance = Approved_monthly_expenses.objects.filter(
        employee__id=employeeprofile.id,
        approved_For_Month_Year__month=month,
        approved_For_Month_Year__year=year
    ).first()

    if approved_model_instance:
        total_expenses = approved_model_instance.approvedExpenses.all()
        total_cost = approved_model_instance.total_expense_allocated
        context['approved'] = approved_model_instance
    else:
        total_expenses = Total_Expense.objects.filter(
            user=user,
            date__month=month,
            date__year=year
        ).order_by('date')
        if total_expenses.count() == 0:
            return JsonResponse({'message': f'No Expenses For {calendar.month_name[month]}.'}, status=404)
        
        total_cost = total_expenses.aggregate(total=Sum('daily_cost'))['total']
        context['approved'] = False
    # Fetch change logs for each expense
    expenses_with_changes = []
    for expense in total_expenses:
        change_logs = expense.change_logs.all()
        changes = {log.field_name: log.new_value for log in change_logs}
        expenses_with_changes.append({
            'expense': expense,
            'changes': changes
        })
    context.update({
        'punchin': punchin,
        'punchout': punchout,
        'total': expenses_with_changes,
        'total_cost': total_cost,
        'employeeprofile': employeeprofile,
        'user': user
    })

    # Render the PDF template with the data
    template = get_template('total_expense_pdf.html')
    rendered_html = template.render(context)

    # Create a PDF file
    pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'total_expense_report.pdf')
    with open(pdf_file_path, 'w+b') as pdf_file:
        pisa_status = pisa.CreatePDF(rendered_html, dest=pdf_file)

    if pisa_status.err:
        return JsonResponse({'message': 'Error while generating PDF file'}, status=500)

    # Serve the PDF file
    with open(pdf_file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="total_expense_report.pdf"'
    
    # Clean up the temporary PDF file
    os.remove(pdf_file_path)
    
    return response
#Api
from rest_framework import viewsets
from .models import EmployeeProfile, Punch_In, Punch_Out, Total_Expense, Daily_Attendance
from .serializers import EmployeeProfileSerializer, PunchInSerializer, PunchOutSerializer, TotalExpenseSerializer, DailyAttendanceSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class EmployeeProfileViewSet(viewsets.ModelViewSet):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer

class PunchInViewSet(viewsets.ModelViewSet):
    queryset = Punch_In.objects.all()
    serializer_class = PunchInSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class PunchOutViewSet(viewsets.ModelViewSet):
    queryset = Punch_Out.objects.all()
    serializer_class = PunchOutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class TotalExpenseViewSet(viewsets.ModelViewSet):
    queryset = Total_Expense.objects.all()
    serializer_class = TotalExpenseSerializer

class DailyAttendanceViewSet(viewsets.ModelViewSet):
    queryset = Daily_Attendance.objects.all()
    serializer_class = DailyAttendanceSerializer


@login_required
def getProfile(request):
    try:
        user = request.user
        user_profile = EmployeeProfile.objects.get(user=user)
    except EmployeeProfile.DoesNotExist:
        return HttpResponseNotFound('Create Profile')
    user_json = serializers.serialize('json', [user_profile])
    return HttpResponse(user_json,content_type ='application/json')

@login_required
def allPunchIn(request):
    try:
        user = request.user
        all_punchin = Punch_In.objects.filter(user=user).order_by('-date','-time').values()  # Get a QuerySet of dictionaries
        response_data = {'data': list(all_punchin)}
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

    return JsonResponse(response_data, safe=False)

@login_required
def allPunchOut(request):
    try:
        user = request.user
        all_Punch_Out = Punch_Out.objects.filter(user=user).order_by('-date','-time').values()  # Get a QuerySet of dictionaries
        response_data = {'data': list(all_Punch_Out)}
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

    return JsonResponse(response_data, safe=False)

@login_required
def attendanceApi(request):
    try:
        if(request.method == "GET"):
            month = (request.GET.get('m'))
            year = (request.GET.get('y') or datetime.now().year)
            user = request.user
            if month:
                attendance = Daily_Attendance.objects.filter(user=user,date__month=month,date__year=year).order_by('-date','-intime').values()
                response_data = {'data': list(attendance)}
            else:
                attendance = Daily_Attendance.objects.filter(user=user).order_by('-date','-intime').values()
                response_data = {'data': list(attendance)}
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

    return JsonResponse(response_data, safe=False)

@login_required
def expensesApi(request):
    try:
        user = request.user
        expenses = Total_Expense.objects.filter(user=user).order_by('-date').values()
        TotalCost = expenses.aggregate(totalCost_Sum = Sum('daily_cost'))
        response_data = {'data': list(expenses),'totalCost': TotalCost}
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)
    return JsonResponse(response_data, safe=False)


def check_username(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        if not username:
            return JsonResponse({'message': 'Username parameter is missing.'}, status=400)
        try:
            user = User.objects.get(username=username)
            return JsonResponse({'message': 'Username is not available.'},status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'Username is available.'},status = 200)
        
def check_email(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        if not email:
            return JsonResponse({'message': 'email parameter is missing.'}, status=400)
        try:
            if User.objects.filter(email=email).first():
                return JsonResponse({'message': 'email is not available.'},status=400)
            else:
                return JsonResponse({'message': 'email is  available.'},status=200)
        except User.DoesNotExist:
            return JsonResponse({'message': 'email is available.'},status = 200)






# download_apk/views.py
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import AppUpdate
def download_apk(request):
    try:
        if request.method == 'GET':
            current_version = str(request.GET.get('version') or '0')
            latest_app = AppUpdate.objects.all().order_by('-release_date').first()
            if latest_app is None:
                    return JsonResponse({'message': 'No APK to download'},status="404")
            else:
                print(current_version)
                print(latest_app.version_code)
                print(latest_app.version_code > current_version)
                if (latest_app.version_code <= current_version):
                    return JsonResponse({'message': 'Up to date'},status="404")
                else:
                    response = FileResponse(latest_app.apk_file.open(), content_type='application/vnd.android.package-archive')
                    response['Content-Disposition'] = f'attachment; filename="{latest_app.apk_file.name}"'
                    return response
    except Exception as e:
        return JsonResponse({'message': 'Error!',"error":f"{e}"},status="404")
