from django.shortcuts import render,HttpResponse,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from ENSApp.models import EmployeeProfile,Total_Expense
from datetime import datetime
from django.http import JsonResponse
from .models import Approved_monthly_expenses
import json
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.
def employee_expense(request, month=None,year=None, department=""):
    if month is None or month == '':
        month = datetime.now().month
    if year is None or year == '':
        year = datetime.now().year
    all_employees = EmployeeProfile.objects.filter(department=department)
    expenses = []

    for employee in all_employees:
        emp_for_month = Total_Expense.objects.filter(user=employee.user, date__month=month,date__year=year)
        if emp_for_month.count() > 0:
          total_cost = emp_for_month.aggregate(total=Sum('daily_cost'))['total']
          statusCheck = Approved_monthly_expenses.objects.filter(employee=employee,approved_For_Month_Year=datetime(int(year), int(month), 1),approved=True)
          # Create expenses instance
          expenses_instance = {
              "employee": employee,
              "total_expense": total_cost or 0,
              "status": statusCheck.exists() or False,
          }
          expenses.append(expenses_instance)
    print(expenses)
    return expenses

@login_required
def home(request):
  if request.method == 'GET':
    month=request.GET.get('month') or datetime.now().month
    year=request.GET.get('year') or datetime.now().year
    user = request.user
    try:
        hod_group = Group.objects.get(name="HOD")
        hod_department = EmployeeProfile.objects.get(user=user).department
        hod_profile = EmployeeProfile.objects.get(user=user)
        if hod_group in user.groups.all():
            context = {
                'user_info': {
                    'username': hod_profile.user.username,
                    'first_name':hod_profile.user.first_name,
                    'last_name': hod_profile.user.last_name,
                    'email': hod_profile.user.email,
                    'department': hod_department,
                    'designation':hod_profile.designation
                },
                'groups': user.groups.all(),
                'employees': employee_expense(request=request,department=hod_department,month=month,year=year),
                'expensesOF': datetime(int(year), int(month), 1)
            }
            return render(request, 'home.html', context)
    except Group.DoesNotExist:
        return HttpResponse("Group Does Not Exist")
    else:
        return HttpResponse("Your Not HOD")
      
from ENSApp.models import Punch_In,Punch_Out
from django.db.models import Sum
from django.contrib.auth.models import User
def view_employee(request, employeeId):
    if request.method == "GET":
        month = request.GET.get('month') or datetime.now().month
        year = request.GET.get('year') or datetime.now().year
        userInstance = get_object_or_404(User, id=employeeId)
        EmployyeInstance = EmployeeProfile.objects.get(user=userInstance)
        expenses = Total_Expense.objects.filter(user=userInstance, date__month=month, date__year=year).order_by('date')
        total_cost_current_page = expenses.aggregate(total=Sum('daily_cost'))['total']
        approval = Approved_monthly_expenses.objects.filter(employee__id=EmployyeInstance.id, approved_For_Month_Year__month=int(month), approved_For_Month_Year__year=int(year)).first()

        if approval:
            approval = approval
        else:
            approval = False

        # Fetch change logs for each expense
        expenses_with_changes = []
        for expense in expenses:
            change_logs = expense.change_logs.all()
            changes = {log.field_name: log.new_value for log in change_logs}
            expenses_with_changes.append({
                'expense': expense,
                'changes': changes
            })
        return render(request, 'employee.html', {
            'expenses': expenses_with_changes,
            'total_cost': total_cost_current_page,
            'employeeprofile': EmployyeInstance,
            'employeeData': userInstance,
            'month': month,
            'year': year,
            'approved': approval or False,
        })
    
    

def change_amount(request, expenseId):
  expense = get_object_or_404(Total_Expense, id=expenseId)
  expense.daily_cost = request.GET['amount'+str(expenseId)]
  expense.save()
  userInstance = get_object_or_404(User, id=expense.user.id)
  month = expense.date.strftime("%m")
  expenses = Total_Expense.objects.filter(user=userInstance,date__month=month).order_by('date')
  total_cost = expenses.aggregate(total=Sum('daily_cost'))['total']
  return HttpResponse(total_cost)


# Mapping of short types to model field names
change_values_type_dict = {
  'da': 'd_a',
  'lb': 'lodging_boarding',
  'dk': 'daily_km',
  'tp': 'toll_parkking',
  'oe': 'other_expenses',
  'tk': 'ticket',
}

def change_values(request, expenseId, type):
  # Get the corresponding model field name from the type
  field_name = change_values_type_dict.get(type)
  # Ensure that the type is valid
  if field_name is None:
    raise ValueError(f"Invalid type: {type}")

  # Get the expense object
  expense = get_object_or_404(Total_Expense, id=expenseId)
  
 
  # Construct the key to fetch the value from the request
  request_key = f'entry_{type}_{expenseId}'
  
  # Check if the key exists in the request
  if request_key not in request.GET:
    raise ValueError(f"Missing value for {type} in the request")
  
  # Get the value from the request
  new_value =int(request.GET[request_key])
  
  # Set the new value for the corresponding field
  setattr(expense, field_name, new_value)
  
  # Save the updated expense object
  expense.save()

  # Retrieve related punchin and punchout objects


  daily_cost  = (
        (expense.ticket or 0) +
        (expense.d_a or 0) +
        (expense.lodging_boarding or 0) +
        (expense.toll_parkking or 0) +
        (expense.other_expenses or 0)+
        ( calculate_km_cost(expense.daily_km,expense.vehicle_type) or 0)
  )
  
  # Update the total amount in the expense object
  expense.daily_cost = daily_cost
  
  # Save the updated expense object with the total amount
  expense.save()
  userInstance = get_object_or_404(User, id=expense.user.id)
  month = expense.date.strftime("%m")
  expenses = Total_Expense.objects.filter(user=userInstance,date__month=month).order_by('date')
  total_cost = expenses.aggregate(total=Sum('daily_cost'))['total']
  return JsonResponse({'amount': expense.daily_cost,'total_cost': total_cost})

def approve_amount(request, employeeId, month=None, year=None):
    if month is None or month == '':
        month = datetime.now().month
    else:
      month = month
    if year is None or year == '':
        year = datetime.now().year
    

    userInstance = get_object_or_404(User, id=employeeId)
    employeeInstance = get_object_or_404(EmployeeProfile, user=userInstance)
    expenses = Total_Expense.objects.filter(user=userInstance, date__month=month).order_by('date')
    total_cost = expenses.aggregate(total=Sum('daily_cost'))['total']

   
    approved_expense_instance = Approved_monthly_expenses.objects.filter(employee__id=employeeInstance.id, approved_For_Month_Year__month=int(month), approved_For_Month_Year__year=int(year))
    if approved_expense_instance.exists():
      # Update the ApprovedExpenses instance
      approved_expense_instance = approved_expense_instance.first()
      approved_expense_instance.approved_by=request.user
      approved_expense_instance.employee=employeeInstance
      approved_expense_instance.remark=request.POST.get('remark', '')
      approved_expense_instance.total_expense_allocated=total_cost
      approved_expense_instance.approved=True
      approved_expense_instance.approved_For_Month_Year=datetime(int(year), int(month), 1)
      approved_expense_instance.save()  # Save for making instace
      # Now set the ManyToMany relationship
      approved_expense_instance.approvedExpenses.set(expenses)
      approved_expense_instance.save()  # Save again if necessary
      messages.add_message(request, messages.SUCCESS, f'''{userInstance.username}'s Expenses Approval Updated Successfully!''')
      
    else:
      approval = Approved_monthly_expenses(
          approved_by=request.user,
          employee=employeeInstance,
          remark=request.POST.get('remark', ''),
          total_expense_allocated=total_cost,
          approved=True,
          approved_For_Month_Year=datetime(int(year), int(month), 1)
      )
      approval.save()  # Save for making instace
      # Now set the ManyToMany relationship
      approval.approvedExpenses.set(expenses)
      approval.save()  # Save again if necessary
      messages.add_message(request, messages.SUCCESS, f'''{userInstance.username}'s Expenses Are Approved Successfully!''')
    return redirect(request.META.get('HTTP_REFERER', '/'))
    
    
def CheckApprovedStatus(employeeId,approved_For_Month_Year=None):
  if approved_For_Month_Year is None or approved_For_Month_Year == '':
        month = datetime.now().month
        year = datetime.now().year
  userInstance = get_object_or_404(EmployeeProfile, user__id=employeeId)
  return  Approved_monthly_expenses.objects.filter(employee__id=userInstance.id, approved_For_Month_Year__month=int(month), approved_For_Month_Year__year=int(year))


def view_approved(request):
    if request.method == 'GET':
        employeeId = request.GET.get('employee')
        month = request.GET.get('month')
        year = request.GET.get('year')

        # Get the current user
        current_user = request.user
        current_user_profile = get_object_or_404(EmployeeProfile, user=current_user)

        # If no employeeId is provided, get all Approved_monthly_expenses for the current month and year
        if not employeeId:
            # Use current month and year if not provided
            if not month:
                month = datetime.now().month
            if not year:
                year = datetime.now().year

            approved_For_Month_Year = datetime(int(year), int(month), 1)
            approved_expenses = Approved_monthly_expenses.objects.filter(
                employee__department=current_user_profile.department,
                approved_For_Month_Year__month=int(month),
                approved_For_Month_Year__year=int(year),
                approved=True
            )

            return render(request, 'approved.html', {
                'approved_expenses': approved_expenses,
                'approved_For_Month_Year': approved_For_Month_Year,
                'employeeInstance': None
            })
        else:
            # If employeeId is provided, filter expenses for that specific employee
            employeeInstance = get_object_or_404(EmployeeProfile, user__id=int(employeeId))

            # Use current month and year if not provided
            if not month:
                month = datetime.now().month
            if not year:
                year = datetime.now().year

            approved_For_Month_Year = datetime(int(year), int(month), 1)
            approved_expenses = Approved_monthly_expenses.objects.filter(
                employee=employeeInstance,
                approved_For_Month_Year__month=int(month),
                approved_For_Month_Year__year=int(year),
                approved=True
            )

            return render(request, 'approved.html', {
                'approved_expenses': approved_expenses,
                'approved_For_Month_Year': approved_For_Month_Year,
                'employeeInstance': employeeInstance
            })

    return HttpResponse('Method not allowed', status=405)      
        
def edit_application(request):
  if request.method == 'GET':
    applicationId = request.GET.get('applicationId')
    approved_monthly_expense = get_object_or_404(Approved_monthly_expenses,id=applicationId)
    approved_monthly_expense.approved = False
    approved_monthly_expense.save()
    messages.add_message(request, messages.SUCCESS, f'''You can edit application now!''')
    return redirect(request.META.get('HTTP_REFERER', '/'))
  
  
def delete_expense(request,id):
  if request.method == 'GET':
    deleteExpense = get_object_or_404(Total_Expense,id=id)
    deleteExpense.delete()
    messages.add_message(request, messages.SUCCESS, f'''Expense Deleted Successfully!''')
    return redirect(request.META.get('HTTP_REFERER', '/'))
  
  
  
def calculate_km_cost(daily_km,vehicle_type):
    if vehicle_type == '4 wheeler' or vehicle_type == '2 wheeler':
        daily_km = daily_km

        if vehicle_type == '4 wheeler':
            km_cost = daily_km * 10
        elif vehicle_type == '2 wheeler':
            km_cost = daily_km * 3.5

    elif vehicle_type in ['By Train', 'By Bus', 'By Auto']:
        km_cost = 0

    return  int(km_cost)