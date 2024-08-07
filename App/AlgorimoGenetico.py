import random
from datetime import datetime, timedelta
from django.db import models
from .models import *
from django.db import transaction

class AlgoritmoGenetico:
    def __init__(self, poblacion_size, generaciones, cursos_grupos, disponibilidad_profesores, fechas_sustentacion, tipo_sustentacion, duracion_sustentacion):
        self.poblacion_size = poblacion_size
        self.generaciones = generaciones
        self.cursos_grupos = cursos_grupos
        self.disponibilidad_profesores = disponibilidad_profesores
        self.fechas_sustentacion = fechas_sustentacion
        self.tipo_sustentacion = tipo_sustentacion
        self.duracion_sustentacion = duracion_sustentacion  # Usar la duración obtenida
        self.poblacion = self.inicializar_poblacion()
        
    def inicializar_poblacion(self):
        poblacion = [self.crear_individuo() for _ in range(self.poblacion_size)]
        return poblacion

    def crear_individuo(self):
        individuo = []
        semestre_vigente = SemestreAcademico.objects.filter(vigencia=True).first()
        if not semestre_vigente:
            print("No hay semestre vigente.")
            return individuo
        
        cursos_grupos_vigentes = Cursos_Grupos.objects.filter(semestre=semestre_vigente)
        for curso_grupo in cursos_grupos_vigentes:
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
                            'asesor': sustentacion.asesor,
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
                            'asesor': sustentacion.asesor,
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
        print(profesores,  sustentacion)
        if not profesores.exists():
            return
        else:
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

                else:
                    depurado.append(sustentaciones[0])

            if not conflictos_encontrados:
                break
            else:
                horario = depurado

        return depurado
    
    def validar_disponibilidad_total(self, fecha, hora_inicio, hora_fin, jurado1, jurado2, asesor):
        disponibilidad_jurado1 = self.disponibilidad_profesores.get((jurado1.id, fecha), [])
        disponibilidad_jurado2 = self.disponibilidad_profesores.get((jurado2.id, fecha), [])
        disponibilidad_asesor = self.disponibilidad_profesores.get((asesor.id, fecha), [])

        for disp1 in disponibilidad_jurado1:
            for disp2 in disponibilidad_jurado2:
                for disp3 in disponibilidad_asesor:
                    if (disp1.hora_inicio <= hora_inicio < disp1.hora_fin) and \
                    (disp2.hora_inicio <= hora_inicio < disp2.hora_fin) and \
                    (disp3.hora_inicio <= hora_inicio < disp3.hora_fin):
                        return True
        return False
    def seleccionar_fecha_hora(self, individuo, jurado1, jurado2, asesor, curso):
        semestre_vigente = SemestreAcademico.objects.filter(vigencia=True).first()

        semanas_sustentacion = Semana_Sustentacion.objects.filter(curso=curso, tipo_sustentacion=self.tipo_sustentacion, semestre_academico=semestre_vigente)

        for semana in semanas_sustentacion:
            rango_fechas = self.generar_rango_fechas(semana.fecha_inicio, semana.fecha_fin)
            for fecha in rango_fechas:
                if fecha not in self.fechas_sustentacion:
                    continue  # Saltar fechas no permitidas

                disponibilidad_jurado1 = self.disponibilidad_profesores.get((jurado1.id, fecha), [])
                disponibilidad_jurado2 = self.disponibilidad_profesores.get((jurado2.id, fecha), [])
                disponibilidad_asesor = self.disponibilidad_profesores.get((asesor.id, fecha), [])

                if disponibilidad_jurado1 and disponibilidad_jurado2 and disponibilidad_asesor:
                    horarios_comunes = self.obtener_horas_comunes(disponibilidad_jurado1, disponibilidad_jurado2, disponibilidad_asesor, fecha)
                    if horarios_comunes:
                        for hora_inicio, hora_fin in horarios_comunes:
                            if not self.hay_conflicto_horario(individuo, fecha, hora_inicio) and self.validar_disponibilidad_total(fecha, hora_inicio, hora_fin, jurado1, jurado2, asesor):
                                return fecha, hora_inicio, hora_fin
                            ajuste = self.duracion_sustentacion
                            for _ in range(4):
                                nueva_hora_inicio_adelante = (datetime.combine(fecha, hora_inicio) + ajuste).time()
                                nueva_hora_fin_adelante = (datetime.combine(fecha, hora_fin) + ajuste).time()
                                if not self.hay_conflicto_horario(individuo, fecha, nueva_hora_inicio_adelante) and self.validar_disponibilidad_total(fecha, nueva_hora_inicio_adelante, nueva_hora_fin_adelante, jurado1, jurado2, asesor):
                                    return fecha, nueva_hora_inicio_adelante, nueva_hora_fin_adelante
                                nueva_hora_inicio_atras = (datetime.combine(fecha, hora_inicio) - ajuste).time()
                                nueva_hora_fin_atras = (datetime.combine(fecha, hora_fin) - ajuste).time()
                                if not self.hay_conflicto_horario(individuo, fecha, nueva_hora_inicio_atras) and self.validar_disponibilidad_total(fecha, nueva_hora_inicio_atras, nueva_hora_fin_atras, jurado1, jurado2, asesor):
                                    return fecha, nueva_hora_inicio_atras, nueva_hora_fin_atras
                                ajuste += self.duracion_sustentacion
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
                        # Agregar intervalos de duracion_sustentacion
                        current_time = datetime_inicio
                        while (current_time + self.duracion_sustentacion) <= datetime_fin:
                            fin = (current_time + self.duracion_sustentacion).time()
                            horarios_comunes.append((current_time.time(), fin))
                            current_time += self.duracion_sustentacion
        return horarios_comunes
    def profesor_valido(self, profesor, fecha, hora_inicio, hora_fin):
        disponibilidad = self.disponibilidad_profesores.get((profesor.id, fecha), [])
        for disp in disponibilidad:
            if disp.hora_inicio <= hora_inicio and disp.hora_fin >= hora_fin:
                return True
        return False

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
        mejor_individuo = self.evaluar_resultados(mejor_individuo)
        
        
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


    def obtener_sustentaciones_no_incluidas(self, mejor_horario):
        semestre_vigente = SemestreAcademico.objects.filter(vigencia=True).first()
        if not semestre_vigente:
            print("No hay semestre vigente.")
            return Sustentacion.objects.none()  # Devolver un queryset vacío si no hay semestre vigente

        ids_incluidos = {(sust['cursos_grupos'].id, sust['estudiante'].id) for sust in mejor_horario}
        
        sustentaciones_no_incluidas = Sustentacion.objects.filter(
            cursos_grupos__semestre=semestre_vigente
        ).exclude(
            models.Q(cursos_grupos_id__in=[sust['cursos_grupos'].id for sust in mejor_horario]) &
            models.Q(estudiante_id__in=[sust['estudiante'].id for sust in mejor_horario])
        )
        return sustentaciones_no_incluidas


    def asignar_horario_y_jurados(self, mejor_horario, sustentacion):
        # Asignar jurados si no están asignados
        jurado1, jurado2 = self.asignar_jurados(sustentacion, sustentacion.cursos_grupos)
        
        # Convertir jurado1, jurado2, y asesor a objetos Profesor si son cadenas
        try:
            if isinstance(jurado1, str):
                jurado1 = Profesor.objects.get(apellidos_nombres=jurado1)
            if isinstance(jurado2, str):
                jurado2 = Profesor.objects.get(apellidos_nombres=jurado2)
            if isinstance(sustentacion.asesor, str):
                asesor = Profesor.objects.get(apellidos_nombres=sustentacion.asesor)
            else:
                asesor = sustentacion.asesor
        except Profesor.DoesNotExist as e:
            print(f"Error: {str(e)} - Profesor no encontrado. Sustentación: {sustentacion}")
            return None  # Saltar esta sustentación si no se encuentra el profesor

        # Seleccionar fecha y hora para la sustentación
        fecha, hora_inicio, hora_fin = self.seleccionar_fecha_hora(mejor_horario, jurado1, jurado2, asesor, sustentacion.cursos_grupos.curso)

        # Verificar si se encontró una fecha y hora válida
        if fecha and hora_inicio and hora_fin:
            return {
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
        return None



    def agregar_sustentaciones_no_incluidas(self, mejor_horario):
        sustentaciones_no_incluidas = self.obtener_sustentaciones_no_incluidas(mejor_horario)
        for sustentacion in sustentaciones_no_incluidas:
            sust_data = self.asignar_horario_y_jurados(mejor_horario, sustentacion)
            if sust_data:
                mejor_horario.append(sust_data)
            else:
                # Si no se pudo asignar horario, agregar con jurados y horarios en blanco o los que ya tiene asignados
                sust_data = {
                    'cursos_grupos': sustentacion.cursos_grupos,
                    'estudiante': sustentacion.estudiante,
                    'jurado1': sustentacion.jurado1 if sustentacion.jurado1 else "",
                    'jurado2': sustentacion.jurado2 if sustentacion.jurado2 else "",
                    'asesor': sustentacion.asesor,
                    'titulo': sustentacion.titulo,
                    'fecha': "",
                    'hora_inicio': "",
                    'hora_fin': ""
                }
                mejor_horario.append(sust_data)
        # Nueva validación para asignar horarios a las sustentaciones con "Fecha Inválida"
        mejor_horario = self.asignar_horarios_a_sustentaciones_invalidas(mejor_horario)
        return mejor_horario

    def asignar_horarios_a_sustentaciones_invalidas(self, mejor_horario):
        sustentaciones_invalidas = [s for s in mejor_horario if not s['fecha'] or s['fecha'] == 'Fecha Inválida']
        for sust in sustentaciones_invalidas:
            # Convertir jurado1, jurado2, y asesor a objetos Profesor si son cadenas
            try:
                if isinstance(sust['jurado1'], str):
                    sust['jurado1'] = Profesor.objects.get(apellidos_nombres=sust['jurado1'])
                if isinstance(sust['jurado2'], str):
                    sust['jurado2'] = Profesor.objects.get(apellidos_nombres=sust['jurado2'])
                if isinstance(sust['asesor'], str):
                    sust['asesor'] = Profesor.objects.get(apellidos_nombres=sust['asesor'])
            except Profesor.DoesNotExist as e:
                print(f"Error: {str(e)} - Profesor no encontrado. Sustentación: {sust}")
                continue  # Saltar esta sustentación si no se encuentra el profesor

            reintentos = 0
            while reintentos < 10:
                fecha, hora_inicio, hora_fin = self.seleccionar_fecha_hora_sin_repetir_jurados(mejor_horario, sust['jurado1'], sust['jurado2'], sust['asesor'], sust['cursos_grupos'].curso)
                if fecha and hora_inicio and hora_fin:
                    sust['fecha'] = fecha
                    sust['hora_inicio'] = hora_inicio
                    sust['hora_fin'] = hora_fin
                    break
                reintentos += 1
        return mejor_horario



    def seleccionar_fecha_hora_sin_repetir_jurados(self, individuo, jurado1, jurado2, asesor, curso):
        semestre_vigente = SemestreAcademico.objects.filter(vigencia=True).first()

        semanas_sustentacion = Semana_Sustentacion.objects.filter(curso=curso, tipo_sustentacion=self.tipo_sustentacion, semestre_academico=semestre_vigente)

        for semana in semanas_sustentacion:
            rango_fechas = self.generar_rango_fechas(semana.fecha_inicio, semana.fecha_fin)
            for fecha in rango_fechas:
                if fecha not in self.fechas_sustentacion:
                    continue  # Saltar fechas no permitidas

                disponibilidad_jurado1 = self.disponibilidad_profesores.get((jurado1.id, fecha), [])
                disponibilidad_jurado2 = self.disponibilidad_profesores.get((jurado2.id, fecha), [])
                disponibilidad_asesor = self.disponibilidad_profesores.get((asesor.id, fecha), [])

                if disponibilidad_jurado1 and disponibilidad_jurado2 and disponibilidad_asesor:
                    horarios_comunes = self.obtener_horas_comunes(disponibilidad_jurado1, disponibilidad_jurado2, disponibilidad_asesor, fecha)
                    if horarios_comunes:
                        for hora_inicio, hora_fin in horarios_comunes:
                            if not self.hay_conflicto_horario_con_diferentes_jurados(individuo, fecha, hora_inicio, jurado1, jurado2, asesor) and self.validar_disponibilidad_total(fecha, hora_inicio, hora_fin, jurado1, jurado2, asesor):
                                return fecha, hora_inicio, hora_fin
                            ajuste = self.duracion_sustentacion
                            for _ in range(4):
                                nueva_hora_inicio_adelante = (datetime.combine(fecha, hora_inicio) + ajuste).time()
                                nueva_hora_fin_adelante = (datetime.combine(fecha, hora_fin) + ajuste).time()
                                if not self.hay_conflicto_horario_con_diferentes_jurados(individuo, fecha, nueva_hora_inicio_adelante, jurado1, jurado2, asesor) and self.validar_disponibilidad_total(fecha, nueva_hora_inicio_adelante, nueva_hora_fin_adelante, jurado1, jurado2, asesor):
                                    return fecha, nueva_hora_inicio_adelante, nueva_hora_fin_adelante
                                nueva_hora_inicio_atras = (datetime.combine(fecha, hora_inicio) - ajuste).time()
                                nueva_hora_fin_atras = (datetime.combine(fecha, hora_fin) - ajuste).time()
                                if not self.hay_conflicto_horario_con_diferentes_jurados(individuo, fecha, nueva_hora_inicio_atras, jurado1, jurado2, asesor) and self.validar_disponibilidad_total(fecha, nueva_hora_inicio_atras, nueva_hora_fin_atras, jurado1, jurado2, asesor):
                                    return fecha, nueva_hora_inicio_atras, nueva_hora_fin_atras
                                ajuste += self.duracion_sustentacion
        return None, None, None

    def hay_conflicto_horario_con_diferentes_jurados(self, individuo, fecha, hora_inicio, jurado1, jurado2, asesor):
        for sustentacion in individuo:
            if sustentacion['fecha'] == fecha and sustentacion['hora_inicio'] == hora_inicio:
                if sustentacion['jurado1'] == jurado1 or sustentacion['jurado1'] == jurado2 or sustentacion['jurado1'] == asesor or \
                sustentacion['jurado2'] == jurado1 or sustentacion['jurado2'] == jurado2 or sustentacion['jurado2'] == asesor or \
                sustentacion['asesor'] == jurado1 or sustentacion['asesor'] == jurado2 or sustentacion['asesor'] == asesor:
                    return True
        return False
def generar_horarios(tipo_sustentacion):
    try:
        semestre_vigente = SemestreAcademico.objects.filter(vigencia=True).first()
        cursos_grupos = Cursos_Grupos.objects.filter(semestre=semestre_vigente)
        disponibilidad_profesores = {
            (disp.profesor.id, disp.fecha): list(Profesores_Semestre_Academico.objects.filter(profesor=disp.profesor, fecha=disp.fecha, semestre=semestre_vigente))
            for disp in Profesores_Semestre_Academico.objects.filter(semestre=semestre_vigente)
        }

        semanas_sustentacion = Semana_Sustentacion.objects.filter(tipo_sustentacion=tipo_sustentacion, semestre_academico=semestre_vigente)  # Filtrar solo las semanas de sustentación según tipo

        # Obtener las fechas de sustentación de las semanas
        fechas_sustentacion = []
        duracion_sustentacion = None
        for semana in semanas_sustentacion:
            rango_fechas = generar_rango_fechas(semana.fecha_inicio, semana.fecha_fin)
            fechas_sustentacion.extend(rango_fechas)
            if not duracion_sustentacion:
                duracion_sustentacion = timedelta(minutes=semana.duracion_sustentacion)
                
        # Generar 3 horarios y comparar los resultados
        mejores_horarios = []
        for _ in range(3):
            ag = AlgoritmoGenetico(poblacion_size=2, generaciones=1, cursos_grupos=cursos_grupos, disponibilidad_profesores=disponibilidad_profesores, fechas_sustentacion=fechas_sustentacion, tipo_sustentacion=tipo_sustentacion, duracion_sustentacion=duracion_sustentacion)
            mejor_horario = ag.ejecutar()
            mejores_horarios.append(mejor_horario)

        # Seleccionar el horario más extenso
        mejor_horario = max(mejores_horarios, key=len)

        # Agregar sustentaciones no incluidas
        ag = AlgoritmoGenetico(poblacion_size=2, generaciones=1, cursos_grupos=cursos_grupos, disponibilidad_profesores=disponibilidad_profesores, fechas_sustentacion=fechas_sustentacion, tipo_sustentacion=tipo_sustentacion, duracion_sustentacion=duracion_sustentacion)
        mejor_horario = ag.agregar_sustentaciones_no_incluidas(mejor_horario)

        return mejor_horario
    except Exception as e:
        print(f"Error en generar_horarios: {e}")
        raise

def generar_rango_fechas(fecha_inicio, fecha_fin):
    delta = fecha_fin - fecha_inicio
    return [fecha_inicio + timedelta(days=i) for i in range(delta.days + 1)]
def guardar_horario(mejor_horario):
    try:
        with transaction.atomic():
            semestre_vigente = SemestreAcademico.objects.filter(vigencia=True).first()
            if not semestre_vigente:
                raise RuntimeError("No hay semestre vigente.")

            for sustentacion_data in mejor_horario:
                try:
                    cursos_grupos = sustentacion_data['cursos_grupos']
                    curso = cursos_grupos.curso
                    grupo = cursos_grupos.grupo
                    semestre = cursos_grupos.semestre

                    cursos_grupos, created = Cursos_Grupos.objects.get_or_create(
                        curso=curso, grupo=grupo, semestre=semestre)

                    estudiante = Estudiante.objects.get(apellidos_nombres=sustentacion_data['estudiante'])
                    jurado1 = Profesor.objects.get(apellidos_nombres=sustentacion_data['jurado1']) if sustentacion_data['jurado1'] else None
                    jurado2 = Profesor.objects.get(apellidos_nombres=sustentacion_data['jurado2']) if sustentacion_data['jurado2'] else None
                    asesor = Profesor.objects.get(apellidos_nombres=sustentacion_data['asesor'])

                    # Verificar si la sustentación ya existe por estudiante, curso y grupo
                    sustentacion_existente = Sustentacion.objects.filter(
                        cursos_grupos=cursos_grupos,
                        estudiante=estudiante
                    ).first()

                    if sustentacion_existente:
                        # Actualizar jurados si están en null y el nuevo valor no es None
                        if not sustentacion_existente.jurado1 and jurado1 is not None:
                            sustentacion_existente.jurado1 = jurado1
                        if not sustentacion_existente.jurado2 and jurado2 is not None:
                            sustentacion_existente.jurado2 = jurado2
                        if not sustentacion_existente.asesor and asesor is not None:
                            sustentacion_existente.asesor = asesor
                        sustentacion_existente.save()

                        # Verificar si el semestre es el vigente
                        if sustentacion_existente.cursos_grupos.semestre == semestre_vigente:
                            # Asignar fecha y horas, usando None para fechas inválidas
                            fecha = sustentacion_data['fecha'] if sustentacion_data['fecha'] and sustentacion_data['fecha'] != 'Fecha Inválida' else None
                            hora_inicio = sustentacion_data['hora_inicio'] if sustentacion_data['hora_inicio'] else None
                            hora_fin = sustentacion_data['hora_fin'] if sustentacion_data['hora_fin'] else None

                            # Crear o actualizar el horario de sustentación
                            horario_existente = Horario_Sustentaciones.objects.filter(sustentacion=sustentacion_existente).first()
                            if horario_existente:
                                horario_existente.fecha = fecha
                                horario_existente.hora_inicio = hora_inicio
                                horario_existente.hora_fin = hora_fin
                                horario_existente.save()
                            else:
                                Horario_Sustentaciones.objects.create(
                                    sustentacion=sustentacion_existente,
                                    fecha=fecha,
                                    hora_inicio=hora_inicio,
                                    hora_fin=hora_fin,
                                )
                    else:
                        continue  # Si no existe la sustentación, continuar al siguiente registro

                except Profesor.DoesNotExist as e:
                    print(f"Error: {str(e)} - Profesor no encontrado. Detalles: {sustentacion_data}")
                    continue
                except ValueError as e:
                    print(f"Error: {str(e)} - Fecha u hora inválida. Detalles: {sustentacion_data}")
                    continue
    except Exception as e:
        raise RuntimeError(f"Error al guardar horarios: {str(e)}")
