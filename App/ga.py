import random
from datetime import datetime, timedelta
from django.db import models
from .models import *

# Algoritmo genético
class AlgoritmoGenetico:
    def __init__(self, poblacion_size, generaciones, cursos_grupos, disponibilidad_profesores):
        self.poblacion_size = poblacion_size
        self.generaciones = generaciones
        self.cursos_grupos = cursos_grupos
        self.disponibilidad_profesores = disponibilidad_profesores
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
        for curso_grupo in self.cursos_grupos:
            sustentacion = {
                'cursos_grupos': curso_grupo,
                'estudiante': self.seleccionar_estudiante(curso_grupo),
                'jurado1': self.seleccionar_profesor(curso_grupo),
                'jurado2': self.seleccionar_profesor(curso_grupo),
                'asesor': curso_grupo.profesor,
                'titulo': self.generar_titulo()
            }
            individuo.append(sustentacion)
        return individuo

    def seleccionar_estudiante(self, curso_grupo):
        sustentaciones = Sustentacion.objects.filter(cursos_grupos=curso_grupo)
        estudiantes = [sustentacion.estudiante for sustentacion in sustentaciones]
        if not estudiantes:
            raise ValueError(f"No hay estudiantes disponibles para el curso_grupo {curso_grupo}")
        estudiante = random.choice(estudiantes)
        print(f"Seleccionado estudiante {estudiante} para el curso {curso_grupo}")
        return estudiante

    def seleccionar_profesor(self, curso_grupo):
        profesores = Profesor.objects.all()
        if not profesores:
            raise ValueError(f"No hay profesores disponibles")
        profesor = random.choice(profesores)
        print(f"Seleccionado profesor {profesor} para el curso {curso_grupo}")
        return profesor

    def generar_titulo(self):
        titulos = ["Sistema de Gestión", "Aplicación Móvil", "Solución de BI"]
        titulo = random.choice(titulos)
        print(f"Generado título: {titulo}")
        return titulo

    def calcular_fitness(self, individuo):
        fitness = 0
        for sustentacion in individuo:
            # Verificar disponibilidad de los profesores
            disponibilidad_jurado1 = self.disponibilidad_profesores.get((sustentacion['jurado1'].id, sustentacion['cursos_grupos'].semestre.id))
            disponibilidad_jurado2 = self.disponibilidad_profesores.get((sustentacion['jurado2'].id, sustentacion['cursos_grupos'].semestre.id))
            disponibilidad_asesor = self.disponibilidad_profesores.get((sustentacion['asesor'].id, sustentacion['cursos_grupos'].semestre.id))

            if disponibilidad_jurado1 and disponibilidad_jurado2 and disponibilidad_asesor:
                fitness += 1
        print(f"Fitness calculado para individuo: {fitness}")
        return fitness

    def seleccionar_padres(self):
        padres = random.sample(self.poblacion, 2)
        print(f"Seleccionados padres: {padres}")
        return padres

    def cruzar(self, padre1, padre2):
        punto_cruce = random.randint(1, len(padre1) - 1)
        hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
        hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
        print(f"Cruzados padres en punto {punto_cruce}: hijo1 = {hijo1}, hijo2 = {hijo2}")
        return hijo1, hijo2

    def mutar(self, individuo):
        if random.random() < 0.1:
            sustentacion_mutada = random.choice(individuo)
            sustentacion_mutada['jurado1'] = self.seleccionar_profesor(sustentacion_mutada['cursos_grupos'])
            sustentacion_mutada['jurado2'] = self.seleccionar_profesor(sustentacion_mutada['cursos_grupos'])
            print(f"Mutado individuo: {individuo}")
        return individuo

    def evolucionar(self):
        print("Evolucionando población...")
        nueva_poblacion = []
        while len(nueva_poblacion) < self.poblacion_size:
            padres = self.seleccionar_padres()
            hijo1, hijo2 = self.cruzar(padres[0], padres[1])
            nueva_poblacion.append(self.mutar(hijo1))
            nueva_poblacion.append(self.mutar(hijo2))
        self.poblacion = nueva_poblacion
        print(f"Nueva población: {nueva_poblacion}")

    def ejecutar(self):
        for generacion in range(self.generaciones):
            print(f"Generación {generacion + 1}")
            self.poblacion = sorted(self.poblacion, key=lambda ind: self.calcular_fitness(ind), reverse=True)
            self.evolucionar()
        mejor_individuo = max(self.poblacion, key=lambda ind: self.calcular_fitness(ind))
        print(f"Mejor individuo encontrado: {mejor_individuo}")
        return mejor_individuo

# Uso del algoritmo genético
def generar_horarios():
    cursos_grupos = Cursos_Grupos.objects.all()
    disponibilidad_profesores = {
        (disp.profesor.id, disp.semestre.id): disp
        for disp in Profesores_Semestre_Academico.objects.all()
    }
    ag = AlgoritmoGenetico(poblacion_size=10, generaciones=50, cursos_grupos=cursos_grupos, disponibilidad_profesores=disponibilidad_profesores)
    mejor_horario = ag.ejecutar()
    print(f"Mejor horario generado: {mejor_horario}")
    return mejor_horario
