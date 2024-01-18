from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponse
from datetime import date

class LogIn(LoginView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        rememberme = request.POST.get('rememberme')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request=request, message="User not found!!!")
            return redirect('login')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request=request, message="Incorrect password")
            return redirect('login')
        login(request=request, user=user)
        if not rememberme:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        messages.success(request=request, message=" ")
        return redirect('profile')


class SignUp(CreateView):
    model = User
    fields = "__all__"
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        try:
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')

            if password1 != password2:
                messages.success(request, 'The passwords in both password fields are not the same!!!')
                return redirect('signup')

            if User.objects.filter(username=username).first():
                messages.success(request, "Such a user has already registered!!!")
                return redirect('signup')

            if User.objects.filter(email=email).first():
                messages.success(request, "This email has already been registered!!!")
                return redirect('signup')

            user_obj = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
            user_obj.set_password(raw_password=password1)
            user_obj.save()
            return redirect('profile')
        except Exception as e:
            messages.error(request, f"Error {e}")
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
        return render(request, 'base.html')
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

from .forms import PunchInForm
from .models import Punch_In
from .models import Daily_Attendance
from .models import Total_Expense

@login_required
def punch_in(request):
    user = request.user
    if request.method == 'POST':
        form = PunchInForm(request.POST, request.FILES)
        last_punchin = Punch_In.objects.last()
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.user = request.user
            attendance.save()
            # Update the attendance record in the attendance table
            attendance_record, created = Daily_Attendance.objects.get_or_create(
                user=request.user,
                date=attendance.date,
                intime=attendance.time
            )
            attendance_record.present = "Present"
            attendance_record.save()
            messages.success(request, 'Punch In saved successfully.')
            return redirect('punch_in')
            
    else:
        form = PunchInForm()
    return render(request, 'punch_in.html', {'form': form})

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
from .forms import PunchOutForm
from django.db import IntegrityError
@login_required
def punch_out_create(request):
    if request.method == 'POST':
        form = PunchOutForm(request.POST, request.FILES)
        if form.is_valid():
            punch_out = form.save(commit=False)
            punch_out.user = request.user
            punch_out.save()
            attendance_records = Daily_Attendance.objects.filter(user=request.user, date=date.today())
            
            if attendance_records.exists():
                attendance_record = attendance_records.first()  # Select the first matching object
                attendance_record.outtime = punch_out.time
                attendance_record.save()
            
            messages.success(request, 'Punch Out saved successfully.')
            last_punchout = Punch_Out.objects.last()
            last_punchin = Punch_In.objects.last()
            vehicle=Punch_In.objects.last()

            if last_punchin.vehicle_type == '4 wheeler':
                daily_km = last_punchout.manual_reading - last_punchin.manual_reading
                daily_cost = daily_km * 10 + (last_punchout.daily_allounce ) + (last_punchout.lodging )
            elif last_punchin.vehicle_type == '2 wheeler':
                daily_km = last_punchout.manual_reading - last_punchin.manual_reading
                daily_cost = (daily_km * 3.5) + int(last_punchout.daily_allounce or 0) + int(last_punchout.lodging or 0 )

            elif last_punchin.vehicle_type == 'By Train':
                daily_km = 0
                daily_cost = (last_punchout.ticket_amount or 0 )+ (last_punchout.daily_allounce or 0) +(last_punchout.lodging or 0)+(last_punchin.ticket_amount or 0)

            elif last_punchin.vehicle_type == 'By Bus':
                daily_km = 0
                daily_cost = (last_punchout.ticket_amount or 0)+ (last_punchout.daily_allounce or 0) +(last_punchout.lodging or 0)+(last_punchin.ticket_amount or 0)

            elif last_punchin.vehicle_type == 'By Auto':
                daily_km = 0
                daily_cost = (last_punchout.ticket_amount or 0)+ (last_punchout.daily_allounce or 0) +(last_punchout.lodging or 0)+(last_punchin.ticket_amount or 0)


            else:
                daily_cost = 0

            try:
                total_expense = Total_Expense.objects.create(
    user=request.user,
    daily_km=daily_km or 0,
    daily_cost=daily_cost or 0,
    vehicle_type=vehicle.vehicle_type,
    punchin_from=last_punchin.from_location,
    punchin_to=last_punchin.to_location,
    punchout_from=last_punchout.from_location,
    punchout_to=last_punchout.to_location,
    morning_reading=last_punchin.manual_reading or 0,
    evening_reading=last_punchout.manual_reading or 0,
    ticket=(last_punchout.ticket_amount or 0) + (last_punchin.ticket_amount or 0),
    d_a=last_punchout.daily_allounce or 0,
    lodging_boarding=last_punchout.lodging or 0
)

                total_expense.save()
            except IntegrityError:
                total_expense = Total_Expense.objects.get(user=request.user, date=date.today())
                total_expense.save()
        return redirect('punch_out')
    else:
            form = PunchOutForm()
    
    return render(request, 'punch_out_create.html', {'form': form})

@login_required
def all_punchin(request):
    user = request.user
    punch_in=Punch_In.objects.filter(user=user)
    return render(request, 'all_punchins.html',{'punch_in': punch_in})

@login_required
def punch_out_details(request):
    user = request.user
    punch_out = Punch_Out.objects.filter(user=user).order_by('-date', '-time').first()
    return render(request, 'punch_out_details.html', {'punch_out': punch_out})

@login_required
def all_punchout(request):
    user = request.user
    punch_out=Punch_Out.objects.filter(user=user)
    return render(request, 'all_punchouts.html',{'punch_out': punch_out})

from django.core.paginator import Paginator
from django.db.models import Sum
from datetime import datetime

@login_required
def total_expense(request):
    user = request.user
    current_month = datetime.now().month
    total=Total_Expense.objects.filter(user=user)
    punchin=Punch_In.objects.filter(user=user)
    punchout=Punch_Out.objects.filter(user=user)
    employeeprofile=EmployeeProfile.objects.filter(user=user)
    paginator = Paginator(total,31)  # Show 10 expenses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Calculate the sum of total_cost for the current page
    total_cost_current_page = page_obj.object_list.aggregate(total=Sum('daily_cost'))['total']


    return render(request, 'daily_credits.html', {
        'page_obj': page_obj,
        'punchin':punchin,
        'punchout':punchout,
        'total_cost': total_cost_current_page,
        'employeeprofile':employeeprofile,
    })
 
@login_required
def attendance(request):
    user = request.user
    attendance=Daily_Attendance.objects.filter(user=user)
    total=Daily_Attendance.objects.filter(user=user,present='Present').count()
    return render(request, 'leave.html',{'attendance':attendance, 'total':total }) 


from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
import os
from xhtml2pdf import pisa
from datetime import datetime

@login_required
def download_pdf(request):
    # Retrieve data for the total expense report
    user = request.user
    current_month = datetime.now().month

    total=Total_Expense.objects.filter(user=user,date__month=current_month)
    punchin=Punch_In.objects.filter(user=user)
    punchout=Punch_Out.objects.filter(user=user)
    employeeprofile = EmployeeProfile.objects.filter(user=user).first()
    paginator = Paginator(total,31)  # Show 10 expenses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Calculate the sum of total_cost for the current page
    total_cost_current_page = page_obj.object_list.aggregate(total=Sum('daily_cost'))['total']


    # Render the PDF template with the data
    template = get_template('total_expense_pdf.html')
    context = {'total':page_obj,'punchin':punchin,'punchout':punchout,'total_cost':total_cost_current_page,'employeeprofile':employeeprofile,'user': user }
    rendered_html = template.render(context)
    
    # Create a PDF file
    pdf_file = os.path.join(settings.MEDIA_ROOT, 'total_expense_report.pdf')
    with open(pdf_file, 'w+b') as f:
        pisa_status = pisa.CreatePDF(rendered_html, dest=f)
    
    if pisa_status.err:
        return HttpResponse('Error generating PDF file')

    # Download the PDF file
    with open(pdf_file, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="total_expense_report.pdf"'
    
    # Delete the temporary PDF file
    os.remove(pdf_file)
    
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
