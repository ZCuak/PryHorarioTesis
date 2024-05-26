from django.contrib import admin
from .models import Estudiante, Tesis, Jurado, Horario, JuradoTesis

admin.site.register(Estudiante)
admin.site.register(Tesis)
admin.site.register(Jurado)
admin.site.register(Horario)
admin.site.register(JuradoTesis)
