from django.urls import path


from users import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUp, name='signup'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),

]