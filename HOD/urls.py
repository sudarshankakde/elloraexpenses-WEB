from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
from ENSApp import views
from ENSPL import views as logicView
from . import views

app_name = 'hod'

urlpatterns = [
    path("", views.home, name="HOD_home"),
    path("view_approved/", views.view_approved, name="view_approved"),
    path("change_amount/<int:expenseId>", views.change_amount, name="change_amount"),
    path("change_values/<int:expenseId>/<str:type>/", views.change_values, name="change_values"),
    path("edit_application", views.edit_application, name="edit_application"),
    path("delete_expense/<int:id>", views.delete_expense, name="delete_expense"),
    path('view_employee/<int:employeeId>/',views.view_employee, name='view_employee'),
    re_path(r'^approve/(?P<employeeId>\d+)/(?P<month>\d{0,2})?//?(?P<year>\d{4})?/$', views.approve_amount, name='approve_amount'),
    
]

