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
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")
    

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Old Password'
    }), label='Old Password')
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")
    

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
    class Meta:
        model = Sustentacion
        fields = ['cursos_grupos', 'estudiante', 'jurado1', 'jurado2', 'asesor', 'titulo']
        

class SemestreAcademicoForm(forms.ModelForm):
    class Meta:
        model = SemestreAcademico
        fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'vigencia']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'vigencia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CursosGruposForm(forms.ModelForm):
    class Meta:
        model = Cursos_Grupos
        fields = ['curso', 'grupo', 'profesor', 'semestre']

class Profesores_Semestre_AcademicoForm(forms.ModelForm):
    class Meta:
        model = Profesores_Semestre_Academico
        fields = ['fecha', 'hora_inicio', 'hora_fin']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
        
class SemanaSustentacionForm(forms.ModelForm):
    class Meta:
        model = Semana_Sustentacion
        fields = ['semestre_academico', 'curso', 'tipo_sustentacion', 'semana_inicio', 'semana_fin', 'fecha_inicio', 'fecha_fin', 'duracion_sustentacion', 'compensan_horas']

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

    def clean(self):
        cleaned_data = super().clean()
        semana_inicio = cleaned_data.get("semana_inicio")
        semana_fin = cleaned_data.get("semana_fin")

        if semana_inicio and semana_fin and semana_inicio > semana_fin:
            raise forms.ValidationError("La semana de inicio no puede ser mayor que la semana de final.")

        return cleaned_data
