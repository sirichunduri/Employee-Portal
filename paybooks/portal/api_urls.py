from django.urls import path,include
from .views import *
from rest_framework import routers
router =routers.DefaultRouter()
router.register('',EmployeeViewSet)


urlpatterns = [
    path('employee/', include(router.urls)),
    #path('jsontimesheet/', timesheet_api,name='timesheet_api'),
    path('jsontimesheet/', EmployeeAPIView.as_view()),
    path('generic/jsontimesheet/', EmployeeListView.as_view()),
    path('generic/jsontimesheet/<int:id>/', EmployeeListView.as_view()),
    path('jsontimesheet/<int:id>/', timesheet_details,name='timesheet_actions'),

]
