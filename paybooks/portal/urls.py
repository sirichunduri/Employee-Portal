from django.urls import path
from . import views

urlpatterns = [
		path('', views.home, name='portal-home'),
		path('saved', views.saved_data, name='saved'),
    	path('<username>/<year>/<week>', views.report_data, name='portal-data'),
		path('data/',views.get_data,name='get-data'),
		path('savename/',views.post_name,name='post-name'),
		
	]