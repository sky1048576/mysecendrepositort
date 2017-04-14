from django.conf.urls import url

from . import views

app_name = 'persons'
urlpatterns = [
    url(r'^add_home$', views.addHome, name='add_home'),
    url(r'^base$', views.base, name='base'),
    url(r'^$', views.showHome, name='show_homes'),
    url(r'^yourHomes/$', views.yourHomes, name='yourHomes'),


    url(r'^(?P<id>[0-9]+)/$', views.remove_a_ana, name='remove_a_ana'),
    url(r'^(?P<id>[0-9]+)/$', views.updown, name='updown'),
    url(r'^(?P<id>[0-9]+)/$', views.add_a_ana, name='add_a_ana'),

    
    url(r'^home/(?P<home_id>[0-9]+)/$', views.detail_home, name='detail_home'),
    url(r'^image/(?P<img_id>[0-9]+)/delete/$', views.delete_image, name='delete_image'),
    url(r'^(?P<home_id>[0-9]+)/delete/$', views.home_delete, name='delete'),
    url(r'^(?P<home_id>[0-9]+)/edit/$', views.home_update, name='update'),
    url(r'^users/(?P<user_id>[0-9]+)/$', views.detail_user, name='users'),
    url(r'^formset$', views.formset_view, name='formset'),
    url(r'^query$', views.query, name='query'),


]



from django.conf.urls import url

urlpatterns += [
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    url(r'^ajax/select_citys/$', views.select_citys, name='select_citys'),
]