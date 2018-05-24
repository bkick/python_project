from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'login$', views.login),
	url(r'register$', views.register),
	url(r'register/submit$', views.regsubmit)
	url(r'login/subit$', views.logsubmit)

]