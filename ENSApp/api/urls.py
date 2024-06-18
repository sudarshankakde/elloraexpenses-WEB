from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ENSApp import views
from ENSPL import views as logicView


urlpatterns = [
    #api call
    path("api_login", views.apiLogin, name="apiLogin"),
    path("api_singUp", views.singUpApi, name="singUpApi"),
    path('check_username', views.check_username, name='check_username'),
    path('check_email', views.check_email, name='check_email'),
    path('getProfile', views.getProfile, name='getProfile'),
    path('allPunchIn', views.allPunchIn, name='allPunchIn'),
    path('punchInRequest_api', logicView.punchInRequest_api, name='punchInRequest_api'),
    path('allPunchOut', views.allPunchOut, name='allPunchOut'),
    path('punchOutRequest_api', logicView.punchOutRequest_api, name='punchOutRequest_api'),
    path('attendanceApi', views.attendanceApi, name='attendanceApi'),
    path('expensesApi', views.expensesApi, name='expensesApi'),
    path('dowloadExpensesPdf', views.dowloadExpensesPdf, name='dowloadExpensesPdf'),

    # apk updates
    path('download_apk', views.download_apk, name='download-apk'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
