from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from App.forms import RegistrationForm, SustentacionForm,SemestreAcademicoForm, LoginForm, CursosGruposForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm, ExcelUploadForm, ProfesorForm
from django.contrib.auth import logout
from .models import Profesor, SemestreAcademico, Semestre_Academico_Profesores, Sustentacion, Estudiante, Cursos_Grupos, Curso, Grupo
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ExcelUploadForm
from django.contrib import messages
import pandas as pd

# Create your views here.

# Pages
def index(request):
    return render(request, 'pages/index.html', { 'segment': 'index' })

def billing(request):
    return render(request, 'pages/billing.html', { 'segment': 'billing' })

def tables(request):
    return render(request, 'pages/tables.html', { 'segment': 'tables' })

def vr(request):
    return render(request, 'pages/virtual-reality.html', { 'segment': 'vr' })

def rtl(request):
    return render(request, 'pages/rtl.html', { 'segment': 'rtl' })

def profile(request):
    return render(request, 'pages/profile.html', { 'segment': 'profile' })

# Authentication
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print('Account created successfully!')
            return redirect('/accounts/login/')
        else:
            print("Register failed!")
    else:
        form = RegistrationForm()

    context = { 'form': form }
    return render(request, 'accounts/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')

class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = UserPasswordChangeForm

# Jurados views
@staff_member_required
def jurados_list(request):
    jurados = Semestre_Academico_Profesores.objects.all()
    query = request.GET.get('q')
    if query:
        jurados = jurados.filter(profesor__apellidos_nombres__icontains=query)
    return render(request, 'admin/jurados_list.html', {'jurados': jurados})

@staff_member_required
def jurados_create(request):
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Jurado creado exitosamente")
            return redirect('jurados_list')
    else:
        form = ProfesorForm()
    return render(request, 'admin/jurados_form.html', {'form': form})

@staff_member_required
def jurados_update(request, pk):
    jurado = get_object_or_404(Semestre_Academico_Profesores, pk=pk)
    if request.method == 'POST':
        form = ProfesorForm(request.POST, instance=jurado)
        if form.is_valid():
            form.save()
            messages.success(request, "Jurado actualizado exitosamente")
            return redirect('jurados_list')
    else:
        form = ProfesorForm(instance=jurado)
    return render(request, 'admin/jurados_form.html', {'form': form})

@staff_member_required
def jurados_delete(request, pk):
    jurado = get_object_or_404(Semestre_Academico_Profesores, pk=pk)
    if request.method == 'POST':
        jurado.delete()
        messages.success(request, "Jurado eliminado exitosamente")
        return redirect('jurados_list')
    return render(request, 'admin/jurados_confirm_delete.html', {'jurado': jurado})

@staff_member_required
def jurados_import(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            try:
                df = pd.read_excel(file)
                for index, row in df.iterrows():
                    profesor, created = Profesor.objects.get_or_create(
                        email=row['Email'],
                        defaults={
                            'apellidos_nombres': row['Apellidos y nombres'],
                            'dedicacion': row['Dedicación'],
                            'telefono': row['Teléfono'],
                        }
                    )
                    try:
                        semestre = SemestreAcademico.objects.get(nombre=row['Semestre'])
                    except SemestreAcademico.DoesNotExist:
                        messages.error(request, f"El semestre '{row['Semestre']}' no existe en la base de datos.")
                        continue

                    if Semestre_Academico_Profesores.objects.filter(semestre=semestre, profesor=profesor).exists():
                        messages.error(request, f"El profesor '{profesor}' ya está asignado al semestre '{semestre}'.")
                        continue

                    Semestre_Academico_Profesores.objects.update_or_create(
                        semestre=semestre,
                        profesor=profesor,
                        defaults={'horas_asesoria_semanal': row['Horas de asesoría semanal']}
                    )
                messages.success(request, "Profesores importados exitosamente")
            except Exception as e:
                messages.error(request, f"Error al importar el archivo: {e}")
            return redirect('jurados_list')
    else:
        form = ExcelUploadForm()
    return render(request, 'admin/jurados_import.html', {'form': form})




#Sustentacion
# Crear y listar grupos horarios
@staff_member_required
def sustentacion_list(request, semestre_nombre, curso_grupo_nombre, curso_grupo_id):
    curso_grupo = get_object_or_404(Cursos_Grupos, id=curso_grupo_id)
    sustentaciones = Sustentacion.objects.filter(cursos_grupos=curso_grupo)
    query = request.GET.get('q')
    if query:
        sustentaciones = sustentaciones.filter(titulo__icontains=query)
    return render(request, 'admin/sustentacion_list.html', {'sustentaciones': sustentaciones, 'curso_grupo': curso_grupo})

@staff_member_required
def sustentacion_create(request, curso_grupo_id):
    curso_grupo = get_object_or_404(Cursos_Grupos, id=curso_grupo_id)
    if request.method == 'POST':
        form = SustentacionForm(request.POST)
        if form.is_valid():
            sustentacion = form.save(commit=False)
            sustentacion.cursos_grupos = curso_grupo
            sustentacion.save()
            messages.success(request, "Sustentacion creada exitosamente")
            return redirect('sustentacion_list', semestre_nombre=curso_grupo.semestre.nombre, curso_grupo_nombre=curso_grupo.curso.nombre +"("+ curso_grupo.grupo.nombre +")", curso_grupo_id=curso_grupo.id)
    else:
        form = SustentacionForm(initial={'cursos_grupos': curso_grupo})
    return render(request, 'admin/sustentacion_form.html', {'form': form, 'curso_grupo': curso_grupo})

@staff_member_required
def sustentacion_update(request, pk):
    sustentacion = get_object_or_404(Sustentacion, pk=pk)
    curso_grupo = sustentacion.cursos_grupos
    if request.method == 'POST':
        form = SustentacionForm(request.POST, instance=sustentacion)
        if form.is_valid():
            form.save()
            messages.success(request, "Sustentacion actualizada exitosamente")
            return redirect('sustentacion_list', semestre_nombre=curso_grupo.semestre.nombre, curso_grupo_nombre=curso_grupo.curso.nombre +"("+ curso_grupo.grupo.nombre +")", curso_grupo_id=curso_grupo.id)
    else:
        form = SustentacionForm(instance=sustentacion)
    return render(request, 'admin/sustentacion_form.html', {'form': form, 'curso_grupo': curso_grupo})

@staff_member_required
def sustentacion_delete(request, pk):
    sustentacion = get_object_or_404(Sustentacion, pk=pk)
    curso_grupo = sustentacion.cursos_grupos
    if request.method == 'POST':
        sustentacion.delete()
        messages.success(request, "Sustentacion eliminada exitosamente")
        return redirect('sustentacion_list', curso_grupo_id=curso_grupo.id)
    return render(request, 'admin/sustentacion_confirm_delete.html', {'sustentacion': sustentacion})

@staff_member_required
def estudiantes_import(request, curso_grupo_id):
    curso_grupo = get_object_or_404(Cursos_Grupos, id=curso_grupo_id)
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            try:
                df = pd.read_excel(file)
                for index, row in df.iterrows():
                    # Crear o actualizar el estudiante
                    estudiante, created = Estudiante.objects.get_or_create(
                        codigo_universitario=row['Código Universitario'],
                        defaults={
                            'apellidos_nombres': row['Apellidos y Nombres'],
                            'email': row['Email'],
                            'telefono': row['Telefono'],
                        }
                    )
                    
                    # Obtener los profesores (jurados y asesor)
                    jurado1 = None
                    jurado2 = None
                    asesor = None

                    if not pd.isnull(row['Jurado 1']):
                        try:
                            jurado1 = Profesor.objects.get(apellidos_nombres=row['Jurado 1'])
                        except Profesor.DoesNotExist:
                            messages.error(request, f"El jurado 1 '{row['Jurado 1']}' no existe.")
                            continue

                    if not pd.isnull(row['Jurado 2']):
                        try:
                            jurado2 = Profesor.objects.get(apellidos_nombres=row['Jurado 2'])
                        except Profesor.DoesNotExist:
                            messages.error(request, f"El jurado 2 '{row['Jurado 2']}' no existe.")
                            continue

                    try:
                        asesor = Profesor.objects.get(apellidos_nombres=row['Asesor (Jurado 3)'])
                    except Profesor.DoesNotExist:
                        messages.error(request, f"El asesor '{row['Asesor (Jurado 3)']}' no existe.")
                        continue
                    
                    # Crear la sustentacion
                    Sustentacion.objects.create(
                        cursos_grupos=curso_grupo,
                        estudiante=estudiante,
                        jurado1=jurado1,
                        jurado2=jurado2,
                        asesor=asesor,
                        titulo=row['Título de Tesis']
                    )
                messages.success(request, "Estudiantes y sustentaciones importados exitosamente")
            except Exception as e:
                messages.error(request, f"Error al importar el archivo: {e}")
            return redirect('sustentacion_list', curso_grupo_id=curso_grupo.id)
    else:
        form = ExcelUploadForm()
    return render(request, 'admin/estudiantes_import.html', {'form': form, 'curso_grupo': curso_grupo})





#Semestres form
@staff_member_required
def semestre_list(request):
    semestres = SemestreAcademico.objects.all()
    query = request.GET.get('q')
    if query:
        semestres = semestres.filter(nombre__icontains=query)
    return render(request, 'admin/semestre_list.html', {'semestres': semestres})

@staff_member_required
def semestre_create(request):
    if request.method == 'POST':
        form = SemestreAcademicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Semestre académico creado exitosamente")
            return redirect('semestre_list')
    else:
        form = SemestreAcademicoForm()
    return render(request, 'admin/semestre_form.html', {'form': form})

@staff_member_required
def semestre_update(request, pk):
    semestre = get_object_or_404(SemestreAcademico, pk=pk)
    if request.method == 'POST':
        form = SemestreAcademicoForm(request.POST, instance=semestre)
        if form.is_valid():
            form.save()
            messages.success(request, "Semestre académico actualizado exitosamente")
            return redirect('semestre_list')
    else:
        form = SemestreAcademicoForm(instance=semestre)
    return render(request, 'admin/semestre_form.html', {'form': form})

@staff_member_required
def semestre_delete(request, pk):
    semestre = get_object_or_404(SemestreAcademico, pk=pk)
    if request.method == 'POST':
        semestre.delete()
        messages.success(request, "Semestre académico eliminado exitosamente")
        return redirect('semestre_list')
    return render(request, 'admin/semestre_confirm_delete.html', {'semestre': semestre})



#grupohorario
@staff_member_required
def grupos_list(request, semestre_nombre):
    semestre = get_object_or_404(SemestreAcademico, nombre=semestre_nombre)
    grupos = Cursos_Grupos.objects.filter(semestre=semestre)
    return render(request, 'admin/grupos_list.html', {'grupos': grupos, 'semestre': semestre})

@staff_member_required
def grupo_create(request, semestre_nombre):
    semestre = get_object_or_404(SemestreAcademico, nombre=semestre_nombre)
    if request.method == 'POST':
        form = CursosGruposForm(request.POST)
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.semestre = semestre
            grupo.save()
            messages.success(request, "Grupo horario creado exitosamente")
            return redirect('grupos_list', semestre_nombre=semestre.nombre)
    else:
        form = CursosGruposForm(initial={'semestre': semestre})
    return render(request, 'admin/grupo_form.html', {'form': form, 'semestre': semestre})

@staff_member_required
def grupo_update(request, pk):
    grupo = get_object_or_404(Cursos_Grupos, pk=pk)
    if request.method == 'POST':
        form = CursosGruposForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            messages.success(request, "Grupo horario actualizado exitosamente")
            return redirect('grupos_list', semestre_nombre=grupo.semestre.nombre)
    else:
        form = CursosGruposForm(instance=grupo)
    return render(request, 'admin/grupo_form.html', {'form': form, 'semestre': grupo.semestre})

@staff_member_required
def grupo_delete(request, pk):
    grupo = get_object_or_404(Cursos_Grupos, pk=pk)
    if request.method == 'POST':
        grupo.delete()
        messages.success(request, "Grupo horario eliminado exitosamente")
        return redirect('grupos_list', semestre_nombre=grupo.semestre.nombre)
    return render(request, 'admin/grupo_confirm_delete.html', {'grupo': grupo})

# Semana Sustentacion
def get_semanas(request, semestre_id):
    semestre = get_object_or_404(SemestreAcademico, pk=semestre_id)
    semanas = semestre.calcular_semanas()
    semanas_formateadas = [(str(semana[0]), str(semana[1])) for semana in semanas]
    return JsonResponse(semanas_formateadas, safe=False)

