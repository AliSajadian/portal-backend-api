from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import include 
# , url
from django.conf.urls.static import static

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path('', include('frontend.urls')),
#         # path('', include('surveyTypes.urls')),
#         path('', include('surveys.urls')),
#         path('', include('accounts.urls')),
#         path('__debug__'), include(debug_toolbar.urls)),
#     ] + urlpatterns

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('baseInfo.urls')),
    # path('', include('doctor_appointments.urls')),
    # path('', include('library.urls')),
    # path('', include('meeting_request.urls')),
    path('', include('resturaunt.urls')),
    # path('', include('surveys.urls')),
   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)