from django.db import models

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

    def __str__(self):
        return self.apellidos_nombres


class SemestreAcademico(models.Model):
    nombre = models.CharField(max_length=7)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    vigencia = models.BooleanField()

    def __str__(self):
        return self.nombre


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
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    sustentacion = models.ForeignKey(Sustentacion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fecha} {self.hora_inicio}-{self.hora_fin}"


class Profesores_Semestre_Academico(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    semestre = models.ForeignKey(SemestreAcademico, on_delete=models.CASCADE)
    fecha = models.IntegerField()
    hora_inicio = models.IntegerField()
    hora_fin = models.IntegerField()


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


class Semestre_Academico_Profesores(models.Model):
    semestre = models.ForeignKey(SemestreAcademico, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    horas_asesoria_semanal = models.IntegerField()
