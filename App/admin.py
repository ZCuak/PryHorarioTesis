
from .models import (
    Curso, Grupo, Estudiante, Profesor, SemestreAcademico, Cursos_Grupos, Sustentacion,
    Horario_Sustentaciones, Profesores_Semestre_Academico, Semana_Sustentacion, Semestre_Academico_Profesores
)


from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponseRedirect
from .forms import ExcelUploadForm

@admin.register(SemestreAcademico)
class SemestreAcademicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'vigencia')
    search_fields = ('nombre',)
    list_filter = ('vigencia',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:semestre_id>/import-profesores/',
                self.admin_site.admin_view(self.import_profesores),
                name='import-profesores',
            ),
        ]
        return custom_urls + urls

    def import_profesores(self, request, semestre_id):
        semestre = self.get_object(request, semestre_id)
        if request.method == 'POST':
            form = ExcelUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data['file']
                semestre.import_profesores_from_excel(file)
                self.message_user(request, "Profesores importados exitosamente")
                return HttpResponseRedirect(request.path_info)
        else:
            form = ExcelUploadForm()
        context = {
            'title': 'Importar Profesores',
            'form': form,
            'opts': self.model._meta,
            'semestre': semestre,
        }
        return render(request, 'admin/import_profesores.html', context)

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('codigo_universitario', 'apellidos_nombres', 'email', 'telefono')
    search_fields = ('codigo_universitario', 'apellidos_nombres', 'email')
    list_filter = ('apellidos_nombres',)


@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('email', 'apellidos_nombres', 'dedicacion', 'telefono', 'v_jurado')
    search_fields = ('email', 'apellidos_nombres')
    list_filter = ('dedicacion', 'v_jurado')



# @admin.register(Cursos_Grupos)
# class CursosGruposAdmin(admin.ModelAdmin):
#     list_display = ('curso', 'grupo', 'profesor', 'semestre')
#     search_fields = ('curso__nombre', 'grupo__nombre', 'profesor__apellidos_nombres', 'semestre__nombre')
#     list_filter = ('curso', 'grupo', 'profesor', 'semestre')


# @admin.register(Sustentacion)
# class SustentacionAdmin(admin.ModelAdmin):
#     list_display = ('titulo', 'cursos_grupos', 'estudiante', 'jurado1', 'jurado2', 'asesor')
#     search_fields = ('titulo', 'cursos_grupos__curso__nombre', 'estudiante__apellidos_nombres', 'juradoid1__apellidos_nombres', 'juradoid2__apellidos_nombres', 'asesor__apellidos_nombres')
#     list_filter = ('cursos_grupos', 'estudiante')


# @admin.register(Horario_Sustentaciones)
# class HorarioSustentacionesAdmin(admin.ModelAdmin):
#     list_display = ('fecha', 'hora_inicio', 'hora_fin', 'sustentacion')
#     search_fields = ('fecha', 'sustentacion__titulo')
#     list_filter = ('fecha',)


# @admin.register(Profesores_Semestre_Academico)
# class ProfesoresSemestreAcademicoAdmin(admin.ModelAdmin):
#     list_display = ('profesor', 'semestre', 'fecha', 'hora_inicio', 'hora_fin')
#     search_fields = ('profesor__apellidos_nombres', 'semestre__nombre')
#     list_filter = ('profesor', 'semestre')


# @admin.register(Semana_Sustentacion)
# class SemanaSustentacionAdmin(admin.ModelAdmin):
#     list_display = ('semestre_academico', 'curso', 'tipo_sustentacion', 'semana_inicio', 'semana_fin', 'fecha_inicio', 'fecha_fin', 'duracion_sustentacion', 'compensan_horas')
#     search_fields = ('semestre_academico__nombre', 'curso__nombre')
#     list_filter = ('semestre_academico', 'curso', 'tipo_sustentacion')


# @admin.register(Semestre_Academico_Profesores)
# class SemestreAcademicoProfesoresAdmin(admin.ModelAdmin):
#     list_display = ('semestre', 'profesor', 'horas_asesoria_semanal')
#     search_fields = ('semestre__nombre', 'profesor__apellidos_nombres')
#     list_filter = ('semestre', 'profesor')
