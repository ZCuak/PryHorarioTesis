from django.urls import path
from App import views
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path('', views.index, name='index'),
    path('billing/', views.billing, name='billing'),
    path('tables/', views.tables, name='tables'),
    path('vr/', views.vr, name='vr'),
    path('rtl/', views.rtl, name='rtl'),
    
    path('ejecutar_algoritmo/', views.ejecutar_algoritmo, name='ejecutar_algoritmo'),
    path('guardar_horarios/', views.guardar_horarios, name='guardar_horarios'),
    path('mostrar_resultados/', views.mostrar_resultados, name='mostrar_resultados'),

    #PARA REPORTES
    path('reporte_sustentaciones/', views.reporte_sustentaciones, name='reporte_sustentaciones'),
    path('exportar_csv/', views.exportar_csv, name='exportar_csv'),
    path('listar_sustentaciones/', views.listar_sustentaciones, name='listar_sustentaciones'),
    path('exportar_excel_profesor/', views.exportar_excel_profesor, name='exportar_excel_profesor'),
    #Para profesor
    
    path('disponibilidad/', disponibilidad_list, name='disponibilidad_list'),
    path('disponibilidad/crear/', disponibilidad_create, name='disponibilidad_create'),
    path('disponibilidad/ver/<int:semana_inicio>/<int:semana_fin>/', views.ver_disponibilidad, name='ver_disponibilidad'),
    path('disponibilidad/fechas_min_max/', views.obtener_fechas_min_max, name='obtener_fechas_min_max'),
    
    path('accounts/profile/', views.profile, name='profile'),
    path('jurados/', jurados_list, name='jurados_list'),
    path('jurados/create/', jurados_create, name='jurados_create'),
    path('jurados/update/<int:pk>/', jurados_update, name='jurados_update'),
    path('jurados/delete/<int:pk>/', jurados_delete, name='jurados_delete'),
    path('jurados/import/', jurados_import, name='jurados_import'),
    # Sustentacion
    path('semestres/<semestre_nombre>/grupos/<curso_grupo_nombre>/sustentacion/<int:curso_grupo_id>/', sustentacion_list, name='sustentacion_list'),
    path('semestres/grupos/sustentaciones/crear/<int:curso_grupo_id>/', sustentacion_create, name='sustentacion_create'),
    path('semestres/grupos/sustentaciones/<int:pk>/editar/', sustentacion_update, name='sustentacion_update'),
    path('semestres/grupos/sustentaciones/<int:pk>/eliminar/', sustentacion_delete, name='sustentacion_delete'),
    path('semestres/grupos/sustentaciones/importar/<int:curso_grupo_id>/', estudiantes_import, name='estudiantes_import'),
    # Semestre academico
    path('semestres/', semestre_list, name='semestre_list'),
    path('semestres/crear/', semestre_create, name='semestre_create'),
    path('semestres/<int:pk>/editar/', semestre_update, name='semestre_update'),
    path('semestres/<int:pk>/eliminar/', semestre_delete, name='semestre_delete'),
    path('semestres/<semestre_nombre>/grupos/', grupos_list, name='grupos_list'),
    path('semestres/<semestre_nombre>/grupos/crear/', grupo_create, name='grupo_create'),
    path('grupos/<int:pk>/editar/', grupo_update, name='grupo_update'),
    path('grupos/<int:pk>/eliminar/', grupo_delete, name='grupo_delete'),
    # Semanas Sustentacion
    path('App/get_semanas/<int:semestre_id>/', views.get_semanas, name='get_semanas'),
    # Disponibilidad profesor
    

    # Authentication
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name="password_change_done"),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', 
        views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]