import random
from datetime import datetime, timedelta
from .models import Estudiante, Profesor, Cursos_Grupos, Sustentacion, Horario_Sustentaciones, Profesores_Semestre_Academico, Semana_Sustentacion, Semestre_Academico_Profesores

class AlgoritmoGenetico:
    def __init__(self, poblacion_size, generaciones, cursos_grupos, disponibilidad_profesores):
        self.poblacion_size = poblacion_size
        self.generaciones = generaciones
        self.cursos_grupos = cursos_grupos
        self.disponibilidad_profesores = disponibilidad_profesores
        self.poblacion = self.inicializar_poblacion()

    def inicializar_poblacion(self):
        poblacion = []
        for _ in range(self.poblacion_size):
            individuo = self.crear_individuo()
            poblacion.append(individuo)
        return poblacion

    def crear_individuo(self):
        individuo = []
        for curso_grupo in self.cursos_grupos:
            sustentaciones = Sustentacion.objects.filter(cursos_grupos=curso_grupo)
            for sustentacion in sustentaciones:
                fecha = self.seleccionar_fecha(curso_grupo.curso)
                sust_data = {
                    'cursos_grupos': curso_grupo,
                    'estudiante': sustentacion.estudiante,
                    'jurado1': sustentacion.jurado1 if sustentacion.jurado1 else self.seleccionar_profesor(curso_grupo),
                    'jurado2': sustentacion.jurado2 if sustentacion.jurado2 else self.seleccionar_profesor(curso_grupo),
                    'asesor': sustentacion.asesor,
                    'titulo': sustentacion.titulo,
                    'fecha': fecha,
                    'hora_inicio': self.seleccionar_hora(fecha),
                    'hora_fin': None
                }
                sust_data['hora_fin'] = (datetime.combine(fecha, sust_data['hora_inicio']) + timedelta(minutes=30)).time()
                individuo.append(sust_data)
        return individuo

    def seleccionar_profesor(self, curso_grupo):
        profesores = Profesor.objects.filter(id__in=Semestre_Academico_Profesores.objects.filter(semestre=curso_grupo.semestre).values_list('profesor_id', flat=True))
        return random.choice(profesores)

    def seleccionar_fecha(self, curso):
        semanas = Semana_Sustentacion.objects.filter(curso=curso)
        if semanas.exists():
            semana = random.choice(semanas)
            start_date = semana.fecha_inicio
            end_date = semana.fecha_fin
            delta = end_date - start_date
            return start_date + timedelta(days=random.randint(0, delta.days))
        return datetime.today().date()

    def seleccionar_hora(self, fecha):
        horas = [datetime.strptime(f"{hour}:00", "%H:%M").time() for hour in range(8, 18)]
        return random.choice(horas)

    def calcular_fitness(self, individuo):
        fitness = 0
        for sustentacion in individuo:
            disponibilidad_jurado1 = self.disponibilidad_profesores.get((sustentacion['jurado1'].id, sustentacion['cursos_grupos'].semestre.id)) if sustentacion['jurado1'] else None
            disponibilidad_jurado2 = self.disponibilidad_profesores.get((sustentacion['jurado2'].id, sustentacion['cursos_grupos'].semestre.id)) if sustentacion['jurado2'] else None
            disponibilidad_asesor = self.disponibilidad_profesores.get((sustentacion['asesor'].id, sustentacion['cursos_grupos'].semestre.id))

            if disponibilidad_jurado1 and disponibilidad_jurado2 and disponibilidad_asesor:
                fitness += 1
        return fitness

    def seleccionar_padres(self):
        padres = random.sample(self.poblacion, 2)
        return padres

    def cruzar(self, padre1, padre2):
        punto_cruce = random.randint(1, len(padre1) - 1)
        hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
        hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
        return hijo1, hijo2

    def mutar(self, individuo):
        if random.random() < 0.1:
            sustentacion_mutada = random.choice(individuo)
            if not sustentacion_mutada['jurado1']:
                sustentacion_mutada['jurado1'] = self.seleccionar_profesor(sustentacion_mutada['cursos_grupos'])
            if not sustentacion_mutada['jurado2']:
                sustentacion_mutada['jurado2'] = self.seleccionar_profesor(sustentacion_mutada['cursos_grupos'])
        return individuo

    def evolucionar(self):
        nueva_poblacion = []
        while len(nueva_poblacion) < self.poblacion_size:
            padres = self.seleccionar_padres()
            hijo1, hijo2 = self.cruzar(padres[0], padres[1])
            nueva_poblacion.append(self.mutar(hijo1))
            nueva_poblacion.append(self.mutar(hijo2))
        self.poblacion = nueva_poblacion

    def ejecutar(self):
        for _ in range(self.generaciones):
            self.poblacion = sorted(self.poblacion, key=lambda ind: self.calcular_fitness(ind), reverse=True)
            self.evolucionar()
        mejor_individuo = max(self.poblacion, key=lambda ind: self.calcular_fitness(ind))
        return mejor_individuo

def generar_horarios():
    cursos_grupos = Cursos_Grupos.objects.all()
    disponibilidad_profesores = {
        (disp.profesor.id, disp.semestre.id): disp
        for disp in Profesores_Semestre_Academico.objects.all()
    }
    ag = AlgoritmoGenetico(poblacion_size=10, generaciones=50, cursos_grupos=cursos_grupos, disponibilidad_profesores=disponibilidad_profesores)
    mejor_horario = ag.ejecutar()
    return mejor_horario

def guardar_horario(mejor_horario):
    for sustentacion in mejor_horario:
        Horario_Sustentaciones.objects.create(
            fecha=sustentacion['fecha'],
            hora_inicio=sustentacion['hora_inicio'],
            hora_fin=sustentacion['hora_fin'],
            sustentacion=Sustentacion.objects.get(
                cursos_grupos=sustentacion['cursos_grupos'],
                estudiante=sustentacion['estudiante'],
                asesor=sustentacion['asesor'],
                titulo=sustentacion['titulo']
            )
        )
