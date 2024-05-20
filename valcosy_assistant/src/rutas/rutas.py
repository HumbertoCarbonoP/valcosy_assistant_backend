import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from queue import PriorityQueue
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD

class Node:
    def __init__(self, coordinates: tuple[float, float], tags: set[str], name: str, address: str):
        self.coordinates = coordinates
        self.tags = tags
        self.name = name
        self.address = address
        self.parent = None
        self.neighbors = None
        self.g = 0
        self.h = 0
        self.f = 0

def get_nodes():
    valcosy_hotel = Node((0, 0), ["hotel"], "Hotel Valcosy", "Avenida Barbosa")
    heladeria1 = Node((0, 20), ["heladería", "postres", "exterior"], "Helados del Cielo", "123 Calle Principal")
    heladeria2 = Node((40, 20), ["heladería", "familia", "interior"], "Frescura Glacial", "456 Calle Secundaria")
    libreria1 = Node((20,0), ["librería", "lectura", "exterior"], "Mundo de Libros", "321 Calle Literaria")
    libreria2 = Node((40, 50), ["librería", "café", "interior"], "Letras y Café", "258 Calle del Saber")
    museo1 = Node((30, 80), ["museo", "arte", "exterior"], "Museo del Arte Moderno", "654 Avenida Quinta")
    museo2 = Node((30, 10), ["museo", "historia", "interior"], "Historias del Ayer", "987 Paseo Sexto")
    restaurante1 = Node((60, 30), ["restaurante", "italiano", "exterior"], "Sabores de Italia", "789 Vía Terciaria")
    restaurante2 = Node((10, 40), ["restaurante", "vegano", "interior"], "Verde Natural", "321 Camino Cuarto")
    cafeteria1 = Node((20, 60), ["cafetería", "café", "exterior"], "Aroma de Oriente", "1357 Ruta Séptima")
    cafeteria2 = Node((50, 70), ["cafetería", "té", "interior"], "Tés del Mundo", "2468 Camino Octavo")
    bar1 = Node((10, 10), ["bar", "nocturno", "exterior"], "Noches de Moscú", "8642 Avenida Novena")
    bar2 = Node((70, 60), ["bar", "cocteles", "interior"], "Cocteles de la Ciudad", "7531 Paseo Décimo")
    parque1 = Node((20, 30), ["parque", "naturaleza", "exterior"], "Oasis Verde", "789 Parque Central")
    parque2 = Node((60, 50), ["parque", "recreación", "interior"], "Parque Aventura", "678 Avenida de los Árboles")

    valcosy_hotel.neighbors = [heladeria1, libreria1, bar1]
    heladeria1.neighbors = [valcosy_hotel, restaurante2, bar1]
    heladeria2.neighbors = [museo2, parque1, restaurante1]
    libreria1.neighbors = [valcosy_hotel, bar1]
    libreria2.neighbors = [cafeteria1, parque2, restaurante1, parque1]
    bar1.neighbors = [valcosy_hotel, libreria1, heladeria1, parque1, museo2]
    bar2.neighbors = [restaurante1, parque2, cafeteria2]
    museo1.neighbors = [cafeteria2, cafeteria1]
    museo2.neighbors = [bar1, heladeria2]
    restaurante1.neighbors = [heladeria2, libreria2, parque2, bar2]
    restaurante2.neighbors = [cafeteria1, parque1, heladeria1]
    cafeteria2.neighbors = [bar2, parque2, museo1]
    cafeteria1.neighbors = [museo1, libreria2, restaurante2]
    parque1.neighbors = [heladeria2, libreria2, restaurante2, bar1]
    parque2.neighbors = [restaurante1, libreria2, cafeteria2, bar2]

    return [valcosy_hotel, heladeria1, heladeria2, restaurante1, restaurante2, museo1, museo2, cafeteria1, cafeteria2, bar1, bar2, libreria1, libreria2, parque1, parque2]


def distance(node1: Node, node2: Node):
    x1, y1 = node1.coordinates
    x2, y2 = node2.coordinates
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def a_star_search(startNode: Node, endNode: Node, preferences: dict):
    opened_list = PriorityQueue()
    closed_list = set()
    g_costs = {startNode: 0}

    opened_list.put((0, startNode))

    while not opened_list.empty():
        current_cost, current_node = opened_list.get()

        if current_node == endNode:
            path = []
            while current_node:
                if current_node != endNode:
                    if 'exterior' in current_node.tags and preferences['Preferencia_Exterior'].iloc[0] < 0.5:
                        current_node.name = ''
                    if 'interior' in current_node.tags and preferences['Preferencia_Interior'].iloc[0] < 0.5:
                        current_node.name = ''
                path.append(current_node)
                current_node = current_node.parent
            return path[::-1]
        
        closed_list.add(current_node)

        for neighbor in current_node.neighbors:
            if neighbor in closed_list:
                continue

            tentative_g_cost = g_costs[current_node] + distance(current_node, neighbor)

            if tentative_g_cost < g_costs.get(neighbor, float('inf')):
                neighbor.parent = current_node
                neighbor.g = tentative_g_cost
                neighbor.h = distance(neighbor, endNode)
                total_cost = neighbor.g + neighbor.h
                g_costs[neighbor] = tentative_g_cost
                opened_list.put((total_cost, neighbor))

    return None

def plot_graph(node):
    G = nx.Graph()
    pos = {}
    labels = {}

    for node in node:
        G.add_node(node)
        pos[node] = node.coordinates
        labels[node] = node.name  # Etiqueta del nodo

        # Añadiendo aristas para cada vecino del nodo
        for neighbor in node.neighbors:
            G.add_edge(node, neighbor)

    nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue', font_size=8, node_size=500)
    plt.show()

def plot_path(path):
    G = nx.Graph()
    pos = {}
    labels = {}

    for node in path:
        G.add_node(node)
        pos[node] = node.coordinates  # Estableciendo la posición del nodo
        labels[node] = node.name  # Etiqueta del nodo

        # Añadiendo aristas para cada vecino del nodo
        if node.parent:
            G.add_edge(node, node.parent)

    nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue', font_size=8, node_size=500)
    plt.show()
    

def bayesian():
    model = BayesianNetwork([('Clima', 'Preferencia'), ('Hora', 'Preferencia')])
    # Los valores de las tablas de distribucion de probabilidad condicional
    # asocian las preferencias de un usuario respecto a si un lugar externo
    # o interno se prefiere con el clima y hora dados.
    # Se lee así:

    # Probabilidad haya clima soleado: 0.7 vs lluvioso: 0.3
    cpd_clima = TabularCPD(variable='Clima', variable_card=2, values=[[0.7], [0.3]], state_names={'Clima': ['Soleado', 'Lluvioso']})
    # Probabilidad de salir en horas de la mañana: 0.4 vs Tarde:0.3 vs Noche: 0.3
    cpd_hora = TabularCPD(variable='Hora', variable_card=3, values=[[0.4], [0.3], [0.3]], state_names={'Hora': ['Mañana', 'Tarde', 'Noche']})


    # Probabilidad de preferir salir a un lugar exterior dado que es soleado y
    # es las horas de la mañana es de: 0.6 (primer lugar de primera fila)
    # Esta tabla de CPD requiere dos hileras: para la probabilidad de
    # que se prefiere un sitio exterior vs interior con las condiciones de clima
    # y luego hora (el orden importa). Hay 2 climas posibles y 3 tiempos por lo
    # que 2*3= 6 probabilidades son necesarias en este caso
    # La tabla para preferencias se vería así:
    """
    | Clima     | Hora    | Probabilidad de Exterior | Probabilidad de Interior |
    |-----------|---------|--------------------------|---------------------------|
    | Soleado   | Mañana  | 0.6                      | 0.4                       |
    | Soleado   | Tarde   | 0.8                      | 0.2                       |
    | Soleado   | Noche   | 0.7                      | 0.3                       |
    | Lluvioso  | Mañana  | 0.3                      | 0.7                       |
    | Lluvioso  | Tarde   | 0.4                      | 0.6                       |
    | Lluvioso  | Noche   | 0.6                      | 0.4                       |
    """
    cpd_pref = TabularCPD(variable='Preferencia', variable_card=2,
                        values=[[0.6, 0.8, 0.7, 0.3, 0.4, 0.6],
                                [0.4, 0.2, 0.3, 0.7, 0.6, 0.4]],
                        evidence=['Clima', 'Hora'],
                        evidence_card=[2, 3],
                        state_names={'Preferencia': ['Exterior', 'Interior'],
                                    'Clima': ['Soleado', 'Lluvioso'],
                                    'Hora': ['Mañana', 'Tarde', 'Noche']})

    model.add_cpds(cpd_clima, cpd_hora, cpd_pref)

    assert model.check_model()
    return model


nodes = get_nodes()

def get_preferences():
    final_node_index = 0
    print('-------------------------------------------------------------------------------------------\n')
    for i in range(len(nodes)):
        print(f'{i}. {nodes[i].name}')
    while (final_node_index > len(nodes) - 1 or final_node_index < 1):
        final_node_index = int(input('Ingresa el número de opción que será el final de tu ruta: ').split(' ')[0])
    final_node = nodes[final_node_index]
    return final_node



def encontrar_ruta(final_node: int, climate: str, hour: str):
    model = bayesian()
    condiciones = pd.DataFrame({'Clima': [climate], 'Hora': [hour]})
    final_node = nodes[final_node]
    probabilities = model.predict_probability(condiciones)
    path = a_star_search(nodes[0], final_node, probabilities)
    final_route = []
    counter = 1
    for i in range(len(path)):
        if(path[i].name != ''):
            final_route.append(f'{counter}. {path[i].name}   {path[i].address}   {path[i].tags}')
            counter += 1
    return final_route