from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from mysite.core import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('makestudy/', views.makestudy, name='makestudy'),
    path('studygroup/', views.StudyGroupsListView.as_view(), name='studygroup_list'),
    path('studygroup/<int:pk>/', views.studygroup_detail_view, name='studygroup_detail'),
    path('search/', views.searchData, name="searchData"),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
