"""
URL configuration for myproj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from .views import (
    AdminLoginView,
    AdminHomeView,
    AdminLogoutView,
    AdminUserListView,
    AdminEditView,
    AdminDeleteView,
    AdminCreateView,
)

urlpatterns = [
    path('myadmin/', AdminLoginView.as_view(), name='myadmin'),
    path('myadmin_home/', AdminHomeView.as_view(), name='myadmin_home'),
    path('myadmin_users/', AdminUserListView.as_view(), name='myadmin_users'),
    path('myadmin_new_user/', AdminCreateView.as_view(), name='myadmin_new_user'),
    path('myadmin_edit_user/<int:id>/', AdminEditView.as_view(), name='myadmin_edit_user'),
    path('myadmin_delete_user/<int:id>/', AdminDeleteView.as_view(), name='myadmin_delete_user'),
    path('admin_logout/', AdminLogoutView.as_view(), name='admin_logout'),
]
