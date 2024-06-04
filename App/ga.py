import random
from datetime import datetime, timedelta, time
from django.db import models
from .models import *

# Algoritmo genético
class AlgoritmoGenetico:
    def __init__(self, poblacion_size, generaciones, cursos_grupos, disponibilidad_profesores, fechas_sustentacion):
        self.poblacion_size = poblacion_size
        self.generaciones = generaciones
        self.cursos_grupos = cursos_grupos
        self.disponibilidad_profesores = disponibilidad_profesores
        self.fechas_sustentacion = fechas_sustentacion
        self.poblacion = self.inicializar_poblacion()

    def inicializar_poblacion(self):
        print("Inicializando población...")
        poblacion = []
        for _ in range(self.poblacion_size):
            individuo = self.crear_individuo()
            poblacion.append(individuo)
        print(f"Población inicial: {poblacion}")
        return poblacion

    def crear_individuo(self):
        individuo = []
        estudiantes_asignados = set()
        for curso_grupo in self.cursos_grupos:
            sustentaciones = Sustentacion.objects.filter(cursos_grupos=curso_grupo)
            for sustentacion in sustentaciones:
                if sustentacion.estudiante.id in estudiantes_asignados:
                    continue
                estudiantes_asignados.add(sustentacion.estudiante.id)

                jurado1 = sustentacion.jurado1 if sustentacion.jurado1 and self.profesor_valido(sustentacion.jurado1, curso_grupo.semestre) else self.seleccionar_profesor(curso_grupo, exclude=[])
                jurado2 = sustentacion.jurado2 if sustentacion.jurado2 and self.profesor_valido(sustentacion.jurado2, curso_grupo.semestre) else self.seleccionar_profesor(curso_grupo, exclude=[jurado1])
                asesor = sustentacion.asesor if self.profesor_valido(sustentacion.asesor, curso_grupo.semestre) else self.seleccionar_profesor(curso_grupo, exclude=[jurado1, jurado2])

                # Asegurarse de que los tres profesores sean distintos
                if jurado1 == jurado2:
                    jurado2 = self.seleccionar_profesor(curso_grupo, exclude=[jurado1])
                if jurado1 == asesor or jurado2 == asesor:
                    asesor = self.seleccionar_profesor(curso_grupo, exclude=[jurado1, jurado2])

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

    def profesor_valido(self, profesor, semestre):
        return Semestre_Academico_Profesores.objects.filter(profesor=profesor, semestre=semestre).exists() and Profesores_Semestre_Academico.objects.filter(profesor=profesor, semestre=semestre).exists()

    def seleccionar_estudiante(self, curso_grupo):
        estudiantes = Estudiante.objects.filter(sustentacion__cursos_grupos=curso_grupo)
        return random.choice(estudiantes)

    def seleccionar_profesor(self, curso_grupo, exclude=[]):
        profesores = Profesor.objects.filter(
            semestre_academico_profesores__semestre=curso_grupo.semestre,
            profesores_semestre_academico__semestre=curso_grupo.semestre,
            id__in=Semestre_Academico_Profesores.objects.filter(semestre=curso_grupo.semestre).values_list('profesor_id', flat=True)
        ).exclude(id__in=[profesor.id for profesor in exclude if profesor]).distinct()
        return random.choice(profesores) if profesores.exists() else None

    def seleccionar_fecha_hora(self, jurado1, jurado2, asesor, curso):
        fechas_horas = []
        fechas_rango = Semana_Sustentacion.objects.filter(curso=curso).values('fecha_inicio', 'fecha_fin')

        for rango in fechas_rango:
            fechas = [rango['fecha_inicio'] + timedelta(days=i) for i in range((rango['fecha_fin'] - rango['fecha_inicio']).days + 1)]
            for fecha in fechas:
                horarios_jurado1 = Profesores_Semestre_Academico.objects.filter(profesor=jurado1, fecha=fecha)
                horarios_jurado2 = Profesores_Semestre_Academico.objects.filter(profesor=jurado2, fecha=fecha)
                horarios_asesor = Profesores_Semestre_Academico.objects.filter(profesor=asesor, fecha=fecha)

                for h1 in horarios_jurado1:
                    for h2 in horarios_jurado2:
                        for ha in horarios_asesor:
                            if h1.hora_inicio <= h2.hora_inicio <= h1.hora_fin and h1.hora_inicio <= ha.hora_inicio <= h1.hora_fin:
                                hora_inicio = max(h1.hora_inicio, h2.hora_inicio, ha.hora_inicio)
                                hora_fin = min(h1.hora_fin, h2.hora_fin, ha.hora_fin)
                                if (datetime.combine(datetime.today(), hora_fin) - datetime.combine(datetime.today(), hora_inicio)).total_seconds() >= 1800:
                                    fechas_horas.append((fecha, hora_inicio, (datetime.combine(datetime.today(), hora_inicio) + timedelta(minutes=30)).time()))

        if fechas_horas:
            return random.choice(fechas_horas)
        else:
            return self.buscar_nueva_disponibilidad(jurado1, jurado2, asesor, curso)

    def buscar_nueva_disponibilidad(self, jurado1, jurado2, asesor, curso):
        fechas_rango = Semana_Sustentacion.objects.filter(curso=curso).values('fecha_inicio', 'fecha_fin')

        for rango in fechas_rango:
            fechas = [rango['fecha_inicio'] + timedelta(days=i) for i in range((rango['fecha_fin'] - rango['fecha_inicio']).days + 1)]
            for fecha in fechas:
                horarios_jurado1 = Profesores_Semestre_Academico.objects.filter(profesor=jurado1, fecha=fecha)
                horarios_jurado2 = Profesores_Semestre_Academico.objects.filter(profesor=jurado2, fecha=fecha)
                horarios_asesor = Profesores_Semestre_Academico.objects.filter(profesor=asesor, fecha=fecha)

                for h1 in horarios_jurado1:
                    for h2 in horarios_jurado2:
                        for ha in horarios_asesor:
                            hora_inicio = max(h1.hora_inicio, h2.hora_inicio, ha.hora_inicio)
                            hora_fin = min(h1.hora_fin, h2.hora_fin, ha.hora_fin)
                            if (datetime.combine(datetime.today(), hora_fin) - datetime.combine(datetime.today(), hora_inicio)).total_seconds() >= 1800:
                                return fecha, hora_inicio, (datetime.combine(datetime.today(), hora_inicio) + timedelta(minutes=30)).time()

        return None, None, None

    def verificar_conflictos_horarios(self, mejor_horario):
        for i, sustentacion in enumerate(mejor_horario):
            for j, otra_sustentacion in enumerate(mejor_horario):
                if i == j:
                    continue
                if sustentacion['fecha'] == otra_sustentacion['fecha'] and (
                    sustentacion['jurado1'] in [otra_sustentacion['jurado1'], otra_sustentacion['jurado2'], otra_sustentacion['asesor']] or
                    sustentacion['jurado2'] in [otra_sustentacion['jurado1'], otra_sustentacion['jurado2'], otra_sustentacion['asesor']] or
                    sustentacion['asesor'] in [otra_sustentacion['jurado1'], otra_sustentacion['jurado2'], otra_sustentacion['asesor']]
                ):
                    if (sustentacion['hora_inicio'] <= otra_sustentacion['hora_inicio'] < sustentacion['hora_fin']) or (
                        otra_sustentacion['hora_inicio'] <= sustentacion['hora_inicio'] < otra_sustentacion['hora_fin']
                    ):
                        # Si hay conflicto, mover la segunda sustentación 30 minutos adelante
                        nueva_hora_inicio = (datetime.combine(datetime.today(), otra_sustentacion['hora_inicio']) + timedelta(minutes=30)).time()
                        nueva_hora_fin = (datetime.combine(datetime.today(), otra_sustentacion['hora_fin']) + timedelta(minutes=30)).time()
                        
                        otra_sustentacion['hora_inicio'] = nueva_hora_inicio
                        otra_sustentacion['hora_fin'] = nueva_hora_fin

                        # Recalcular la disponibilidad para la nueva hora
                        otra_sustentacion['hora_inicio'], otra_sustentacion['hora_fin'] = self.ajustar_hora_disponibilidad(otra_sustentacion, mejor_horario)

        return mejor_horario

    def ajustar_hora_disponibilidad(self, sustentacion, mejor_horario):
        while True:
            conflicto = False
            for otra_sustentacion in mejor_horario:
                if sustentacion == otra_sustentacion:
                    continue
                if sustentacion['fecha'] == otra_sustentacion['fecha'] and (
                    sustentacion['jurado1'] in [otra_sustentacion['jurado1'], otra_sustentacion['jurado2'], otra_sustentacion['asesor']] or
                    sustentacion['jurado2'] in [otra_sustentacion['jurado1'], otra_sustentacion['jurado2'], otra_sustentacion['asesor']] or
                    sustentacion['asesor'] in [otra_sustentacion['jurado1'], otra_sustentacion['jurado2'], otra_sustentacion['asesor']]
                ):
                    if (sustentacion['hora_inicio'] <= otra_sustentacion['hora_inicio'] < sustentacion['hora_fin']) or (
                        otra_sustentacion['hora_inicio'] <= sustentacion['hora_inicio'] < otra_sustentacion['hora_fin']
                    ):
                        conflicto = True
                        sustentacion['hora_inicio'] = (datetime.combine(datetime.today(), sustentacion['hora_inicio']) + timedelta(minutes=30)).time()
                        sustentacion['hora_fin'] = (datetime.combine(datetime.today(), sustentacion['hora_fin']) + timedelta(minutes=30)).time()
                        break
            if not conflicto:
                break

        return sustentacion['hora_inicio'], sustentacion['hora_fin']

    def calcular_fitness(self, individuo):
        fitness = 0
        for sustentacion in individuo:
            disponibilidad_jurado1 = self.disponibilidad_profesores.get((sustentacion['jurado1'].id, sustentacion['cursos_grupos'].semestre.id)) if sustentacion['jurado1'] else None
            disponibilidad_jurado2 = self.disponibilidad_profesores.get((sustentacion['jurado2'].id, sustentacion['cursos_grupos'].semestre.id)) if sustentacion['jurado2'] else None
            disponibilidad_asesor = self.disponibilidad_profesores.get((sustentacion['asesor'].id, sustentacion['cursos_grupos'].semestre.id))

            if disponibilidad_jurado1 and disponibilidad_jurado2 and disponibilidad_asesor:
                fitness += 1
        return fitness

    def verificar_disponibilidad(self, mejor_horario):
        no_disponibles = []
        for sustentacion in mejor_horario:
            jurado1_disp = Profesores_Semestre_Academico.objects.filter(profesor=sustentacion['jurado1'], semestre=sustentacion['cursos_grupos'].semestre)
            jurado2_disp = Profesores_Semestre_Academico.objects.filter(profesor=sustentacion['jurado2'], semestre=sustentacion['cursos_grupos'].semestre)
            asesor_disp = Profesores_Semestre_Academico.objects.filter(profesor=sustentacion['asesor'], semestre=sustentacion['cursos_grupos'].semestre)

            if not Semestre_Academico_Profesores.objects.filter(profesor=sustentacion['jurado1'], semestre=sustentacion['cursos_grupos'].semestre).exists() and not jurado1_disp.exists():
                no_disponibles.append(sustentacion['jurado1'].apellidos_nombres)

            if not Semestre_Academico_Profesores.objects.filter(profesor=sustentacion['jurado2'], semestre=sustentacion['cursos_grupos'].semestre).exists() and not jurado2_disp.exists():
                no_disponibles.append(sustentacion['jurado2'].apellidos_nombres)

            if not Semestre_Academico_Profesores.objects.filter(profesor=sustentacion['asesor'], semestre=sustentacion['cursos_grupos'].semestre).exists() or not asesor_disp.exists():
                no_disponibles.append(sustentacion['asesor'].apellidos_nombres)

        # Eliminar profesores no disponibles del horario
        for profesor in no_disponibles:
            mejor_horario = [sustentacion for sustentacion in mejor_horario if sustentacion['jurado1'].apellidos_nombres != profesor and sustentacion['jurado2'].apellidos_nombres != profesor and sustentacion['asesor'].apellidos_nombres != profesor]

        return mejor_horario, list(set(no_disponibles))

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
                sustentacion_mutada['jurado1'] = self.seleccionar_profesor(sustentacion_mutada['cursos_grupos'], exclude=[sustentacion_mutada['jurado2'], sustentacion_mutada['asesor']])
            if not sustentacion_mutada['jurado2']:
                sustentacion_mutada['jurado2'] = self.seleccionar_profesor(sustentacion_mutada['cursos_grupos'], exclude=[sustentacion_mutada['jurado1'], sustentacion_mutada['asesor']])
            if not sustentacion_mutada['asesor']:
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

    def ejecutar(self):
        for _ in range(self.generaciones):
            self.poblacion = sorted(self.poblacion, key=lambda ind: self.calcular_fitness(ind), reverse=True)
            self.evolucionar()
        mejor_individuo = max(self.poblacion, key=lambda ind: self.calcular_fitness(ind))
        mejor_individuo, no_disponibles = self.verificar_disponibilidad(mejor_individuo)
        mejor_individuo = self.verificar_conflictos_horarios(mejor_individuo)
        mejor_individuo = self.eliminar_duplicados(mejor_individuo)
        mejor_individuo = self.garantizar_todas_sustentaciones(mejor_individuo)
        return mejor_individuo, no_disponibles

    def eliminar_duplicados(self, mejor_horario):
        seen = set()
        nuevo_horario = []
        for sustentacion in mejor_horario:
            key = (sustentacion['cursos_grupos'].id, sustentacion['estudiante'].id)
            if key not in seen:
                nuevo_horario.append(sustentacion)
                seen.add(key)
        return nuevo_horario

    def garantizar_todas_sustentaciones(self, mejor_horario):
        asignadas = {(sustentacion['cursos_grupos'].id, sustentacion['estudiante'].id) for sustentacion in mejor_horario}
        todas_sustentaciones = {(s.cursos_grupos.id, s.estudiante.id): s for s in Sustentacion.objects.all()}

        for key, sustentacion in todas_sustentaciones.items():
            if key not in asignadas:
                jurado1 = sustentacion.jurado1 if sustentacion.jurado1 and self.profesor_valido(sustentacion.jurado1, sustentacion.cursos_grupos.semestre) else self.seleccionar_profesor(sustentacion.cursos_grupos, exclude=[])
                jurado2 = sustentacion.jurado2 if sustentacion.jurado2 and self.profesor_valido(sustentacion.jurado2, sustentacion.cursos_grupos.semestre) else self.seleccionar_profesor(sustentacion.cursos_grupos, exclude=[jurado1])
                asesor = sustentacion.asesor if self.profesor_valido(sustentacion.asesor, sustentacion.cursos_grupos.semestre) else self.seleccionar_profesor(sustentacion.cursos_grupos, exclude=[jurado1, jurado2])

                # Asegurarse de que los tres profesores sean distintos
                if jurado1 == jurado2:
                    jurado2 = self.seleccionar_profesor(sustentacion.cursos_grupos, exclude=[jurado1])
                if jurado1 == asesor or jurado2 == asesor:
                    asesor = self.seleccionar_profesor(sustentacion.cursos_grupos, exclude=[jurado1, jurado2])

                fecha, hora_inicio, hora_fin = self.seleccionar_fecha_hora(jurado1, jurado2, asesor, sustentacion.cursos_grupos.curso)

                if fecha and hora_inicio and hora_fin:
                    sust_data = {
                        'cursos_grupos': sustentacion.cursos_grupos,
                        'estudiante': sustentacion.estudiante,
                        'jurado1': jurado1,
                        'jurado2': jurado2,
                        'asesor': asesor,
                        'titulo': sustentacion.titulo,
                        'fecha': fecha,
                        'hora_inicio': hora_inicio,
                        'hora_fin': hora_fin
                    }
                    mejor_horario.append(sust_data)

        return mejor_horario

def generar_horarios():
    cursos_grupos = Cursos_Grupos.objects.all()
    disponibilidad_profesores = {
        (disp.profesor.id, disp.semestre.id): disp
        for disp in Profesores_Semestre_Academico.objects.all()
    }
    fechas_sustentacion = Semana_Sustentacion.objects.all()
    ag = AlgoritmoGenetico(poblacion_size=10, generaciones=50, cursos_grupos=cursos_grupos, disponibilidad_profesores=disponibilidad_profesores, fechas_sustentacion=fechas_sustentacion)
    mejor_horario, no_disponibles = ag.ejecutar()
    return mejor_horario, no_disponibles

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
