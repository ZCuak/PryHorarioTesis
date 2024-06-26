
from .models import (
    Curso, Grupo, Estudiante, Profesor, SemestreAcademico, Cursos_Grupos, Sustentacion,
    Horario_Sustentaciones, Profesores_Semestre_Academico, Semana_Sustentacion, Semestre_Academico_Profesores
)


from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponseRedirect, JsonResponse
from .forms import ExcelUploadForm, SemanaSustentacionForm
from App.views import get_semanas
from .forms import ProfesorForm2

# @admin.register(SemestreAcademico)
# class SemestreAcademicoAdmin(admin.ModelAdmin):
#     list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'vigencia')
#     search_fields = ('nombre',)
#     list_filter = ('vigencia',)

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path(
#                 '<int:semestre_id>/import-profesores/',
#                 self.admin_site.admin_view(self.import_profesores),
#                 name='import-profesores',
#             ),
#         ]
#         return custom_urls + urls

#     def import_profesores(self, request, semestre_id):
#         semestre = self.get_object(request, semestre_id)
#         if request.method == 'POST':
#             form = ExcelUploadForm(request.POST, request.FILES)
#             if form.is_valid():
#                 file = form.cleaned_data['file']
#                 semestre.import_profesores_from_excel(file)
#                 self.message_user(request, "Profesores importados exitosamente")
#                 return HttpResponseRedirect(request.path_info)
#         else:
#             form = ExcelUploadForm()
#         context = {
#             'title': 'Importar Profesores',
#             'form': form,
#             'opts': self.model._meta,
#             'semestre': semestre,
#         }
#         return render(request, 'admin/import_profesores.html', context)

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



@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    form = ProfesorForm2
    list_display = ('email', 'apellidos_nombres', 'dedicacion', 'telefono')
    search_fields = ('email', 'apellidos_nombres')


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

# @admin.register(Profesores_Semestre_Academico)
# class DisponibilidadProfesorAdmin(admin.ModelAdmin):
#     list_display = ('semestre', 'profesor', 'fecha', 'hora_inicio', 'hora_fin')
#     list_filter = ('profesor', )

    

@admin.register(Semana_Sustentacion)
class SemanaSustentacionAdmin(admin.ModelAdmin):
    form = SemanaSustentacionForm
    list_display = ('semestre_academico', 'curso', 'tipo_sustentacion', 'semana_inicio', 'semana_fin', 'fecha_inicio', 'fecha_fin', 'duracion_sustentacion', 'compensan_horas')
    search_fields = ('semestre_academico__nombre', 'curso__nombre')
    list_filter = ('curso', 'tipo_sustentacion')
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('App/get_semanas/<int:semestre_id>/', self.admin_site.admin_view(get_semanas), name='get_semanas')
        ]
        return custom_urls + urls
    
    def get_semanas(self, request, semestre_id):
        semestre = SemestreAcademico.objects.get(pk=semestre_id)
        semanas = semestre.calcular_semanas()
        semanas_formateadas = [(str(semana[0]), str(semana[1])) for semana in semanas]
        return JsonResponse(semanas_formateadas, safe=False)
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_change_form'] = True
        return super(SemanaSustentacionAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

# @admin.register(Semestre_Academico_Profesores)
# class SemestreAcademicoProfesoresAdmin(admin.ModelAdmin):
#     list_display = ('semestre', 'profesor', 'horas_asesoria_semanal')
#     search_fields = ('semestre__nombre', 'profesor__apellidos_nombres')
#     list_filter = ('semestre', 'profesor')
