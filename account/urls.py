from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
app_name ='accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.my_login, name='login'),
    path('redirect_user/',views.redirect_user,name='redirect_user'),
    path('teacher_dashboard/',views.teacher_dashboard,name='teacher_dashboard'),
    path('student_dashboard/',views.student_dashboard,name='students_dashboard'),
    path('create_student/',views.create_student,name='create_student'),
    path('create_records/',views.create_record,name='create_records'),
    path('grade/edit/<int:grade_id>/', views.edit_grade, name='edit_grade'),
    path('grade/delete/<int:grade_id>/', views.delete_grade, name='delete_grade'),
    path('', views.home, name='home'),


  

  

    path('logout/', views.log_out, name='logout'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
