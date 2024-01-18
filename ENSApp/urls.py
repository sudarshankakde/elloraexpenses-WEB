from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

from .views import (
    LogIn,
    success,
    user_logout,
    SignUp,
    profile,
    create_profile,
    edit_profile
)

urlpatterns = [
    path("", LogIn.as_view(), name="login"),
    path("success/", success, name="success"),
    path("logout/", user_logout, name="logout"),
    path("signup/", SignUp.as_view(), name="signup"),
    #for crud profile
    path('profile/', profile, name='profile'),
    path('create_profile/', create_profile, name='create_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),

    #api call
    path("api_login", views.apiLogin, name="apiLogin"),
    path("api_singUp", views.singUpApi, name="singUpApi"),
    path('check_username', views.check_username, name='check_username'),
    path('check_email', views.check_email, name='check_email'),
    path('getProfile', views.getProfile, name='getProfile'),
    path('allPunchIn', views.allPunchIn, name='allPunchIn'),
    path('punchInRequest_api', views.punchInRequest_api, name='punchInRequest_api'),
    path('allPunchOut', views.allPunchOut, name='allPunchOut'),
    path('punchOutRequest_api', views.punchOutRequest_api, name='punchOutRequest_api'),
    path('attendanceApi', views.attendanceApi, name='attendanceApi'),
    path('expensesApi', views.expensesApi, name='expensesApi'),
    path('dowloadExpensesPdf', views.dowloadExpensesPdf, name='dowloadExpensesPdf'),
    
    #for crud tr_expenses
    path('punch_in/', views.punch_in, name='punch_in'),
    path('punchindetails',views.show_punchin, name='punchindetails'),
    #for Punch Out
    path('punch_out/', views.punch_out_create,name='punch_out'),
    path('punchoutdetails',views.punch_out_details, name='punchoutdetails'),
    path('cost',views.total_expense,name='total_cost'),
    path('allin',views.all_punchin,name='allpunchin'),
    path('allout',views.all_punchout,name='allpunchout'),
    path('attendance',views.attendance,name='attendance'),
    path('pdf',views.download_pdf,name='pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
