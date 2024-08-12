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

class ProfesorForm2(forms.ModelForm):

    class Meta:
        model = Profesor
        fields = ['email', 'apellidos_nombres', 'dedicacion', 'telefono']
        


class SustentacionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cursos_grupos'].widget = forms.HiddenInput()

    class Meta:
        model = Sustentacion
        fields = ['cursos_grupos', 'estudiante', 'jurado1', 'jurado2', 'asesor', 'titulo']

class Horario_SustentacionForm(forms.ModelForm):
    fecha = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d']
    )
    hora_inicio = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    hora_fin = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )

    class Meta:
        model = Sustentacion
        fields = ['cursos_grupos', 'estudiante', 'jurado1', 'jurado2', 'asesor', 'titulo']
        widgets = {
            'cursos_grupos': forms.Select(attrs={'class': 'form-control'}),
            'estudiante': forms.Select(attrs={'class': 'form-control'}),
            'jurado1': forms.Select(attrs={'class': 'form-control'}),
            'jurado2': forms.Select(attrs={'class': 'form-control'}),
            'asesor': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        jurado1 = cleaned_data.get("jurado1")
        jurado2 = cleaned_data.get("jurado2")
        asesor = cleaned_data.get("asesor")

        if jurado1 and jurado2 and jurado1 == jurado2:
            raise forms.ValidationError("Jurado 1 y Jurado 2 no pueden ser la misma persona.")

        if jurado1 and asesor and jurado1 == asesor:
            raise forms.ValidationError("Jurado 1 y el Asesor no pueden ser la misma persona.")

        if jurado2 and asesor and jurado2 == asesor:
            raise forms.ValidationError("Jurado 2 y el Asesor no pueden ser la misma persona.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['jurado1'].queryset = Profesor.objects.none()
        self.fields['jurado2'].queryset = Profesor.objects.none()
        self.fields['asesor'].queryset = Profesor.objects.none()
        if 'fecha' in self.data:
            
            fecha = self.data.get('fecha')
            self.fields['jurado1'].queryset = Profesor.objects.filter(
                id__in=Profesores_Semestre_Academico.objects.filter(fecha=fecha).values_list('profesor_id', flat=True)
            )
            self.fields['jurado2'].queryset = self.fields['jurado1'].queryset
            self.fields['asesor'].queryset = self.fields['jurado1'].queryset
        elif self.instance.pk:
            # Pre-popular los selects si la instancia ya existe
            self.fields['jurado1'].queryset = Profesor.objects.all()
            self.fields['jurado2'].queryset = Profesor.objects.all()
            self.fields['asesor'].queryset = Profesor.objects.all()


    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            Horario_Sustentaciones.objects.update_or_create(
                sustentacion=instance,
                defaults={
                    'fecha': self.cleaned_data.get('fecha'),
                    'hora_inicio': self.cleaned_data.get('hora_inicio'),
                    'hora_fin': self.cleaned_data.get('hora_fin')
                }
            )
        return instance

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
            'fecha_inicio': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD', 'readonly': 'readonly'}),
            'fecha_fin': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD', 'readonly': 'readonly'}),
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
        self.fields['fecha_fin'].widget.attrs['readonly'] = True


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
        
class DisponibilidadForm(forms.Form):
    profesor = forms.ModelChoiceField(queryset=Profesor.objects.all(), required=False)
    semana_inicio = forms.IntegerField(widget=forms.HiddenInput())
    semana_fin = forms.IntegerField(widget=forms.HiddenInput())
    
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