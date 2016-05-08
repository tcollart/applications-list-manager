from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ApplicationListView.as_view(), name='list_app'),
    url(r'^upload/$', views.ApplicationCreateView.as_view(), name='upload_app'),
    url(r'^edit/(?P<pk>\d+)/$', views.ApplicationUpdateView.as_view(), name='edit_app'),
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^signin/$', views.signin, {'template_name': 'app/signin.html'}, name='signin'),
    url(r'^signout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='signout'),
]
