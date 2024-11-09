'''
Modelo de limpieza para simulación de agentes (Rumbas)
Autores: Alma Teresa Carpio Revilla
         Mariana Marzayani Hernández Jurado
'''

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from cleaning_agent import CleaningAgent, Dirt
import time

class CleaningModel(Model):
    """
    Modelo que simula un entorno donde agentes limpian una cuadrícula con celdas sucias.
    """

    def __init__(self, num_agents, grid_size, dirty_percentage, max_time):
        """
        Inicializa el modelo de limpieza.
        
        Parámetros:
        - num_agents: Número de agentes de limpieza.
        - grid_size: Tamaño de la cuadrícula (grid_size x grid_size).
        - dirty_percentage: Porcentaje de celdas inicialmente sucias.
        - max_time: Tiempo máximo de ejecución en segundos.
        """
        super().__init__()
        self.num_agents = num_agents
        self.grid = MultiGrid(grid_size, grid_size, True)
        self.schedule = RandomActivation(self)
        self.dirty_percentage = dirty_percentage
        self.max_time = max_time  # Tiempo máximo en segundos
        self.total_moves = 0
        self.cleaned = False
        self.start_time = time.time()  # Inicio de seguimiento del tiempo real

        # Colección de datos
        self.datacollector = DataCollector(
            {
                "Cleaned Cells": lambda m: self.count_cleaned_cells(),
                "Total Moves": lambda m: m.total_moves,
                "Cleaned Percentage": lambda m: m.calculate_cleaned_percentage()
            }
        )

        # Creación de agentes de limpieza
        for i in range(self.num_agents):
            agent = CleaningAgent(i, self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, (1, 1))

        # Inicialización de celdas sucias
        self._initialize_dirty_cells()

    def _find_empty_cell(self):
        """
        Encuentra una celda vacía en la cuadrícula para colocar un agente o suciedad.
        """
        empty_cells = [(x, y) for x in range(self.grid.width) for y in range(self.grid.height) if self.grid.is_cell_empty((x, y))]
        return self.random.choice(empty_cells)

    def _initialize_dirty_cells(self):
        """
        Inicializa las celdas sucias según el porcentaje especificado.
        """
        num_dirt_cells = int(self.dirty_percentage * self.grid.width * self.grid.height)
        for i in range(num_dirt_cells):
            x, y = self._find_empty_cell()
            dirt = Dirt(f'dirt-{i}', self)
            self.grid.place_agent(dirt, (x, y))

    def count_cleaned_cells(self):
        """
        Cuenta la cantidad de celdas que han sido limpiadas.
        """
        return sum(1 for cell in self.grid.coord_iter() if not any(isinstance(agent, Dirt) for agent in cell[0]))

    def calculate_cleaned_percentage(self):
        """
        Calcula el porcentaje de la cuadrícula que ha sido limpiada.
        """
        total_cells = self.grid.width * self.grid.height
        cleaned_cells = self.count_cleaned_cells()
        return (cleaned_cells / total_cells) * 100

    def step(self):
        """
        Ejecuta un paso del modelo: Mueve agentes, recolecta datos y verifica el estado de limpieza.
        """
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        # Ejecuta el paso de los agentes y recolecta datos
        self.schedule.step()
        self.datacollector.collect(self)
        self.total_moves += 1

        # Verifica si el tiempo ha expirado o si el área está completamente limpia
        if elapsed_time >= self.max_time or self.calculate_cleaned_percentage() == 100:
            self.running = False
            self.cleaned = True
