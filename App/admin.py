from django.contrib import admin
from .models import Estudiante, Tesis, Jurado, Horario, JuradoTesis

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'telefono')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('nombre', 'apellido')

@admin.register(Tesis)
class TesisAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'fecha_entrega', 'estudiante')
    search_fields = ('titulo', 'descripcion')
    list_filter = ('fecha_entrega', 'estudiante')
    raw_id_fields = ('estudiante',)

@admin.register(Jurado)
class JuradoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'telefono')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('nombre', 'apellido')

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'hora_inicio', 'hora_fin', 'tesis')
    search_fields = ('fecha', 'tesis__titulo')
    list_filter = ('fecha', 'tesis')
    raw_id_fields = ('tesis',)

@admin.register(JuradoTesis)
class JuradoTesisAdmin(admin.ModelAdmin):
    list_display = ('jurado', 'tesis')
    search_fields = ('jurado__nombre', 'jurado__apellido', 'tesis__titulo')
    list_filter = ('jurado', 'tesis')
    raw_id_fields = ('jurado', 'tesis')


