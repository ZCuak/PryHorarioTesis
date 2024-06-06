from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User

class Curso(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Grupo(models.Model):
    nombre = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre


class Estudiante(models.Model):
    codigo_universitario = models.CharField(max_length=20, unique=True)
    apellidos_nombres = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.apellidos_nombres


class Profesor(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    apellidos_nombres = models.CharField(max_length=100)
    dedicacion = models.CharField(max_length=2, choices=[('TC', 'Tiempo Completo'), ('TP', 'Tiempo Parcial')])
    telefono = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.apellidos_nombres

    def save(self, *args, **kwargs):
        # Crear usuario en auth_user si no existe
        if not self.user_id:
            username = self.email.split('@')[0]
            user = User(
                username=username,
                email=self.email,
                first_name=self.apellidos_nombres.split(' ')[0],
                last_name=' '.join(self.apellidos_nombres.split(' ')[1:]),
                is_active=True,
                is_staff=True
            )
            user.set_password(self.telefono)
            user.save()
            self.user = user
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"


class SemestreAcademico(models.Model):
    nombre = models.CharField(max_length=7)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    vigencia = models.BooleanField()
    class Meta:
            verbose_name = "Semestre"
            verbose_name_plural = "Semestres"
    def __str__(self):
        return self.nombre

    def calcular_semanas(self):
        semanas = []
        current_start = self.fecha_inicio

        # Ajustar el primer día al lunes si no es lunes
        if current_start.weekday() != 0:
            first_saturday = current_start + timedelta(days=(5 - current_start.weekday()))
        else:
            first_saturday = current_start + timedelta(days=5)
        
        if first_saturday > self.fecha_fin:
            first_saturday = self.fecha_fin
        
        # Primera semana parcial
        semanas.append((current_start, first_saturday))
        
        current_start = first_saturday + timedelta(days=2)  # Saltar al próximo lunes
        
        while current_start + timedelta(days=5) < self.fecha_fin:
            current_end = current_start + timedelta(days=5)
            semanas.append((current_start, current_end))
            current_start = current_end + timedelta(days=2)  # Saltar al próximo lunes
        
        # Última semana parcial
        if current_start <= self.fecha_fin:
            current_end = min(current_start + timedelta(days=5), self.fecha_fin)
            semanas.append((current_start, current_end))
        
        return semanas
    

class Cursos_Grupos(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    semestre = models.ForeignKey(SemestreAcademico, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.curso} - {self.grupo} - {self.semestre}"


class Sustentacion(models.Model):
    cursos_grupos = models.ForeignKey(Cursos_Grupos, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    jurado1 = models.ForeignKey(Profesor, related_name='jurado1', on_delete=models.SET_NULL, null=True, blank=True)
    jurado2 = models.ForeignKey(Profesor, related_name='jurado2', on_delete=models.SET_NULL, null=True, blank=True)
    asesor = models.ForeignKey(Profesor, related_name='asesor', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)

    def __str__(self):
        return self.titulo


class Horario_Sustentaciones(models.Model):
    fecha = models.DateField(null=True, blank=True)
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)
    sustentacion = models.ForeignKey(Sustentacion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fecha} {self.hora_inicio}-{self.hora_fin}"   


class Profesores_Semestre_Academico(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    semestre = models.ForeignKey(SemestreAcademico, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f" {self.semestre} {self.profesor}  {self.fecha} {self.hora_inicio} {self.hora_fin}"
    class Meta:
        verbose_name = "Disp. del profesor"
        verbose_name_plural = "Disps. de los profesores"


class Semana_Sustentacion(models.Model):
    semestre_academico = models.ForeignKey(SemestreAcademico, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    tipo_sustentacion = models.CharField(max_length=7, choices=[('PARCIAL', 'Parcial'), ('FINAL', 'Final')])
    semana_inicio = models.IntegerField()
    semana_fin = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    duracion_sustentacion = models.IntegerField()
    compensan_horas = models.BooleanField()

    def __str__(self):
        return f"{self.semestre_academico} {self.curso} {self.tipo_sustentacion}"
    class Meta:
        verbose_name = "Semana de Sustentación"
        verbose_name_plural = "Semanas de Sustentación"



class Semestre_Academico_Profesores(models.Model):
    semestre = models.ForeignKey(SemestreAcademico, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    horas_asesoria_semanal = models.IntegerField()

    class Meta:
        verbose_name = "Semestre Académico - Profesor"
        verbose_name_plural = "Semestres Académicos - Profesores"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=1, default='P')

    def __str__(self):
        return self.user.username
