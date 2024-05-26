from django.db import models

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Tesis(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_entrega = models.DateField()
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo


class Jurado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Horario(models.Model):
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    tesis = models.ForeignKey(Tesis, on_delete=models.CASCADE)

    def __str__(self):
        return f"Horario {self.fecha} {self.hora_inicio}-{self.hora_fin}"


class JuradoTesis(models.Model):
    jurado = models.ForeignKey(Jurado, on_delete=models.CASCADE)
    tesis = models.ForeignKey(Tesis, on_delete=models.CASCADE)
