from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('course/', views.ListCourses.as_view(), name='courses'),
    path('course/<slug>', views.CourseDetailPage.as_view(), name='course-detail'),
    path('course/<slug>/<lesson_slug>', views.LessonDetailPage.as_view(), name='lesson-detail'),
    # path('add-course', views.AddCourse, name='add-course'),
    path('add-course', views.CreateCourse.as_view(), name='add-course'),
    path('tarrifs/', views.tarrifsPage, name='tarrifs'),
]

