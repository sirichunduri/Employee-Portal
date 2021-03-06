from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='portal-home'),
    path('portal/', views.report_data, name='portal-data'),
    path('data/', views.get_data, name='get-data'),
    path('savename/', views.post_name, name='savename'),
    path('jobtitle/', views.jobtitle, name='jobtitle'),
    path('applyLeave/', views.applyLeave, name='applyLeave'),
    path('applyLeave/<action>', views.applyLeave, name='applyLeave'),
    path('approveleave/', views.approveleave, name='approveleave'),

]
