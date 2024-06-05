from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from django import forms

class ExcelUploadForm(forms.Form):
    file = forms.FileField()

class RegistrationForm(UserCreationForm):
  password1 = forms.CharField(
      label=_("Password"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
  )
  password2 = forms.CharField(
      label=_("Password Confirmation"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Confirmation'}),
  )

  class Meta:
    model = User
    fields = ('username', 'email', )

    widgets = {
      'username': forms.TextInput(attrs={
          'class': 'form-control',
          'placeholder': 'Username'
      }),
      'email': forms.EmailInput(attrs={
          'class': 'form-control',
          'placeholder': 'Email'
      })
    }


class LoginForm(AuthenticationForm):
  username = UsernameField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
  password = forms.CharField(
      label=_("Password"),
      strip=False,
      widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
  )

class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label="Nueva contraseña")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label="Confirmar nueva contraseña")
    

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Old Password'
    }), label='Contraseña anterior')
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label="Nueva contraseña")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label="Confirmar nueva contraseña")
    

from django import forms
from .models import *

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Semestre_Academico_Profesores
        fields = ['semestre', 'profesor', 'horas_asesoria_semanal']

    def clean_horas_asesoria_semanal(self):
        horas = self.cleaned_data.get('horas_asesoria_semanal')
        if horas < 0:
            raise forms.ValidationError("Las horas de asesoría semanal no pueden ser negativas.")
        return horas

    def clean(self):
        cleaned_data = super().clean()
        semestre = cleaned_data.get('semestre')
        profesor = cleaned_data.get('profesor')
        
        if self.instance.pk is None:  # Only check uniqueness for new instances
            if Semestre_Academico_Profesores.objects.filter(semestre=semestre, profesor=profesor).exists():
                raise forms.ValidationError("Este profesor ya está asignado a este semestre.")
        
        return cleaned_data

class SustentacionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cursos_grupos'].widget = forms.HiddenInput()

    class Meta:
        model = Sustentacion
        fields = ['cursos_grupos', 'estudiante', 'jurado1', 'jurado2', 'asesor', 'titulo']

class SemestreAcademicoForm(forms.ModelForm):
    class Meta:
        model = SemestreAcademico
        fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'vigencia']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'vigencia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(SemestreAcademicoForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio'].input_formats = ['%Y-%m-%d']
        self.fields['fecha_fin'].input_formats = ['%Y-%m-%d']

class CursosGruposForm(forms.ModelForm):
    class Meta:
        model = Cursos_Grupos
        fields = ['curso', 'grupo', 'profesor', 'semestre']

class Profesores_Semestre_AcademicoForm(forms.ModelForm):
    class Meta:
        model = Profesores_Semestre_Academico
        fields = ['fecha', 'hora_inicio', 'hora_fin']
        
class SemanaSustentacionForm(forms.ModelForm):
    class Meta:
        model = Semana_Sustentacion
        fields = ['semestre_academico', 'curso', 'tipo_sustentacion', 'semana_inicio', 'semana_fin', 'fecha_inicio', 'fecha_fin', 'duracion_sustentacion', 'compensan_horas']
        widgets = {
            'fecha_inicio': forms.TextInput(attrs={'class': 'form-control datepicker', 'placeholder': 'YYYY-MM-DD', 'readonly': 'readonly', 'disabled': 'disabled'}),
            'fecha_fin': forms.TextInput(attrs={'class': 'form-control datepicker', 'placeholder': 'YYYY-MM-DD', 'readonly': 'readonly', 'disabled': 'disabled'}),
        }

    def __init__(self, *args, **kwargs):
        super(SemanaSustentacionForm, self).__init__(*args, **kwargs)
        self.fields['semestre_academico'].queryset = SemestreAcademico.objects.filter(vigencia=True)
        self.fields['semana_inicio'].widget = forms.Select(attrs={
            'data-initial-value': self.instance.semana_inicio if self.instance.pk else 1
        })
        self.fields['semana_fin'].widget = forms.Select(attrs={
            'data-initial-value': self.instance.semana_fin if self.instance.pk else 1
        })
        self.fields['duracion_sustentacion'].label = 'Duración de Sustentación (minutos)'

        # Marcar los campos de fecha como no editables
        self.fields['fecha_inicio'].widget.attrs['readonly'] = True
        self.fields['fecha_inicio'].widget.attrs['disabled'] = True
        self.fields['fecha_fin'].widget.attrs['readonly'] = True
        self.fields['fecha_fin'].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super().clean()
        semana_inicio = cleaned_data.get("semana_inicio")
        semana_fin = cleaned_data.get("semana_fin")

        if semana_inicio and semana_fin and semana_inicio > semana_fin:
            raise forms.ValidationError("La semana de inicio no puede ser mayor que la semana de final.")

        return cleaned_data


from django import forms
from .models import Profesor

class ProfesorForm(forms.ModelForm):
    semestre_academico = forms.ModelChoiceField(queryset=SemestreAcademico.objects.all(), required=True, label="Semestre Académico")
    horas_asesoria_semanal = forms.IntegerField(required=True, label="Horas de Asesoría Semanal")

    class Meta:
        model = Profesor
        fields = ['email', 'apellidos_nombres', 'dedicacion', 'telefono']