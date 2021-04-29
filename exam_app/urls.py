from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('register', views.register),
    path('wishes', views.wishes),
    path('login', views.login),
    path('logout', views.logout),

    path('wishes/new', views.new_wish),
    path('wishes/create', views.create_wishe),
    path('wishes/delete/<int:wish_id>', views.delete_wish),
    path('wishes/edit/<int:wish_id>', views.edit_wish),
    path('wishes/update/<int:wish_id>', views.update_wish),
    path('wishes/granted/<int:wish_id>', views.granted_wish),
    path('wishes/liked/<int:wish_id>', views.liked_wish),
    path('wishes/unliked/<int:wish_id>', views.unliked_wish),
    path('wishes/stats/<int:user_id>', views.stats)
]