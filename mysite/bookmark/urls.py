from django.conf.urls import url

from . import views
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$',views.register, name='register'),
    url(r'^login/$',views.login_view, name='login'),
    url(r'^register/success/$',views.register_success, name='register_success'),
    url(r'^category/$',views.get_category,name='getcategory'),
    url(r'^#/$',views.save_bookmark,name='savebookmark'),
    url(r'^tag/$',views.save_tag,name = 'savetag'),
    url(r'^home/$',views.home,name='home'),
    url(r'^profile/$',views.profile,name = 'profile'),
    url(r'^about/$',views.about,name = 'about'),
    url(r'^deletebookmark/(?P<bookmark>http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)/$',views.delete_bookmark,name='deletebookmark'),
    url(r'^add/(?P<bookmark>http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)/$',views.add_bookmark,name='add'),
]
