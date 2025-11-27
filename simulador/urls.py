from django.urls import path
from . import views

app_name = 'simulador'

urlpatterns = [
    # Login, logout y registro
    path('login_admin/', views.login_admin, name='login_admin'),
    path('login_alumno/', views.login_alumno, name='login_alumno'),
    path('registro_alumno/', views.registro_alumno, name='registro_alumno'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards
    path('dashboard_admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard_alumno/', views.dashboard_alumno, name='dashboard_alumno'),

    # Mini curso
    path('ver_minicurso/', views.ver_minicurso, name='ver_minicurso'),
    path('editar_minicurso/', views.editar_minicurso, name='editar_minicurso'),

    # Evaluación por imágenes (nuevo sistema)
    path('evaluacion/<int:numero>/', views.pregunta, name='pregunta'),
    path('finalizar_evaluacion/', views.finalizar_evaluacion, name='finalizar_evaluacion'),

    # Exportar CSV
    path('export_csv/', views.export_csv, name='export_csv'),

    # Página inicial → login del alumno
    path('', views.login_alumno, name='home'),

    path('fix_admin/', views.fix_admin, name='fix_admin')
]

