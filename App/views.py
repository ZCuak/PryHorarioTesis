from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from App.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm, ExcelUploadForm, ProfesorForm
from django.contrib.auth import logout
from .models import Profesor, SemestreAcademico, Semestre_Academico_Profesores
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