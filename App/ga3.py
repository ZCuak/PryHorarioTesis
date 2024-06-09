import random
from datetime import datetime, timedelta
from collections import defaultdict
from .models import Profesores_Semestre_Academico, Sustentacion, Semana_Sustentacion, Cursos_Grupos, Profesor, Horario_Sustentaciones

# Función para obtener la disponibilidad de los profesores
def obtener_disponibilidad_profesores():
    disponibilidad = defaultdict(list)
    for disp in Profesores_Semestre_Academico.objects.all():
        disponibilidad[disp.profesor_id].append((disp.fecha, disp.hora_inicio, disp.hora_fin))
    return disponibilidad

# Función para verificar disponibilidad de todos los profesores necesarios
def verificar_disponibilidad_profesores(profesores_necesarios):
    disponibilidad = obtener_disponibilidad_profesores()
    sin_disponibilidad = []
    for profesor_id in profesores_necesarios:
        try:
            profesor = Profesor.objects.get(id=profesor_id)
        except Profesor.DoesNotExist:
            print(f"El profesor con ID {profesor_id} no existe.")
            continue
        if profesor_id not in disponibilidad:
            sin_disponibilidad.append(profesor.apellidos_nombres)
    return sin_disponibilidad

# Función para asignar jurados a las sustentaciones que los tengan en null
def asignar_jurados(sustentacion, disponibilidad):
    profesores_disponibles = list(disponibilidad.keys())
    random.shuffle(profesores_disponibles)
    for profesor_id in profesores_disponibles:
        if profesor_id != sustentacion.asesor_id:
            if sustentacion.jurado1_id is None:
                sustentacion.jurado1_id = profesor_id
            elif sustentacion.jurado2_id is None and profesor_id != sustentacion.jurado1_id:
                sustentacion.jurado2_id = profesor_id
                break
    return sustentacion

# Función para obtener las semanas de sustentación solo de tipo parcial
def obtener_semanas_sustentacion():
    semanas = []
    for semana in Semana_Sustentacion.objects.filter(tipo_sustentacion='PARCIAL'):
        semanas.append((semana.fecha_inicio, semana.fecha_fin))
    return semanas

# En la función generar_horarios_disponibles, asegúrate de que la duración sea de 30 minutos
def generar_horarios_disponibles(duracion, disponibilidad):
    campo_horas = defaultdict(list)
    for profesor_id, periodos in disponibilidad.items():
        for fecha, hora_inicio, hora_fin in periodos:
            actual = datetime.combine(fecha, hora_inicio)
            fin_dia = datetime.combine(fecha, hora_fin)
            while actual + timedelta(minutes=duracion) <= fin_dia:
                campo_horas[fecha].append((actual.time(), (actual + timedelta(minutes=duracion)).time()))
                actual += timedelta(minutes=30)  # Intervalos de 30 minutos
    return campo_horas

# Verificación de la disponibilidad de un jurado
def verificar_disponibilidad(jurado, fecha, hora_inicio, hora_fin, disponibilidad):
    if jurado not in disponibilidad:
        return False
    for disp_fecha, disp_hora_inicio, disp_hora_fin in disponibilidad[jurado]:
        if disp_fecha == fecha and disp_hora_inicio <= hora_inicio and disp_hora_fin >= hora_fin:
            return True
    return False

# Verificación de la disponibilidad combinada de los tres jurados
def verificar_disponibilidad_combinada(fecha, hora_inicio, hora_fin, sustentacion, disponibilidad):
    return (verificar_disponibilidad(sustentacion.jurado1_id, fecha, hora_inicio, hora_fin, disponibilidad) and 
            verificar_disponibilidad(sustentacion.jurado2_id, fecha, hora_inicio, hora_fin, disponibilidad) and 
            verificar_disponibilidad(sustentacion.asesor_id, fecha, hora_inicio, hora_fin, disponibilidad))

# Asignación de horarios asegurando no hay conflictos y cada sustentación obtiene un horario válido
def asignar_horarios(sustentaciones, duracion, disponibilidad):
    campo_horas = generar_horarios_disponibles(duracion, disponibilidad)
    semanas_sustentacion = obtener_semanas_sustentacion()
    horarios_asignados = []

    for sustentacion in sustentaciones:
        if sustentacion.jurado1_id is None or sustentacion.jurado2_id is None:
            sustentacion = asignar_jurados(sustentacion, disponibilidad)
        fecha_asignada, inicio_asignado, fin_asignado = None, None, None
        for (fecha_inicio, fecha_fin) in semanas_sustentacion:
            for fecha in campo_horas.keys():
                if fecha_inicio <= fecha <= fecha_fin:
                    for inicio, fin in campo_horas[fecha]:
                        if verificar_disponibilidad_combinada(fecha, inicio, fin, sustentacion, disponibilidad):
                            fecha_asignada, inicio_asignado, fin_asignado = fecha, inicio, fin
                            break
                    if fecha_asignada:
                        break
            if fecha_asignada:
                break
        if fecha_asignada:
            horarios_asignados.append((sustentacion, fecha_asignada, inicio_asignado, fin_asignado))
            campo_horas[fecha_asignada].remove((inicio_asignado, fin_asignado))
        else:
            horarios_asignados.append((sustentacion, None, None, None))
    return horarios_asignados

# Evaluación de la aptitud de un individuo
def evaluar_individuo(individuo):
    penalizacion = sum(1 for sustentacion, fecha, hora_inicio, hora_fin in individuo if not fecha or not hora_inicio or not hora_fin)
    return penalizacion

# Selección de individuos para la reproducción
def seleccion(poblacion):
    evaluaciones = [(individuo, evaluar_individuo(individuo)) for individuo in poblacion]
    evaluaciones.sort(key=lambda x: x[1])
    return [individuo for individuo, _ in evaluaciones[:len(poblacion)//2]]

# Cruce de individuos
def cruzar(individuo1, individuo2):
    punto_cruce = random.randint(0, len(individuo1)-1)
    return individuo1[:punto_cruce] + individuo2[punto_cruce:]

# Mutación de un individuo
def mutar(individuo, tasa_mutacion, sustentaciones, disponibilidad, duracion):
    for i in range(len(individuo)):
        if random.random() < tasa_mutacion:
            sustentacion, _, _, _ = individuo[i]
            fecha, hora_inicio, hora_fin = asignar_horarios([sustentacion], duracion, disponibilidad)[0][1:]
            individuo[i] = (sustentacion, fecha, hora_inicio, hora_fin)
    return individuo

# En la función generar_horarios, cambia la duración de las sustentaciones a 30 minutos
def generar_horarios():
    tamano_poblacion = 100
    generaciones = 20
    tasa_mutacion = 0.01
    duracion_sustentacion = 30  # Duración en minutos cambiada a 30

    sustentaciones = list(Sustentacion.objects.all())
    disponibilidad = obtener_disponibilidad_profesores()

    # Verificar disponibilidad de todos los profesores necesarios
    profesores_necesarios = set()
    for sustentacion in sustentaciones:
        profesores_necesarios.update([sustentacion.asesor_id, sustentacion.jurado1_id, sustentacion.jurado2_id])

    sin_disponibilidad = verificar_disponibilidad_profesores(profesores_necesarios)
    if sin_disponibilidad:
        raise ValueError(f"Los siguientes profesores no tienen disponibilidad registrada: {', '.join(sin_disponibilidad)}")

    # Generar población inicial
    poblacion = [asignar_horarios(sustentaciones, duracion_sustentacion, disponibilidad) for _ in range(tamano_poblacion)]

    for generacion in range(generaciones):
        print(f"Generación {generacion + 1}")
        poblacion = seleccion(poblacion)
        nueva_poblacion = []

        while len(nueva_poblacion) < tamano_poblacion:
            padres = random.sample(poblacion, 2)
            hijo1 = cruzar(padres[0], padres[1])
            hijo2 = cruzar(padres[1], padres[0])
            nueva_poblacion.append(mutar(hijo1, tasa_mutacion, sustentaciones, disponibilidad, duracion_sustentacion))
            nueva_poblacion.append(mutar(hijo2, tasa_mutacion, sustentaciones, disponibilidad, duracion_sustentacion))

        poblacion = nueva_poblacion

    mejor_individuo = min(poblacion, key=lambda ind: evaluar_individuo(ind))
    return mejor_individuo

# Guardar los horarios generados en la base de datos
def guardar_horario(mejor_horario):
    for sustentacion, fecha, hora_inicio, hora_fin in mejor_horario:
        if fecha and hora_inicio and hora_fin:
            Horario_Sustentaciones.objects.create(
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                sustentacion=sustentacion
            )
            print(f"Horario guardado para sustentación {sustentacion.id}: {fecha} {hora_inicio} - {hora_fin}")
        else:
            print(f"Horario no asignado para sustentación {sustentacion.id}")
