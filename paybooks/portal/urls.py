from django.urls import path
from . import views

urlpatterns = [
		path('', views.home, name='portal-home'),
    	path('<username>/<year>/<week>', views.report_data, name='portal-data'),
		
	]