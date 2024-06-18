from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import date, timedelta
from ENSApp.forms import PunchInForm , PunchOutForm_API , PunchInForm_API,PunchOutForm
from ENSApp.models import Punch_In 

def handle_punch_in(request, form_class, response_type='html'):
    todays_date = date.today()
    
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        for_date = request.POST.get('date', todays_date)
        last_punchin = Punch_In.objects.filter(user=request.user).last()
        
        if last_punchin:
            last_punchin_date = last_punchin.date
        else:
            last_punchin_date = todays_date - timedelta(days=1)
        
        if form.is_valid():
            if last_punchin_date != todays_date:
                attendance = form.save(commit=False)
                attendance.user = request.user
                attendance.save()
                
                attendance_record, created = Daily_Attendance.objects.get_or_create(
                    user=request.user,
                    date=for_date,
                    defaults={'intime': attendance.time}
                )
                attendance_record.present = "Present"
                attendance_record.save()
                
                if response_type == 'html':
                    messages.success(request, 'Punch In saved successfully.')
                    return redirect('punch_in')
                else:
                    return JsonResponse({'message': 'Punch In Saved!'}, status=201)
            else:
                if response_type == 'html':
                    messages.success(request, f'Punch In For {todays_date} Already Exists.')
                    return redirect('punch_in')
                else:
                    return JsonResponse({'message': f'Punch In For {todays_date} Already Exists.'}, status=406)
        else:
            if response_type == 'html':
                messages.error(request, 'Form is not valid.')
            else:
                return JsonResponse({'message': 'Form is not valid'}, status=406)
    
    if response_type == 'html':
        form = form_class()
        return render(request, 'punch_in.html', {'form': form})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

@login_required
def punch_in(request):
    return handle_punch_in(request, PunchInForm, response_type='html')

@login_required
def punchInRequest_api(request):
    return handle_punch_in(request, PunchInForm_API, response_type='json')


# Punch Out
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError
from datetime import date, timedelta

from ENSApp.models import  Punch_Out, Total_Expense, Daily_Attendance

def calculate_daily_cost_and_km(last_punchin, last_punchout):
    daily_km = 0
    daily_cost = 0

    if last_punchin.vehicle_type == '4 wheeler':
        daily_km = (last_punchout.manual_reading or 0) - (last_punchin.manual_reading or 0)
        daily_cost = daily_km * 10 + (last_punchout.daily_allounce or 0) + (last_punchout.lodging or 0) + (last_punchin.ticket_amount or 0)

    elif last_punchin.vehicle_type == '2 wheeler':
        daily_km = (last_punchout.manual_reading or 0) - (last_punchin.manual_reading or 0)
        daily_cost = (daily_km * 3.5) + int(last_punchout.daily_allounce or 0) + int(last_punchout.lodging or 0) + (last_punchout.ticket_amount or 0) + (last_punchin.ticket_amount or 0)
        
    elif last_punchin.vehicle_type in ['By Train', 'By Bus', 'By Auto']:
        daily_km = 0
        daily_cost = (last_punchout.ticket_amount or 0) + (last_punchout.daily_allounce or 0) + (last_punchout.lodging or 0) + (last_punchin.ticket_amount or 0)
    
    daily_cost += (last_punchout.toll_parkking or 0) + (last_punchout.other_expenses or 0)
    
    return daily_km, daily_cost

def handle_punch_out(request, form_class, response_type='html'):
    if request.method == 'POST':
        todays_date = date.today()
        form = form_class(request.POST, request.FILES)
        for_date = request.POST.get('date', todays_date)
        last_punchout = Punch_Out.objects.filter(user=request.user).last()
        
        if last_punchout:
            last_punchout_date = last_punchout.date
        else:
            last_punchout_date = todays_date - timedelta(days=1)
        
        if form.is_valid():
            if last_punchout_date != todays_date:
                punch_out = form.save(commit=False)
                punch_out.user = request.user
                punch_out.save()
                
                attendance_records = Daily_Attendance.objects.filter(user=request.user, date=for_date)
                if attendance_records.exists():
                    attendance_record = attendance_records.first()
                    attendance_record.outtime = punch_out.time
                    attendance_record.save()

                last_punchin = Punch_In.objects.filter(user=request.user, date=for_date).last()
                daily_km, daily_cost = calculate_daily_cost_and_km(last_punchin, punch_out)

                try:
                    total_expense = Total_Expense.objects.create(
                        user=request.user,
                        date=for_date,
                        daily_km=daily_km or 0,
                        daily_cost=daily_cost or 0,
                        vehicle_type=last_punchin.vehicle_type,
                        punchin_from=last_punchin.from_location,
                        punchin_to=last_punchin.to_location,
                        punchout_from=punch_out.from_location,
                        punchout_to=punch_out.to_location,
                        morning_reading=last_punchin.manual_reading or 0,
                        evening_reading=punch_out.manual_reading or 0,
                        ticket=(punch_out.ticket_amount or 0) + (last_punchin.ticket_amount or 0),
                        d_a=punch_out.daily_allounce or 0,
                        lodging_boarding=punch_out.lodging or 0,
                        toll_parkking=punch_out.toll_parkking or 0,
                        other_expenses=punch_out.other_expenses or 0
                    )
                    total_expense.save()
                except IntegrityError:
                    total_expense = Total_Expense.objects.get(user=request.user, date=for_date)
                    total_expense.save()
                
                if response_type == 'html':
                    messages.success(request, 'Punch Out saved successfully.')
                    return redirect('punch_out')
                else:
                    return JsonResponse({'message': 'Punch Out Saved!'}, status=201)
            else:
                if response_type == 'html':
                    messages.success(request, f'Punch Out For {todays_date} Already Exists.')
                    return redirect('punch_out')
                else:
                    return JsonResponse({'message': f'Punch Out For {todays_date} Already Exists.'}, status=406)
    
    if response_type == 'html':
        form = form_class()
        return render(request, 'punch_out_create.html', {'form': form})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

@login_required
def punch_out_create(request):
    return handle_punch_out(request, PunchOutForm, response_type='html')

@login_required
def punchOutRequest_api(request):
    return handle_punch_out(request, PunchOutForm_API, response_type='json')


