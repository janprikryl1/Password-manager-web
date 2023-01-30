from django.urls import path

from . import views

urlpatterns = [
 path('', views.index, name="index"),
 path('profile', views.profile, name="profile"),
 path('sign_up', views.sign_up, name="sign_up"),
 path('sign_in', views.sign_in, name="sign_in"),
 path('logout', views.log_out, name="logout"),
 path('new_item', views.new_item, name="new_item"),
 path('add_new_item', views.add_new_item, name="add_new_item"),
 path('change', views.change, name="change"),
path('delete_item', views.delete_item, name="delete_item"),
path('change_user', views.chage_user, name="change_user"),

]