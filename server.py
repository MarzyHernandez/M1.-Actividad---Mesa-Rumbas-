'''
Módulo de visualización para el modelo de limpieza
Autores: Alma Teresa Carpio Revilla
         Mariana Marzayani Hernández Jurado
'''

from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from cleaning_model import CleaningModel
from cleaning_agent import CleaningAgent, Dirt
import random
import time

# Visualización de cantidad de agentes y movimientos
class StatsDisplay(TextElement):
    def render(self, model):
        return f"Agentes: {model.num_agents} | Movimientos: {model.total_moves}"

# Visualización de tiempo máximo y tiempo restante
class TimeDisplay(TextElement):
    def render(self, model):
        current_time = time.time()
        elapsed_time = current_time - model.start_time
        remaining_time = model.max_time - elapsed_time
        return f"Tiempo máximo: {model.max_time} segundos | Tiempo restante: {round(remaining_time)} segundos"

# Visualización de tamaño de la habitación y porcentaje de limpieza
class CleanedCellsDisplay(TextElement):
    def render(self, model):
        cleaned_percentage = model.calculate_cleaned_percentage()
        return f"Tamaño de la habitación: {model.grid.width}x{model.grid.height} | Porcentaje limpio: {cleaned_percentage:.2f}%"

# Definición de las características visuales de los agentes
def agent_portrayal(agent):
    if isinstance(agent, CleaningAgent):
        color = "blue" if agent.is_cleaning else "red"
        return {"Shape": "circle", "Filled": "true", "Layer": 1, "Color": color, "r": 0.5}
    elif isinstance(agent, Dirt):
        return {"Shape": "rect", "Filled": "true", "Layer": 0, "Color": "brown", "w": 0.5, "h": 0.5}
    return {}

# Configuración e inicio del servidor de visualización
def start_server():
    num_agents = random.randint(1, 10)
    grid_size = random.randint(10, 20)
    dirty_percentage = round(random.uniform(0.1, 0.3), 2)
    max_time = random.randint(100, 300)

    grid = CanvasGrid(agent_portrayal, grid_size, grid_size, 500, 500)

    # Gráficas individuales
    cleaned_cells_chart = ChartModule([{"Label": "Cleaned Cells", "Color": "Green"}], canvas_height=200, canvas_width=500)
    cleaned_percentage_chart = ChartModule([{"Label": "Cleaned Percentage", "Color": "Purple"}], canvas_height=200, canvas_width=500)

    # Elementos de visualización
    stats_display = StatsDisplay()
    time_display = TimeDisplay()
    cleaned_display = CleanedCellsDisplay()

    # Iniciar el servidor con los elementos de visualización
    server = ModularServer(
        CleaningModel,
        [time_display, cleaned_display, stats_display, grid, cleaned_cells_chart, cleaned_percentage_chart],
        "M1. Actividad",
        {
            "num_agents": num_agents,
            "grid_size": grid_size,
            "dirty_percentage": dirty_percentage,
            "max_time": max_time
        }
    )
    server.port = 8521
    server.launch()

# Iniciar el servidor
start_server()
