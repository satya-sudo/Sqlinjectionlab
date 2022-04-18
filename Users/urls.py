from django.urls import path
from . import views
from . import insecureViews
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.user_view, name='profile'),
    path('profile_edit/', views.edit_profile, name='edit_profile'),
    path('project/', views.project_add, name='project'),
    path('search',views.search,name='search'),

    # # insecure code , code which is vulnerable to sql injection
    # path('/s/login/', views.login, name='login'),
    # path('/s/logout/', views.logout, name='logout'),
    # path('/s/register/', views.register, name='register'),
    # path('/s/profile/', views.profile, name='profile'),

]
