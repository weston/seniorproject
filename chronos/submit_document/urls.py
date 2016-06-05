from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^submit$', views.submit, name='submit'),
	url(r'^submit_success$', views.submit_success, name='submit_success'),

]
