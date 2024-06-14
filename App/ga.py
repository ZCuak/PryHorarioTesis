import random
from datetime import datetime, timedelta
from django.db import models
from .models import *

class AlgoritmoGenetico:
    def __init__(self, poblacion_size, generaciones, cursos_grupos, disponibilidad_profesores, fechas_sustentacion):
        self.poblacion_size = poblacion_size
        self.generaciones = generaciones
        self.cursos_grupos = cursos_grupos
        self.disponibilidad_profesores = disponibilidad_profesores
        self.fechas_sustentacion = fechas_sustentacion
        self.duracion_sustentacion = timedelta(minutes=30)  # Duración de la sustentación de 30 minutos
        self.poblacion = self.inicializar_poblacion()

    def inicializar_poblacion(self):
        print("Inicializando población...")
        poblacion = [self.crear_individuo() for _ in range(self.poblacion_size)]
        return poblacion

    def crear_individuo(self):
        individuo = []
        for curso_grupo in self.cursos_grupos:
            sustentaciones = Sustentacion.objects.filter(cursos_grupos=curso_grupo)
            for sustentacion in sustentaciones:
                jurado1, jurado2, asesor = self.asignar_jurados_y_asesor(curso_grupo)
                fecha, hora_inicio, hora_fin = self.seleccionar_fecha_hora(jurado1, jurado2, asesor, curso_grupo.curso)
                if fecha and hora_inicio and hora_fin:
                    sust_data = {
                        'cursos_grupos': curso_grupo,
                        'estudiante': sustentacion.estudiante,
                        'jurado1': jurado1,
                        'jurado2': jurado2,
                        'asesor': asesor,
                        'titulo': sustentacion.titulo,
                        'fecha': fecha,
                        'hora_inicio': hora_inicio,
                        'hora_fin': hora_fin
                    }
                    individuo.append(sust_data)
        return individuo

    def asignar_jurados_y_asesor(self, curso_grupo):
        profesores_disponibles = Profesor.objects.filter(
            semestre_academico_profesores__semestre=curso_grupo.semestre,
            profesores_semestre_academico__semestre=curso_grupo.semestre
        ).distinct()

        jurado1 = random.choice(profesores_disponibles)
        profesores_disponibles = profesores_disponibles.exclude(id=jurado1.id)

        jurado2 = random.choice(profesores_disponibles)
        profesores_disponibles = profesores_disponibles.exclude(id=jurado2.id)

        asesor = random.choice(profesores_disponibles)
        
        return jurado1, jurado2, asesor

    def seleccionar_fecha_hora(self, jurado1, jurado2, asesor, curso):
        fechas_horas = []
        fechas_rango = Semana_Sustentacion.objects.filter(curso=curso).values('fecha_inicio', 'fecha_fin')

        for rango in fechas_rango:
            fechas = [rango['fecha_inicio'] + timedelta(days=i) for i in range((rango['fecha_fin'] - rango['fecha_inicio']).days + 1)]
            for fecha in fechas:
                horarios_jurado1 = self.obtener_horarios_disponibles(jurado1, fecha)
                horarios_jurado2 = self.obtener_horarios_disponibles(jurado2, fecha)
                horarios_asesor = self.obtener_horarios_disponibles(asesor, fecha)

                for h1 in horarios_jurado1:
                    for h2 in horarios_jurado2:
                        for ha in horarios_asesor:
                            hora_inicio, hora_fin = self.obtener_horas_comunes(h1, h2, ha)
                            if hora_inicio and hora_fin:
                                fechas_horas.append((fecha, hora_inicio, hora_fin))

        if fechas_horas:
            return random.choice(fechas_horas)
        else:
            return None, None, None

    def obtener_horarios_disponibles(self, profesor, fecha):
        return Profesores_Semestre_Academico.objects.filter(profesor=profesor, fecha=fecha)

    def obtener_horas_comunes(self, h1, h2, ha):
        hora_inicio = max(h1.hora_inicio, h2.hora_inicio, ha.hora_inicio)
        hora_fin = min(h1.hora_fin, h2.hora_fin, ha.hora_fin)
        if (datetime.combine(datetime.today(), hora_fin) - datetime.combine(datetime.today(), hora_inicio)).total_seconds() >= 1800:
            return hora_inicio, (datetime.combine(datetime.today(), hora_inicio) + self.duracion_sustentacion).time()
        return None, None

    def calcular_fitness(self, individuo):
        fitness = 0
        for sustentacion in individuo:
            if all(self.profesor_valido(sustentacion[key], sustentacion['cursos_grupos'].semestre) for key in ['jurado1', 'jurado2', 'asesor']):
                fitness += 1
        return fitness

    def profesor_valido(self, profesor, semestre):
        return (profesor and 
                Semestre_Academico_Profesores.objects.filter(profesor=profesor, semestre=semestre).exists() and 
                Profesores_Semestre_Academico.objects.filter(profesor=profesor, semestre=semestre).exists())

    def seleccionar_padres(self):
        return random.sample(self.poblacion, 2)

    def cruzar(self, padre1, padre2):
        punto_cruce = random.randint(1, len(padre1) - 1)
        hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
        hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
        return hijo1, hijo2

    def mutar(self, individuo):
        if random.random() < 0.1:
            sustentacion_mutada = random.choice(individuo)
            sustentacion_mutada['jurado1'] = self.seleccionar_profesor(sustentacion_mutada['cursos_grupos'], exclude=[sustentacion_mutada['jurado2'], sustentacion_mutada['asesor']])
            sustentacion_mutada['jurado2'] = self.seleccionar_profesor(sustentacion_mutada['cursos_grupos'], exclude=[sustentacion_mutada['jurado1'], sustentacion_mutada['asesor']])
            sustentacion_mutada['asesor'] = self.seleccionar_profesor(sustentacion_mutada['cursos_grupos'], exclude=[sustentacion_mutada['jurado1'], sustentacion_mutada['jurado2']])
        return individuo

    def evolucionar(self):
        nueva_poblacion = []
        while len(nueva_poblacion) < self.poblacion_size:
            padres = self.seleccionar_padres()
            hijo1, hijo2 = self.cruzar(padres[0], padres[1])
            nueva_poblacion.append(self.mutar(hijo1))
            nueva_poblacion.append(self.mutar(hijo2))
        self.poblacion = nueva_poblacion

    def verificar_disponibilidad(self, sustentacion):
        fecha = sustentacion['fecha']
        hora_inicio = sustentacion['hora_inicio']
        hora_fin = sustentacion['hora_fin']
        return (self.profesor_disponible(sustentacion['jurado1'], fecha, hora_inicio, hora_fin) and
                self.profesor_disponible(sustentacion['jurado2'], fecha, hora_inicio, hora_fin) and
                self.profesor_disponible(sustentacion['asesor'], fecha, hora_inicio, hora_fin))

    def profesor_disponible(self, profesor, fecha, hora_inicio, hora_fin):
        disponibilidad = Profesores_Semestre_Academico.objects.filter(profesor=profesor, fecha=fecha)
        for disp in disponibilidad:
            if disp.hora_inicio <= hora_inicio and disp.hora_fin >= hora_fin:
                return True
        return False

    def reprogramar_sustentacion(self, sustentacion, curso_grupo):
        jurado1, jurado2, asesor = sustentacion['jurado1'], sustentacion['jurado2'], sustentacion['asesor']
        fecha, hora_inicio, hora_fin = self.seleccionar_fecha_hora(jurado1, jurado2, asesor, curso_grupo.curso)
        if fecha and hora_inicio and hora_fin:
            sustentacion['fecha'] = fecha
            sustentacion['hora_inicio'] = hora_inicio
            sustentacion['hora_fin'] = hora_fin
        return sustentacion

    def ejecutar(self):
        for _ in range(self.generaciones):
            self.poblacion.sort(key=self.calcular_fitness, reverse=True)
            self.evolucionar()

        mejor_individuo = max(self.poblacion, key=self.calcular_fitness)

        # Verificar disponibilidad final y reprogramar si es necesario
        mejor_individuo = self.verificar_y_reprogramar(mejor_individuo)
        mejor_individuo = self.eliminar_duplicados(mejor_individuo)
        mejor_individuo = self.ordenar_por_curso_grupo(mejor_individuo)
        return mejor_individuo

    def verificar_y_reprogramar(self, mejor_individuo):
        for sustentacion in mejor_individuo:
            while not self.verificar_disponibilidad(sustentacion):
                curso_grupo = sustentacion['cursos_grupos']
                reprogramada = self.reprogramar_sustentacion(sustentacion, curso_grupo)
                if reprogramada['fecha'] and reprogramada['hora_inicio'] and reprogramada['hora_fin']:
                    sustentacion['fecha'] = reprogramada['fecha']
                    sustentacion['hora_inicio'] = reprogramada['hora_inicio']
                    sustentacion['hora_fin'] = reprogramada['hora_fin']
        return mejor_individuo

    def eliminar_duplicados(self, mejor_horario):
        seen = set()
        nuevo_horario = []
        for sustentacion in mejor_horario:
            key = (sustentacion['cursos_grupos'].id, sustentacion['estudiante'].id)
            if key not in seen:
                nuevo_horario.append(sustentacion)
                seen.add(key)
        return nuevo_horario

    def ordenar_por_curso_grupo(self, mejor_horario):
        return sorted(mejor_horario, key=lambda x: (x['cursos_grupos'].curso.nombre, x['cursos_grupos'].grupo.nombre))

def generar_horarios():
    cursos_grupos = Cursos_Grupos.objects.all()
    disponibilidad_profesores = {
        (disp.profesor.id, disp.semestre.id): disp
        for disp in Profesores_Semestre_Academico.objects.all()
    }
    fechas_sustentacion = Semana_Sustentacion.objects.all()
    ag = AlgoritmoGenetico(poblacion_size=10, generaciones=20, cursos_grupos=cursos_grupos, disponibilidad_profesores=disponibilidad_profesores, fechas_sustentacion=fechas_sustentacion)
    mejor_horario = ag.ejecutar()
    return mejor_horario

def guardar_horario(mejor_horario):
    for sustentacion in mejor_horario:
        nueva_sustentacion = Sustentacion.objects.create(
            cursos_grupos=sustentacion['cursos_grupos'],
            estudiante=sustentacion['estudiante'],
            jurado1=sustentacion['jurado1'],
            jurado2=sustentacion['jurado2'],
            asesor=sustentacion['asesor'],
            titulo=sustentacion['titulo']
        )
        Horario_Sustentaciones.objects.create(
            fecha=sustentacion['fecha'],
            hora_inicio=sustentacion['hora_inicio'],
            hora_fin=sustentacion['hora_fin'],
            sustentacion=nueva_sustentacion
        )