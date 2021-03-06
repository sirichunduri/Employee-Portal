"""paybooks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from users import views as user_views
from django.contrib.auth import views as auth_view
from portal.views import LoginView,LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
	path('register/', user_views.register, name='register'),
	path('', include('portal.urls')),
	path('login/', auth_view.LoginView.as_view(template_name='users/login.html'), name='login'),
	path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
	path('api/v1/', include('portal.api_urls')),
	#path('api/v1/auth/', include('rest_framework.urls')),
	path('api/v1/auth/login/', LoginView.as_view()),
	path('api/v1/auth/logout/', LogoutView.as_view()),
]
