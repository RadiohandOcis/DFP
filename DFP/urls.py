"""DFP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from department import views

urlpatterns = [

    # 部门管理
    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),
    path('depart/delete/', views.depart_delete),
    path('depart/<int:nid>/edit/', views.depart_edit),

    # 职工管理
    path('personnel/list/', views.personnel_list),
    path('personnel/add/', views.personnel_add),
    path('personnel/<int:nid>/edit/', views.personnel_edit),
    path('personnel/<int:nid>/delete/', views.personnel_delete),

    # 登录界面
    path('login/', views.login),
    path('logout/', views.logout),
]
