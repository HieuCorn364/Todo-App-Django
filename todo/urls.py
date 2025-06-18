from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signup, name='signup'),
    path('loginn', views.loginn, name='loginn'),
    path('logoutt', views.logoutt, name='logoutt'),
    path('todopage/', login_required(views.todo), name='todopage'),
    path('edit_todo/<int:srno>/', login_required(views.edit_todo), name='edit_todo'),
    path('delete_todo/<int:srno>/', login_required(views.delete_todo), name='delete_todo'),
    path('toggle_todo/<int:srno>/', login_required(views.toggle_todo), name='toggle_todo'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
]