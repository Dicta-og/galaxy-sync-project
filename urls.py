from django.urls import path
from . import views


urlpatterns = [
    path('', views.WelcomeView, name='home'),
    path('register', views.RegisterView, name='register'),
    path('login/', views.LoginView, name="login"),
    path('logout/', views.LogoutView, name='logout'),
    path('dashboard/', views.DashboardView, name="dashboard"),
    path('dashboard/admin', views.AdminDashboardView, name="admin_dashboard"),
    path('update/profile', views.UpdateProfileView, name='update_profile'),
    path('users/', views.AddUserView, name="add_user"),
    path('departments/', views.DepartmentsView, name="departments"),
    # path('add_tasks/', views.TasksView, name="add_tasks"),
    path('add_tasks/<int:user_id>/', views.TasksView, name='add_tasks'),
    path('view_tasks/', views.task_tracking_view, name="view_tasks"),
    path('my_tasks/', views.MyTasksView, name="my_tasks"),
    path('staff_list/', views.StaffView, name="staff_list"),
    path('tasks/complete/<int:task_id>/', views.complete_task, name='complete_task'),
]

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
