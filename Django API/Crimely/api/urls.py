from django.contrib import admin
from django.urls import path, include
from api.views import *
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

router  = routers.DefaultRouter()
router.register(r'Register', RegisterViewset)
router.register(r'Properties', PropertyViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('home/', HomeView, name='home'),
    path('getstream', Stream, name='streamdt'),
    path('gettokenstream/<token>', StreamToken, name='streamtk'),
    path('stream/', StreamView, name='streamroom'),
    path('streamtoken/<token>', StreamTokenView, name='stokenview'),
    path('videoapi/', APIEnd, name='api'),
    path('user_login/', UserLoginView.as_view(), name='login')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
