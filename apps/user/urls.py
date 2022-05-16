from django.conf.urls import url
from user import views
urlpatterns = [
    url('register/',views.register,name='register'),
    url('login/',views.login,name='login'),
    # url('register_handle/',views.register_handle,name='register_handle'),
]
