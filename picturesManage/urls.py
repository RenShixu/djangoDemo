"""djangoDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name="index"),
    url(r'^pictures/(?P<pageNum>[0-9]+)/(?P<pageTotal>[0-9]+)',views.pictureslist,name="pictures"),
    url(r'^add/',views.addpicture,name="add"),
    url(r'^editshow/(?P<pid>[0-9]+)',views.editshow,name="editshow"),
    url(r'^editajax/(?P<pid>[0-9]+)',views.editajax,name="editajax"),

    url(r'^edit/',views.editpicture,name="edit"),
    url(r'^delete/(?P<pid>[0-9]+)',views.detelpicture,name="delete"),
    url(r'^submit/',views.submitpicture,name="submit"),

]
