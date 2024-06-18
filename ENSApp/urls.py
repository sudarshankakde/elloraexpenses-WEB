from django.urls import path,include
from ENSApp.api import urls as api_urls
from django.conf import settings
from django.conf.urls.static import static
from . import views
from ENSPL import views as logicView
from .views import (
    LogIn,
    success,
    user_logout,
    SignUp,
    profile,
    create_profile,
    edit_profile,home_view
)

urlpatterns = [
    path("",include(api_urls)),
    path("", home_view, name="home"),
    path("login", LogIn.as_view(), name="login"),
    path("success/", success, name="success"),
    path("logout/", user_logout, name="logout"),
    path("signup/", SignUp.as_view(), name="signup"),
    #for crud profile
    path('profile/', profile, name='profile'),
    path('create_profile/', create_profile, name='create_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),

    
    #for crud tr_expenses
    path('punch_in/', logicView.punch_in, name='punch_in'),
    path('punchindetails',views.show_punchin, name='punchindetails'),
    #for Punch Out
    path('punch_out/', logicView.punch_out_create,name='punch_out'),
    path('punchoutdetails',views.punch_out_details, name='punchoutdetails'),
    path('cost',views.total_expense,name='total_cost'),
    path('allin',views.all_punchin,name='allpunchin'),
    path('allout',views.all_punchout,name='allpunchout'),
    path('attendance',views.attendance,name='attendance'),
    path('pdf',views.download_pdf,name='pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
