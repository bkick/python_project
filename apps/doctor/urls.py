from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'login$', views.login),
	url(r'register$', views.register),
	url(r'register/submit$', views.regsubmit),
	url(r'login/submit$', views.logsubmit),
	url(r'edit$', views.edit),
	url(r'dashboard$', views.dashboard),
	url(r'edit/submit$', views.submit),
	url(r'patient/(?P<number>\d)', views.patient)
]