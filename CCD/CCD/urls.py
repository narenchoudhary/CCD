"""CCD URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static


# https://docs.djangoproject.com/en/1.9/topics/http/views/#customizing-error
# -views
# http://stackoverflow.com/questions/17662928/django-creating-a-custom-500-
# 404-error-page
handler400 = 'jobportal.views.handler400'
handler403 = 'jobportal.views.handler403'
handler404 = 'jobportal.views.handler404'
handler500 = 'jobportal.views.handler500'
handler503 = 'jobportal.views.handler503'

urlpatterns = [
    url(r'^tracking/', include('tracking.urls')),
    url(r'^jobportal/', include('jobportal.urls')),
    url(r'^mentormentee/', include('mentormentee.urls',
                                       namespace="mentormentee",
                                       app_name="mentormentee")),
    url(r'^internships/', include('internships.urls',
                                      namespace="internships",
                                      app_name="internships")),
    url(r'^alumnijobs/', include('alumnijobs.urls',
                                     namespace="alumnijobs",
                                     app_name="alumnijobs")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('jobportal.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
