"""cryptoclass URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^references', TemplateView.as_view(template_name='references.html'), name="references_index"),
    url(r'^faq', TemplateView.as_view(template_name='faq.html'), name="faq_index"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^lectures/', include('lectures.urls')),
    url(r'^media/material/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT + '/material/' }),
    url(r'^', include('exercises.urls'), name='exercise_index'),
]
