from django.urls import path
from . import views

urlpatterns = [
    path('',views.form_page),
    path('register',views.register),
    path('login',views.login),
    path('allusers',views.allusers),
    path('addteam',views.addteam),
    path('shows/<int:id>/edit',views.edit,name="edit_user"),
    path('editshow/<int:id>',views.editshow),
    path('delete/<int:id>',views.delete,name="del_user"),
]