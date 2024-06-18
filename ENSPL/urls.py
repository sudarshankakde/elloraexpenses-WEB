from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
admin.site.site_header="Ellora Natural Seeds Pvt Ltd"
admin.site.site_title="Ellora Natural Seeds Pvt Ltd"
admin.site.index_title="Welcome to Admin Panel"
from rest_framework import routers
from ENSApp.views import EmployeeProfileViewSet, PunchInViewSet, PunchOutViewSet, TotalExpenseViewSet, DailyAttendanceViewSet, UserViewSet,allPunchIn,getProfile
from HOD import urls as hod_urls
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'employee-profiles', EmployeeProfileViewSet)
router.register(r'punch-in', PunchInViewSet)
router.register(r'punch-out', PunchOutViewSet)
router.register(r'total-expense', TotalExpenseViewSet)
router.register(r'daily-attendance', DailyAttendanceViewSet)


urlpatterns = [ 
    path("admin/", admin.site.urls),
    path("", include('ENSApp.urls')),
    path('api/', include(router.urls)),
    path('hod-panel/', include(hod_urls)),
    
   
] 
if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)