from django.conf.urls import url
from sokol import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    url(r'^signup', views.signup, name='signup'),
    url(r'^login', LoginView.as_view(extra_context={'next': 'profile'}), name='login'),
    url(r'^profile/$', views.Account.as_view(), name='profile'),
    url(r'^logged_out', LogoutView.as_view(), name='logged_out'),
    url(r'^profile/(?P<slug>[\w\-]+)/$', views.show_user_page, name='user_page'),
    url(r'^set_status/(?P<slug>[\w\-]+)/$', views.view_status, name='user_status'),
    url(r'^change_status/(?P<slug>[\w\-]+)/$', views.view_set_status, name='change_status'),
]
