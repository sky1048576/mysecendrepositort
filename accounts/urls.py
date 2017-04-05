


from django.conf.urls import url

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^register$', views.register, name='register'),
    url(r'^information$', views.information, name='information'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^like$', views.like, name='like'),

]