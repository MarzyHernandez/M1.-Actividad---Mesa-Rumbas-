'''
Agentes para el modelo de limpieza
Autores: Alma Teresa Carpio Revilla
         Mariana Marzayani Hernández Jurado
'''

from mesa import Agent

class CleaningAgent(Agent):
    """
    Agente de limpieza que se mueve por la cuadrícula y limpia celdas sucias.
    """
    def __init__(self, unique_id, model):
        """
        Inicializa un agente de limpieza.
        
        Parámetros:
        - unique_id: Identificador único del agente.
        - model: Instancia del modelo en el cual opera el agente.
        """
        super().__init__(unique_id, model)
        self.is_cleaning = False
        self.moves = 0

    def step(self):
        """
        Define el comportamiento del agente en cada paso.
        Si encuentra suciedad en su celda actual, limpia la celda;
        de lo contrario, se mueve a una posición aleatoria.
        """
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        dirt_present = any(isinstance(obj, Dirt) for obj in cellmates)
        
        if dirt_present:
            self.is_cleaning = True
            dirt = next(obj for obj in cellmates if isinstance(obj, Dirt))
            self.model.grid.remove_agent(dirt)
        else:
            self.is_cleaning = False
            self.random_move()
        
        self.moves += 1
        self.model.total_moves += 1

    def random_move(self):
        """
        Mueve el agente a una posición aleatoria.
        """
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

class Dirt(Agent):
    """
    Representa una celda sucia en la cuadrícula.
    """
    def __init__(self, unique_id, model):
        """
        Inicializa una celda sucia.
        
        Parámetros:
        - unique_id: Identificador único de la celda sucia.
        - model: Instancia del modelo en el cual opera la celda.
        """
        super().__init__(unique_id, model)
