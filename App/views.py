from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from App.forms import  *
from django.contrib.auth import logout
from .models import Profesor, SemestreAcademico, Profile, Semestre_Academico_Profesores, Sustentacion, Estudiante, Cursos_Grupos, Curso, Grupo
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ExcelUploadForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction, DatabaseError
import pandas as pd
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.db import connection
from django.utils.dateparse import parse_datetime
from django.contrib.auth.decorators import login_required
# views.py
from django.http import JsonResponse
from .ga import generar_horarios, guardar_horario
from .utils import send_whatsapp_message

@staff_member_required
def ejecutar_algoritmo(request):
    semestres = SemestreAcademico.objects.all()
    cursos_grupos = Cursos_Grupos.objects.all()
    semestre_id = request.GET.get('semestre')
    tipo_sustentacion = request.GET.get('tipo_sustentacion')
    curso_grupo_id = request.GET.get('curso_grupo')
    sustentaciones = Sustentacion.objects.all()

    if semestre_id:
        sustentaciones = sustentaciones.filter(cursos_grupos__semestre_id=semestre_id)

    if tipo_sustentacion:
        semanas_sustentacion = Semana_Sustentacion.objects.filter(tipo_sustentacion=tipo_sustentacion)
        sustentaciones = sustentaciones.filter(cursos_grupos__curso__in=semanas_sustentacion.values('curso'))

    if curso_grupo_id:
        sustentaciones = sustentaciones.filter(cursos_grupos_id=curso_grupo_id)

    if request.method == 'POST':
        mejor_horario, no_disponibles = generar_horarios()
        if no_disponibles:
            messages.error(request, f"Los siguientes profesores no tienen disponibilidad registrada: {', '.join(no_disponibles)}")
            return render(request, 'admin/ejecutar_algoritmo.html', {
                'sustentaciones': sustentaciones,
                'semestres': semestres,
                'cursos_grupos': cursos_grupos,
                'semestre_id': semestre_id,
                'tipo_sustentacion': tipo_sustentacion,
                'curso_grupo_id': curso_grupo_id
            })
        
        # Convertir objetos a diccionarios
        mejor_horario_dict = [
            {
                'cursos_grupos': {
                    'curso': sustentacion['cursos_grupos'].curso.nombre,
                    'grupo': sustentacion['cursos_grupos'].grupo.nombre,
                    'profesor': sustentacion['cursos_grupos'].profesor.apellidos_nombres,
                    'semestre': sustentacion['cursos_grupos'].semestre.nombre,
                },
                'estudiante': sustentacion['estudiante'].apellidos_nombres,
                'jurado1': sustentacion['jurado1'].apellidos_nombres,
                'jurado2': sustentacion['jurado2'].apellidos_nombres,
                'asesor': sustentacion['asesor'].apellidos_nombres,
                'titulo': sustentacion['titulo'],
                'fecha': sustentacion['fecha'].isoformat(),
                'hora_inicio': sustentacion['hora_inicio'].isoformat(),
                'hora_fin': sustentacion['hora_fin'].isoformat(),
            }
            for sustentacion in mejor_horario
        ]
        # Almacenar el mejor horario en la sesión para usarlo después
        request.session['mejor_horario'] = mejor_horario_dict
        return redirect('mostrar_resultados')

    # Preparar los datos de las sustentaciones para pasarlos a la plantilla
    sustentaciones_json = json.dumps([{
        'estudiante': {
            'id': sustentacion.estudiante.id,
            'telefono': sustentacion.estudiante.telefono
        },
        'jurado1': {
            'id': sustentacion.jurado1.id if sustentacion.jurado1 else None,
            'telefono': sustentacion.jurado1.telefono if sustentacion.jurado1 else None
        },
        'jurado2': {
            'id': sustentacion.jurado2.id if sustentacion.jurado2 else None,
            'telefono': sustentacion.jurado2.telefono if sustentacion.jurado2 else None
        },
        'asesor': {
            'id': sustentacion.asesor.id,
            'telefono': sustentacion.asesor.telefono
        },
        'titulo': sustentacion.titulo,
        'fecha': str(sustentacion.horario_sustentaciones_set.first().fecha) if sustentacion.horario_sustentaciones_set.exists() else None,
        'hora_inicio': str(sustentacion.horario_sustentaciones_set.first().hora_inicio) if sustentacion.horario_sustentaciones_set.exists() else None,
    } for sustentacion in sustentaciones])

    context = {
        'sustentaciones': sustentaciones,
        'semestres': semestres,
        'cursos_grupos': cursos_grupos,
        'semestre_id': semestre_id,
        'tipo_sustentacion': tipo_sustentacion,
        'curso_grupo_id': curso_grupo_id,
        'sustentaciones_json': sustentaciones_json,
    }

    return render(request, 'admin/ejecutar_algoritmo.html', context)


@staff_member_required
def mostrar_resultados(request):
    mejor_horario = request.session.get('mejor_horario', [])
    if mejor_horario:
        return render(request, 'admin/resultado_algoritmo.html', {'mejor_horario': mejor_horario})
    else:
        messages.error(request, "No hay resultados del algoritmo para mostrar.")
        return redirect('ejecutar_algoritmo')


@staff_member_required
def guardar_horarios(request):
    if request.method == 'POST':
        mejor_horario = request.session.get('mejor_horario', [])
        if mejor_horario:
            try:
                with transaction.atomic():
                    for sustentacion_data in mejor_horario:
                        curso = Curso.objects.get(nombre=sustentacion_data['cursos_grupos']['curso'])
                        grupo = Grupo.objects.get(nombre=sustentacion_data['cursos_grupos']['grupo'])
                        semestre = SemestreAcademico.objects.get(nombre=sustentacion_data['cursos_grupos']['semestre'])

                        cursos_grupos = Cursos_Grupos.objects.get_or_create(
                            curso=curso, grupo=grupo, semestre=semestre)[0]

                        estudiante = Estudiante.objects.get(apellidos_nombres=sustentacion_data['estudiante'])
                        jurado1 = Profesor.objects.get(apellidos_nombres=sustentacion_data['jurado1'])
                        jurado2 = Profesor.objects.get(apellidos_nombres=sustentacion_data['jurado2'])
                        asesor = Profesor.objects.get(apellidos_nombres=sustentacion_data['asesor'])

                        # Verificar si la sustentación ya existe por estudiante, curso y grupo
                        sustentacion_existente = Sustentacion.objects.filter(
                            cursos_grupos=cursos_grupos,
                            estudiante=estudiante
                        ).first()

                        if sustentacion_existente:
                            # Actualizar jurados si están en null
                            if not sustentacion_existente.jurado1:
                                sustentacion_existente.jurado1 = jurado1
                            if not sustentacion_existente.jurado2:
                                sustentacion_existente.jurado2 = jurado2
                            if not sustentacion_existente.asesor:
                                sustentacion_existente.asesor = asesor
                            sustentacion_existente.save()

                            Horario_Sustentaciones.objects.create(
                                sustentacion=sustentacion_existente,
                                fecha=sustentacion_data['fecha'],
                                hora_inicio=sustentacion_data['hora_inicio'],
                                hora_fin=sustentacion_data['hora_fin'],
                            )
                        else:
                            # Crear una nueva sustentación si no existe
                            nueva_sustentacion = Sustentacion.objects.create(
                                cursos_grupos=cursos_grupos,
                                estudiante=estudiante,
                                jurado1=jurado1,
                                jurado2=jurado2,
                                asesor=asesor,
                                titulo=sustentacion_data['titulo']
                            )
                            Horario_Sustentaciones.objects.create(
                                sustentacion=nueva_sustentacion,
                                fecha=sustentacion_data['fecha'],
                                hora_inicio=sustentacion_data['hora_inicio'],
                                hora_fin=sustentacion_data['hora_fin'],
                            )

                    messages.success(request, "Horarios guardados exitosamente.")
            except Exception as e:
                messages.error(request, f"Error al guardar horarios: {str(e)}")
                return redirect('ejecutar_algoritmo')
        else:
            messages.error(request, "No hay horarios para guardar.")
        return redirect('ejecutar_algoritmo')
    return redirect('home')



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
@transaction.atomic
def jurados_create(request):
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            profesor = form.save()

            # Obtener los datos adicionales del formulario
            semestre_academico = form.cleaned_data['semestre_academico']
            horas_asesoria_semanal = form.cleaned_data['horas_asesoria_semanal']

            # Crear el registro en Semestre_Academico_Profesores
            Semestre_Academico_Profesores.objects.create(
                semestre=semestre_academico,
                profesor=profesor,
                horas_asesoria_semanal=horas_asesoria_semanal
            )

            messages.success(request, "Jurado creado exitosamente")
            return redirect('jurados_list')
    else:
        form = ProfesorForm()
    return render(request, 'admin/jurados_form.html', {'form': form})

@staff_member_required
def jurados_update(request, pk):
    semestre_academico_profesor = get_object_or_404(Semestre_Academico_Profesores, pk=pk)
    profesor = semestre_academico_profesor.profesor

    if request.method == 'POST':
        form = ProfesorForm(request.POST, instance=profesor)
        if form.is_valid():
            profesor = form.save()

            # Actualizar los datos adicionales del modelo Semestre_Academico_Profesores
            semestre_academico_profesor.semestre = form.cleaned_data['semestre_academico']
            semestre_academico_profesor.horas_asesoria_semanal = form.cleaned_data['horas_asesoria_semanal']
            semestre_academico_profesor.save()

            messages.success(request, "Jurado actualizado exitosamente")
            return redirect('jurados_list')
    else:
        initial_data = {
            'semestre_academico': semestre_academico_profesor.semestre,
            'horas_asesoria_semanal': semestre_academico_profesor.horas_asesoria_semanal,
        }
        form = ProfesorForm(instance=profesor, initial=initial_data)

    return render(request, 'admin/jurados_form.html', {'form': form})
@staff_member_required
def jurados_delete(request, pk):
    jurado = get_object_or_404(Semestre_Academico_Profesores, pk=pk)
    if request.method == 'POST':
        jurado.delete()
        messages.success(request, "Jurado eliminado exitosamente")
        return redirect('jurados_list')
    return render(request, 'admin/jurados_confirm_delete.html', {'jurado': jurado})




from django.db import transaction
from django.contrib.auth.models import User
from App.models import *

@staff_member_required
def jurados_import(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            try:
                df = pd.read_excel(file)
                with transaction.atomic():
                    for index, row in df.iterrows():
                        email = row['Email']
                        username = email.split('@')[0]
                        telefono = str(row['Teléfono'])  # Convertir a cadena para la contraseña

                        # Crear usuario en auth_user
                        user, user_created = User.objects.get_or_create(
                            username=username,
                            defaults={
                                'email': email,
                                'first_name': row['Apellidos y nombres'].split(' ')[0],  # Primer nombre
                                'last_name': ' '.join(row['Apellidos y nombres'].split(' ')[1:]),  # Apellidos
                                'is_staff': True,
                                'is_active': True,
                            }
                        )
                        if user_created:
                            user.set_password(telefono)
                            user.save()
                        else:
                            user.email = email
                            user.set_password(telefono)
                            user.first_name = row['Apellidos y nombres'].split(' ')[0]
                            user.last_name = ' '.join(row['Apellidos y nombres'].split(' ')[1:])
                            user.save()

                        # Crear o actualizar el perfil
                        profile, profile_created = Profile.objects.get_or_create(
                            user=user,
                            defaults={'rol': 'P'}
                        )
                        if not profile_created:
                            profile.rol = 'P'
                            profile.save()

                        # Crear profesor
                        profesor, created = Profesor.objects.get_or_create(
                            email=email,
                            defaults={
                                'apellidos_nombres': row['Apellidos y nombres'],
                                'dedicacion': row['Dedicación'],
                                'telefono': telefono,
                                'user': user
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
        return redirect('sustentacion_list', semestre_nombre=curso_grupo.semestre.nombre, curso_grupo_nombre=curso_grupo.curso.nombre +"("+ curso_grupo.grupo.nombre +")", curso_grupo_id=curso_grupo.id)
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
                    
                    # Verificar si el estudiante ya está registrado en el mismo curso y grupo
                    if Sustentacion.objects.filter(cursos_grupos=curso_grupo, estudiante=estudiante).exists():
                        messages.warning(request, f"El estudiante '{estudiante.apellidos_nombres}' ya está registrado en este curso y grupo.")
                        continue
                    
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
            return redirect('sustentacion_list', semestre_nombre=curso_grupo.semestre.nombre, curso_grupo_nombre=curso_grupo.curso.nombre + "(" + curso_grupo.grupo.nombre + ")", curso_grupo_id=curso_grupo.id)
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
            if form.cleaned_data['vigencia']:
                # Si este semestre se establece como vigente, desactivar los demás
                SemestreAcademico.objects.update(vigencia=False)
            form.save()
            messages.success(request, "Semestre académico creado exitosamente")
            return redirect('semestre_list')
    else:
        form = SemestreAcademicoForm()
    return render(request, 'admin/semestre_form.html', {'form': form})



@staff_member_required
def disponibilidad_list(request):
    # Realizar la consulta SQL específica
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                assu.semana_inicio, 
                assu.semana_fin
            FROM 
                app_profesores_semestre_academico aps
            INNER JOIN 
                app_semestreacademico asap ON asap.id = aps.semestre_id
            INNER JOIN 
                app_semana_sustentacion assu ON assu.semestre_academico_id = asap.id
            GROUP BY 
                assu.semana_inicio, 
                assu.semana_fin
            ORDER BY 
                assu.semana_inicio
        """)
        disponibilidades = cursor.fetchall()

    return render(request, 'profesor/disponibilidad_list.html', {'disponibilidades': disponibilidades})

@staff_member_required
@csrf_exempt
def disponibilidad_create(request):
    usuario_logueado = request.user
    profesor_logueado = get_object_or_404(Profesor, user=usuario_logueado)
    semestre_academico = get_object_or_404(SemestreAcademico, vigencia=True)

    if request.method == 'POST':
        # Obtener semanas de la URL
        semana_inicio = int(request.GET.get('semana_inicio'))
        semana_fin = int(request.GET.get('semana_fin'))

        # Calcular las fechas de inicio y fin de las semanas seleccionadas
        semanas = semestre_academico.calcular_semanas()
        fecha_inicio_semana = semanas[semana_inicio - 1][0]
        fecha_fin_semana = semanas[semana_fin - 1][1]

        # Borrar todas las disponibilidades existentes del profesor para esas semanas
        Profesores_Semestre_Academico.objects.filter(
            profesor=profesor_logueado,
            semestre=semestre_academico,
            fecha__range=[fecha_inicio_semana, fecha_fin_semana]
        ).delete()

        # Procesar la solicitud POST para guardar nuevas disponibilidades
        try:
            event_data = json.loads(request.body)
            for event in event_data:
                start = parse_datetime(event['start'])
                end = parse_datetime(event['end'])
                Profesores_Semestre_Academico.objects.create(
                    profesor=profesor_logueado,
                    semestre=semestre_academico,
                    fecha=start.date(),
                    hora_inicio=start.time(),
                    hora_fin=end.time()
                )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f"Error al guardar las disponibilidades: {e}")
            return JsonResponse({'status': 'error'})

    # Obtener las disponibilidades existentes
    disponibilidades = Profesores_Semestre_Academico.objects.filter(
        profesor=profesor_logueado,
        semestre=semestre_academico
    ).values_list('fecha', 'hora_inicio', 'hora_fin', 'profesor__apellidos_nombres')

    return render(request, 'profesor/disponibilidad_form.html', {
        'disponibilidades': disponibilidades
    })



@staff_member_required
def obtener_fechas_min_max(request):
    semana_inicio = request.GET.get('semana_inicio')
    semana_fin = request.GET.get('semana_fin')

    # Asegúrate de convertir semana_inicio y semana_fin en enteros
    semana_inicio = int(semana_inicio)
    semana_fin = int(semana_fin)

    # Obtén las fechas de inicio y fin del semestre
    semestre = SemestreAcademico.objects.get(vigencia=True)  # Ajusta según tus requisitos
    semanas = semestre.calcular_semanas()

    fecha_inicio_min = semanas[semana_inicio - 1][0]
    fecha_fin_max = semanas[semana_fin - 1][1]

    return JsonResponse({
        'fecha_inicio_min': fecha_inicio_min,
        'fecha_fin_max': fecha_fin_max,
    })
    
@staff_member_required
def ver_disponibilidad(request, semana_inicio, semana_fin):
    usuario_logueado = request.user
    try:
        profesor_logueado = Profesor.objects.get(user=usuario_logueado)
        
        # Obtener el semestre académico vigente
        semestre_academico = get_object_or_404(SemestreAcademico, vigencia=True)

        # Calcular las semanas del semestre
        semanas = semestre_academico.calcular_semanas()
        
        # Obtener las fechas de inicio y fin de las semanas seleccionadas
        fecha_inicio_semana = semanas[semana_inicio - 1][0]
        fecha_fin_semana = semanas[semana_fin - 1][1]
        
        # Realizar la consulta SQL específica
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        aps.id, aps.fecha, aps.hora_inicio, aps.hora_fin, 
                        ap.apellidos_nombres
                    FROM 
                        app_profesores_semestre_academico aps
                    INNER JOIN 
                        app_profesor ap ON aps.profesor_id = ap.id
                    INNER JOIN 
                        app_semestreacademico sem ON aps.semestre_id = sem.id
                    WHERE 
                        aps.fecha >= %s AND aps.fecha <= %s AND ap.id = %s AND sem.vigencia = true
                """, [fecha_inicio_semana, fecha_fin_semana, profesor_logueado.id])
                disponibilidades = cursor.fetchall()
        except DatabaseError as e:
            disponibilidades = []
            print(f"Error en la base de datos: {e}")

    except Profesor.DoesNotExist:
        disponibilidades = []

    return render(request, 'profesor/ver_disponibilidad.html', {
        'disponibilidades': disponibilidades,
        'semana_inicio': semana_inicio,
        'semana_fin': semana_fin
    })
    
   
    
@staff_member_required
def semestre_update(request, pk):
    semestre = get_object_or_404(SemestreAcademico, pk=pk)
    if request.method == 'POST':
        form = SemestreAcademicoForm(request.POST, instance=semestre)
        if form.is_valid():
            if form.cleaned_data['vigencia']:
                # Si este semestre se establece como vigente, desactivar los demás
                SemestreAcademico.objects.exclude(pk=semestre.pk).update(vigencia=False)
            form.save()
            messages.success(request, "Semestre académico actualizado exitosamente")
            return redirect('semestre_list')
    else:
        form = SemestreAcademicoForm(instance=semestre)
        print(f"Fecha Inicio: {semestre.fecha_inicio}, Fecha Fin: {semestre.fecha_fin}")
    return render(request, 'admin/semestre_form.html', {'form': form, 'semestre': semestre})



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
#PARA REPORTES

from django.shortcuts import render
from django.http import HttpResponse
import csv

from django.http import HttpResponse
from django.db import connection
import openpyxl
from openpyxl.utils import get_column_letter

#Reporte 1: Sustentaciones

def reporte_sustentaciones(request):
    semestre = request.GET.get('semestre', '')
    tipo_sustentacion = request.GET.get('tipo_sustentacion', '')
    nombre_estudiante = request.GET.get('nombre_estudiante', '')
    codigo_estudiante = request.GET.get('codigo_estudiante', '')
    fecha = request.GET.get('fecha', '')
    
    # Obtener la lista de semestres
    semestres = SemestreAcademico.objects.all()

    sql = """
    SELECT 
    appsa.nombre as semestre,
    appc.nombre as curso,
    appg.nombre as grupo,
    appe.codigo_universitario, 
    appe.apellidos_nombres as estudiante,
    appe.email as email_estudiante,
    appe.telefono as telefono_estudiante,
    appc.nombre as curso,
    appss.tipo_sustentacion,
    app1.apellidos_nombres as jurado1,
    app2.apellidos_nombres as jurado2,
    app3.apellidos_nombres as asesor,
    apphs.fecha,
    apphs.hora_inicio,
    apphs.hora_fin,
    apps.titulo
    FROM app_sustentacion apps
    INNER JOIN app_cursos_grupos appcg on apps.cursos_grupos_id=appcg.id
    INNER JOIN app_curso appc on appc.id=appcg.curso_id
    INNER JOIN app_grupo appg on appg.id=appcg.grupo_id
    INNER JOIN app_estudiante appe on appe.id=apps.estudiante_id
    INNER JOIN app_profesor app1 on app1.id=apps.jurado1_id
    INNER JOIN app_profesor app2 on app2.id=apps.jurado2_id
    INNER JOIN app_profesor app3 on app3.id=apps.asesor_id
    INNER JOIN app_horario_sustentaciones apphs on apphs.sustentacion_id=apps.id
    INNER JOIN app_semana_sustentacion appss on appss.curso_id=appc.id
    INNER JOIN app_semestreacademico appsa ON appsa.id=appss.semestre_academico_id
    WHERE 1=1
    """

    params = []
    
    if semestre:
        sql += " AND appsa.nombre = %s"
        params.append(semestre)
    
    if tipo_sustentacion:
        sql += " AND appss.tipo_sustentacion = %s"
        params.append(tipo_sustentacion)
    
    if nombre_estudiante:
        sql += " AND appe.apellidos_nombres LIKE %s"
        params.append(f'%{nombre_estudiante}%')
    
    if codigo_estudiante:
        sql += " AND appe.codigo_universitario = %s"
        params.append(codigo_estudiante)
    
    if fecha:
        sql += " AND apphs.fecha = %s"
        params.append(fecha)
    
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    data = [
        dict(zip(columns, row))
        for row in rows
    ]

    context = {
        'data': data,
        'semestre': semestre,
        'tipo_sustentacion': tipo_sustentacion,
        'nombre_estudiante': nombre_estudiante,
        'codigo_estudiante': codigo_estudiante,
        'fecha': fecha,
        'semestres': semestres,  # Pasar los semestres al contexto
    }

    return render(request, 'admin/reporte_sustentaciones.html', context)



def exportar_csv(request):
    semestre = request.GET.get('semestre')
    tipo_sustentacion = request.GET.get('tipo_sustentacion')
    nombre_estudiante = request.GET.get('nombre_estudiante')
    codigo_estudiante = request.GET.get('codigo_estudiante')
    fecha = request.GET.get('fecha')
    
    sql = """
    SELECT 
    appsa.nombre as semestre,
    appc.nombre as curso,
    appg.nombre as grupo,
    appe.codigo_universitario, 
    appe.apellidos_nombres as estudiante,
    appe.email as email_estudiante,
    appe.telefono as telefono_estudiante,
    appc.nombre as curso,
    appss.tipo_sustentacion,
    app1.apellidos_nombres as jurado1,
    app2.apellidos_nombres as jurado2,
    app3.apellidos_nombres as asesor,
    apphs.fecha,
    apphs.hora_inicio,
    apphs.hora_fin,
    apps.titulo
    FROM app_sustentacion apps
    INNER JOIN app_cursos_grupos appcg on apps.cursos_grupos_id=appcg.id
    INNER JOIN app_curso appc on appc.id=appcg.curso_id
    INNER JOIN app_grupo appg on appg.id=appcg.grupo_id
    INNER JOIN app_estudiante appe on appe.id=apps.estudiante_id
    INNER JOIN app_profesor app1 on app1.id=apps.jurado1_id
    INNER JOIN app_profesor app2 on app2.id=apps.jurado2_id
    INNER JOIN app_profesor app3 on app3.id=apps.asesor_id
    INNER JOIN app_horario_sustentaciones apphs on apphs.sustentacion_id=apps.id
    INNER JOIN app_semana_sustentacion appss on appss.curso_id=appc.id
    INNER JOIN app_semestreacademico appsa ON appsa.id=appss.semestre_academico_id
    WHERE 1=1
    """

    params = []
    
    if semestre:
        sql += " AND appsa.nombre = %s"
        params.append(semestre)
    
    if tipo_sustentacion:
        sql += " AND appss.tipo_sustentacion = %s"
        params.append(tipo_sustentacion)
    
    if nombre_estudiante:
        sql += " AND appe.apellidos_nombres LIKE %s"
        params.append(f'%{nombre_estudiante}%')
    
    if codigo_estudiante:
        sql += " AND appe.codigo_universitario = %s"
        params.append(codigo_estudiante)
    
    if fecha:
        sql += " AND apphs.fecha = %s"
        params.append(fecha)
    
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    # Crear el libro de Excel
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Sustentaciones"

    # Escribir los encabezados de columna
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=1, column=col_num)
        cell.value = column_title

    # Escribir los datos
    for row_num, row_data in enumerate(rows, 2):
        for col_num, cell_value in enumerate(row_data, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value

    # Ajustar el ancho de las columnas
    for col_num, column_title in enumerate(columns, 1):
        column_letter = get_column_letter(col_num)
        worksheet.column_dimensions[column_letter].width = 15

    # Preparar la respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="sustentaciones.xlsx"'
    
    # Guardar el libro en la respuesta
    workbook.save(response)
    
    return response



#Reporte 2: list sustentaciones por docente
from django.http import HttpResponse
from django.db import connection
import openpyxl
from openpyxl.utils import get_column_letter
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def listar_sustentaciones(request):
    usuario_id = request.user.id
    sql_profesor_id = """
        SELECT id FROM app_profesor WHERE user_id = %s
    """
    
    with connection.cursor() as cursor:
        cursor.execute(sql_profesor_id, [usuario_id])
        profesor_id = cursor.fetchone()[0]

    sql = """
    SELECT 
        appc.nombre AS curso,
        appg.nombre AS grupo,
        appe.codigo_universitario,
        appe.apellidos_nombres AS estudiante,
        apphs.fecha,
        apphs.hora_inicio,
        apps.titulo
    FROM app_sustentacion apps
    INNER JOIN app_estudiante appe ON appe.id = apps.estudiante_id
    LEFT JOIN app_profesor app1 ON app1.id = apps.jurado1_id
    LEFT JOIN app_profesor app2 ON app2.id = apps.jurado2_id
    LEFT JOIN app_profesor app3 ON app3.id = apps.asesor_id
    INNER JOIN app_cursos_grupos appcg ON apps.cursos_grupos_id = appcg.id
    INNER JOIN app_curso appc ON appc.id = appcg.curso_id
    INNER JOIN app_grupo appg ON appg.id = appcg.grupo_id
    INNER JOIN app_horario_sustentaciones apphs ON apphs.sustentacion_id = apps.id
    WHERE apps.jurado1_id = %s OR apps.jurado2_id = %s OR apps.asesor_id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [profesor_id, profesor_id, profesor_id])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    data = [dict(zip(columns, row)) for row in rows]

    return render(request, 'profesor/listar_sustentaciones.html', {'data': data})
 
def exportar_excel_profesor(request):
    usuario_id = request.user.id
    sql_profesor_id = """
        SELECT id FROM app_profesor WHERE user_id = %s
    """
    
    with connection.cursor() as cursor:
        cursor.execute(sql_profesor_id, [usuario_id])
        profesor_id = cursor.fetchone()[0]
    
    sql = """
    SELECT 
        appc.nombre AS curso,
        appg.nombre AS grupo,
        appe.codigo_universitario,
        appe.apellidos_nombres AS estudiante,
        apphs.fecha,
        apphs.hora_inicio,
        apps.titulo
    FROM app_sustentacion apps
    INNER JOIN app_estudiante appe ON appe.id = apps.estudiante_id
    LEFT JOIN app_profesor app1 ON app1.id = apps.jurado1_id
    LEFT JOIN app_profesor app2 ON app2.id = apps.jurado2_id
    LEFT JOIN app_profesor app3 ON app3.id = apps.asesor_id
    INNER JOIN app_cursos_grupos appcg ON apps.cursos_grupos_id = appcg.id
    INNER JOIN app_curso appc ON appc.id = appcg.curso_id
    INNER JOIN app_grupo appg ON appg.id = appcg.grupo_id
    INNER JOIN app_horario_sustentaciones apphs ON apphs.sustentacion_id = apps.id
    WHERE apps.jurado1_id = %s OR apps.jurado2_id = %s OR apps.asesor_id = %s
    """
    
    with connection.cursor() as cursor:
        cursor.execute(sql, [profesor_id, profesor_id, profesor_id])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    # Crear el libro de Excel
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Sustentaciones"

    # Escribir los encabezados de columna
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=1, column=col_num)
        cell.value = column_title

    # Escribir los datos
    for row_num, row_data in enumerate(rows, 2):
        for col_num, cell_value in enumerate(row_data, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value

    # Ajustar el ancho de las columnas
    for col_num, column_title in enumerate(columns, 1):
        column_letter = get_column_letter(col_num)
        worksheet.column_dimensions[column_letter].width = 15

    # Preparar la respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="sustentaciones_profesor.xlsx"'
    
    # Guardar el libro en la respuesta
    workbook.save(response)
    
    return response

@login_required
def user_profile(request):
    user = request.user

   
def send_bulk_messages_view(request):
    if request.method == 'POST':
        number = '+51916702954'
        sustentaciones = Sustentacion.objects.all()
        message = "Listado de Sustentaciones:\n"
        for sustentacion in sustentaciones:
            message += f"Curso - Grupo: {sustentacion.cursos_grupos.curso.nombre} - {sustentacion.cursos_grupos.grupo.nombre}\n"
        result = send_whatsapp_message(number, message)
        print(message)
        
        if result:
            return JsonResponse({'status': 'success', 'result': result})
        else:
            return JsonResponse({'status': 'fail', 'message': 'Error al enviar el mensaje'})
    
    return JsonResponse({'status': 'fail', 'message': 'Invalid request method'})

