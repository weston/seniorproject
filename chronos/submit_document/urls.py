from django.conf.urls import url

import views
import utilities

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^submit$', views.submit, name='submit'),
	url(r'^submit_success$', views.submit_success, name='submit_success'),
	url(r'^coinbase_hook$', utilities.coinbase_hook, name='coinbase_hook'),
	url(r'^submit_success/(?P<address>[\w\-]+)/$', views.submit_success, name='submit_success'),
	url(r'^verify_document/$', views.verify_document, name='verify_document'),
	url(r'^document_query/$',views.document_query, name='document_query'),
	url(r'^about/$',views.about, name='about'),
]
