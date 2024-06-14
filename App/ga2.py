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
        poblacion = [self.crear_individuo() for _ in range(self.poblacion_size)]
        return poblacion

    def crear_individuo(self):
        individuo = []
        for curso_grupo in self.cursos_grupos:
            sustentaciones = Sustentacion.objects.filter(cursos_grupos=curso_grupo)
            for sustentacion in sustentaciones:
                if sustentacion.jurado1 and sustentacion.jurado2 and sustentacion.asesor:
                    fecha, hora_inicio, hora_fin = self.seleccionar_fecha_hora(individuo, sustentacion.jurado1, sustentacion.jurado2, sustentacion.asesor, curso_grupo.curso)
                    if fecha and hora_inicio and hora_fin:
                        if fecha not in self.fechas_sustentacion:
                            print(f"Error: Fecha {fecha} no está en las fechas de sustentación permitidas")
                            continue  # Saltar esta fecha si no está permitida
                        sust_data = {
                            'cursos_grupos': curso_grupo,
                            'estudiante': sustentacion.estudiante,
                            'jurado1': sustentacion.jurado1,
                            'jurado2': sustentacion.jurado2,
                            'asesor': sustentacion.asesor,  # Mantener el asesor de la sustentación original
                            'titulo': sustentacion.titulo,
                            'fecha': fecha,
                            'hora_inicio': hora_inicio,
                            'hora_fin': hora_fin
                        }
                        individuo.append(sust_data)
                else:
                    jurado1, jurado2 = self.asignar_jurados(sustentacion, curso_grupo)

                    fecha, hora_inicio, hora_fin = self.seleccionar_fecha_hora(individuo, jurado1, jurado2, sustentacion.asesor, curso_grupo.curso)

                    if fecha and hora_inicio and hora_fin:
                        if fecha not in self.fechas_sustentacion:
                            print(f"Error: Fecha {fecha} no está en las fechas de sustentación permitidas")
                            continue  # Saltar esta fecha si no está permitida
                        sust_data = {
                            'cursos_grupos': curso_grupo,
                            'estudiante': sustentacion.estudiante,
                            'jurado1': jurado1,
                            'jurado2': jurado2,
                            'asesor': sustentacion.asesor,  # Mantener el asesor de la sustentación original
                            'titulo': sustentacion.titulo,
                            'fecha': fecha,
                            'hora_inicio': hora_inicio,
                            'hora_fin': hora_fin
                        }
                        individuo.append(sust_data)
        return individuo
    def asignar_jurados(self, sustentacion, curso_grupo):
        profesores = Profesor.objects.filter(
            semestre_academico_profesores__semestre=curso_grupo.semestre,
            profesores_semestre_academico__semestre=curso_grupo.semestre
        ).distinct()

        profesores = profesores.exclude(id=sustentacion.asesor.id)  # Excluir al asesor de los posibles jurados

        jurado1 = sustentacion.jurado1 if sustentacion.jurado1 else random.choice(profesores)
        jurado2 = sustentacion.jurado2 if sustentacion.jurado2 else random.choice([p for p in profesores if p != jurado1])
        return jurado1, jurado2

    def asignar_profesor(self, curso_grupo, exclude=[]):
        profesores = Profesor.objects.filter(
            semestre_academico_profesores__semestre=curso_grupo.semestre,
            profesores_semestre_academico__semestre=curso_grupo.semestre
        ).distinct().exclude(id__in=[prof.id for prof in exclude])
        return random.choice(profesores)
    def evaluar_resultados(self, horario):
        todos_los_estudiantes = set(Sustentacion.objects.values_list('estudiante_id', flat=True))
        no_asignadas = []

        while True:
            conflictos = {}
            depurado = []

            for sustentacion in horario:
                fecha_hora = (sustentacion['fecha'], sustentacion['hora_inicio'])
                if fecha_hora not in conflictos:
                    conflictos[fecha_hora] = []
                conflictos[fecha_hora].append(sustentacion)

            conflictos_encontrados = False

            for key, sustentaciones in conflictos.items():
                if len(sustentaciones) > 1:
                    conflictos_encontrados = True
                    print(f"Conflicto encontrado en {key}:")
                    for sust in sustentaciones:
                        print(f"  Curso: {sust['cursos_grupos'].curso.nombre}, Grupo: {sust['cursos_grupos'].grupo.nombre}, Estudiante: {sust['estudiante']}")

                    # Mantener la primera sustentación y reasignar las demás
                    depurado.append(sustentaciones[0])
                    for sust in sustentaciones[1:]:
                        nueva_fecha, nueva_hora_inicio, nueva_hora_fin = None, None, None
                        intentos = 0
                        while not (nueva_fecha and nueva_hora_inicio and nueva_hora_fin) and intentos < 10:
                            nueva_fecha, nueva_hora_inicio, nueva_hora_fin = self.seleccionar_fecha_hora(depurado, sust['jurado1'], sust['jurado2'], sust['asesor'], sust['cursos_grupos'].curso)
                            intentos += 1
                            if not (nueva_fecha and nueva_hora_inicio and nueva_hora_fin):
                                print(f"Intento {intentos}: No se pudo encontrar nueva fecha y hora para la sustentación de {sust['estudiante']}")
                        
                        if nueva_fecha and nueva_hora_inicio and nueva_hora_fin:
                            sust['fecha'] = nueva_fecha
                            sust['hora_inicio'] = nueva_hora_inicio
                            sust['hora_fin'] = nueva_hora_fin
                            depurado.append(sust)
                        else:
                            print(f"No se pudo reasignar la sustentación de {sust['estudiante']} después de {intentos} intentos")
                            no_asignadas.append(sust)  # Añadir a la lista de no asignadas

                else:
                    depurado.append(sustentaciones[0])

            if not conflictos_encontrados:
                break
            else:
                horario = depurado

        # Añadir sustentaciones no asignadas a la lista no_asignadas
        asignados_estudiantes = set([sust['estudiante'].id for sust in depurado])
        no_asignados_estudiantes = todos_los_estudiantes - asignados_estudiantes

        for estudiante_id in no_asignados_estudiantes:
            sustentacion = Sustentacion.objects.get(estudiante_id=estudiante_id)
            no_asignadas.append({
                'cursos_grupos': sustentacion.cursos_grupos,
                'estudiante': sustentacion.estudiante,
                'jurado1': sustentacion.jurado1,
                'jurado2': sustentacion.jurado2,
                'asesor': sustentacion.asesor,
                'titulo': sustentacion.titulo,
                'fecha': "",
                'hora_inicio': "",
                'hora_fin': ""
            })

        return depurado, no_asignadas
   
    def seleccionar_fecha_hora(self, individuo, jurado1, jurado2, asesor, curso):
        semanas_sustentacion = Semana_Sustentacion.objects.filter(curso=curso, tipo_sustentacion='PARCIAL')  # Filtrar semanas de sustentación por curso

        for semana in semanas_sustentacion:
            rango_fechas = self.generar_rango_fechas(semana.fecha_inicio, semana.fecha_fin)
            for fecha in rango_fechas:
                if fecha not in self.fechas_sustentacion:
                    continue  # Saltar fechas no permitidas

                disponibilidad_jurado1 = self.disponibilidad_profesores.get((jurado1.id, fecha), [])
                disponibilidad_jurado2 = self.disponibilidad_profesores.get((jurado2.id, fecha), [])
                disponibilidad_asesor = self.disponibilidad_profesores.get((asesor.id, fecha), [])

                if disponibilidad_jurado1 and disponibilidad_jurado2 and disponibilidad_asesor:  # Verificar disponibilidad de todos los profesores
                    horarios_comunes = self.obtener_horas_comunes(disponibilidad_jurado1, disponibilidad_jurado2, disponibilidad_asesor, fecha)
                    if horarios_comunes:
                        for hora_inicio, hora_fin in horarios_comunes:
                            if not self.hay_conflicto_horario(individuo, fecha, hora_inicio):
                                return fecha, hora_inicio, hora_fin
                            # Intentar ajustar la hora en intervalos de 30 minutos adelante o atrás si hay conflicto
                            ajuste = timedelta(minutes=30)
                            for _ in range(4):  # Intentar hasta 2 horas (4 intervalos de 30 minutos)
                                nueva_hora_inicio_adelante = (datetime.combine(fecha, hora_inicio) + ajuste).time()
                                nueva_hora_fin_adelante = (datetime.combine(fecha, hora_fin) + ajuste).time()
                                if not self.hay_conflicto_horario(individuo, fecha, nueva_hora_inicio_adelante) and \
                                self.profesor_valido(jurado1, fecha, nueva_hora_inicio_adelante, nueva_hora_fin_adelante) and \
                                self.profesor_valido(jurado2, fecha, nueva_hora_inicio_adelante, nueva_hora_fin_adelante) and \
                                self.profesor_valido(asesor, fecha, nueva_hora_inicio_adelante, nueva_hora_fin_adelante):
                                    return fecha, nueva_hora_inicio_adelante, nueva_hora_fin_adelante
                                nueva_hora_inicio_atras = (datetime.combine(fecha, hora_inicio) - ajuste).time()
                                nueva_hora_fin_atras = (datetime.combine(fecha, hora_fin) - ajuste).time()
                                if not self.hay_conflicto_horario(individuo, fecha, nueva_hora_inicio_atras) and \
                                self.profesor_valido(jurado1, fecha, nueva_hora_inicio_atras, nueva_hora_fin_atras) and \
                                self.profesor_valido(jurado2, fecha, nueva_hora_inicio_atras, nueva_hora_fin_atras) and \
                                self.profesor_valido(asesor, fecha, nueva_hora_inicio_atras, nueva_hora_fin_atras):
                                    return fecha, nueva_hora_inicio_atras, nueva_hora_fin_atras
                                ajuste += timedelta(minutes=30)
        return None, None, None

    def hay_conflicto_horario(self, individuo, fecha, hora_inicio):
        for sustentacion in individuo:
            if sustentacion['fecha'] == fecha and sustentacion['hora_inicio'] == hora_inicio:
                return True
        return False
    def generar_rango_fechas(self, fecha_inicio, fecha_fin):
        delta = fecha_fin - fecha_inicio
        return [fecha_inicio + timedelta(days=i) for i in range(delta.days + 1)]

    def obtener_horas_comunes(self, disp1, disp2, disp3, fecha):
        horarios_comunes = []
        for d1 in disp1:
            for d2 in disp2:
                for d3 in disp3:
                    hora_inicio = max(d1.hora_inicio, d2.hora_inicio, d3.hora_inicio)
                    hora_fin = min(d1.hora_fin, d2.hora_fin, d3.hora_fin)
                    
                    # Convertir a datetime para comparar
                    datetime_inicio = datetime.combine(fecha, hora_inicio)
                    datetime_fin = datetime.combine(fecha, hora_fin)
                    
                    if (datetime_fin - datetime_inicio) >= self.duracion_sustentacion:
                        # Agregar intervalos de 30 minutos
                        current_time = datetime_inicio
                        while (current_time + self.duracion_sustentacion) <= datetime_fin:
                            fin = (current_time + self.duracion_sustentacion).time()
                            horarios_comunes.append((current_time.time(), fin))
                            current_time += self.duracion_sustentacion
        return horarios_comunes

    def calcular_fitness(self, individuo):
        fitness = 0
        for sustentacion in individuo:
            if self.profesor_valido(sustentacion['jurado1'], sustentacion['fecha'], sustentacion['hora_inicio'], sustentacion['hora_fin']) and \
               self.profesor_valido(sustentacion['jurado2'], sustentacion['fecha'], sustentacion['hora_inicio'], sustentacion['hora_fin']) and \
               self.profesor_valido(sustentacion['asesor'], sustentacion['fecha'], sustentacion['hora_inicio'], sustentacion['hora_fin']):
                fitness += 1
            else:
                # Penalizar si hay conflicto de horario
                fitness -= 1
        return fitness

    def profesor_valido(self, profesor, fecha, hora_inicio, hora_fin):
        disponibilidad = self.disponibilidad_profesores.get((profesor.id, fecha), [])
        for disp in disponibilidad:
            if disp.hora_inicio <= hora_inicio and disp.hora_fin >= hora_fin:
                return True
        return False

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
            # Verificar si ya hay tres jurados asignados
            if sustentacion_mutada['jurado1'] and sustentacion_mutada['jurado2'] and sustentacion_mutada['asesor']:
                # No hacer cambios si ya están asignados los tres jurados
                return individuo
            # Si no están asignados los tres jurados, entonces realizar la asignación
            sustentacion_mutada['jurado1'] = self.asignar_profesor(sustentacion_mutada['cursos_grupos'], exclude=[sustentacion_mutada['jurado2'], sustentacion_mutada['asesor']])
            sustentacion_mutada['jurado2'] = self.asignar_profesor(sustentacion_mutada['cursos_grupos'], exclude=[sustentacion_mutada['jurado1'], sustentacion_mutada['asesor']])
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
            self.poblacion.sort(key=self.calcular_fitness, reverse=True)
            self.evolucionar()
        mejor_individuo = max(self.poblacion, key=self.calcular_fitness)
        mejor_individuo = self.eliminar_duplicados(mejor_individuo)
        mejor_individuo = self.ordenar_por_curso_grupo(mejor_individuo)
        mejor_individuo, no_asignadas = self.evaluar_resultados(mejor_individuo)
        print(no_asignadas)
        # Añadir sustentaciones no asignadas al final con fecha y hora en blanco
        for sustentacion in no_asignadas:
            sustentacion['fecha'] = ""
            sustentacion['hora_inicio'] = ""
            sustentacion['hora_fin'] = ""
            mejor_individuo.append(sustentacion)

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
        (disp.profesor.id, disp.fecha): list(Profesores_Semestre_Academico.objects.filter(profesor=disp.profesor, fecha=disp.fecha))
        for disp in Profesores_Semestre_Academico.objects.all()
    }
    semanas_sustentacion = Semana_Sustentacion.objects.filter(tipo_sustentacion='PARCIAL')  # Filtrar solo las semanas de sustentación parciales

    # Obtener las fechas de sustentación de las semanas
    fechas_sustentacion = []
    for semana in semanas_sustentacion:
        rango_fechas = generar_rango_fechas(semana.fecha_inicio, semana.fecha_fin)
        fechas_sustentacion.extend(rango_fechas)

    print("Fechas de sustentación:")
    for fecha in fechas_sustentacion:
        print(fecha)

    ag = AlgoritmoGenetico(poblacion_size=10, generaciones=100, cursos_grupos=cursos_grupos, disponibilidad_profesores=disponibilidad_profesores, fechas_sustentacion=fechas_sustentacion)
    mejor_horario = ag.ejecutar()
    # print(mejor_horario)
    return mejor_horario

def generar_rango_fechas(fecha_inicio, fecha_fin):
    delta = fecha_fin - fecha_inicio
    return [fecha_inicio + timedelta(days=i) for i in range(delta.days + 1)]

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