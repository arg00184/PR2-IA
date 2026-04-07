# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    inicio = problem.getStartState()
    if problem.isGoalState(inicio):
        return []

    frontera = util.Stack()
    frontera.push((inicio, []))
    visitados = set()

    while not frontera.isEmpty():
        estado, camino = frontera.pop()

        if estado in visitados:
            continue

        visitados.add(estado)

        if problem.isGoalState(estado):
            return camino

        for sucesor, accion, _ in reversed(problem.getSuccessors(estado)):
            if sucesor not in visitados:
                frontera.push((sucesor, camino + [accion]))

    return []

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""

    inicio = problem.getStartState()
    if problem.isGoalState(inicio):
        return []

    frontera = util.PriorityQueue()
    frontera.push((inicio, [], 0), heuristic(inicio, problem))
    mejor_coste = {inicio: 0}

    while not frontera.isEmpty():
        estado, camino, coste_actual = frontera.pop()

        if coste_actual > mejor_coste.get(estado, float('inf')):
            continue

        if problem.isGoalState(estado):
            return camino

        for sucesor, accion, coste_paso in problem.getSuccessors(estado):
            nuevo_coste = coste_actual + coste_paso
            if nuevo_coste < mejor_coste.get(sucesor, float('inf')):
                mejor_coste[sucesor] = nuevo_coste
                prioridad = nuevo_coste + heuristic(sucesor, problem)
                frontera.push((sucesor, camino + [accion], nuevo_coste), prioridad)

    return []


def exploracion(problem: SearchProblem) -> List[Directions]:
    """
    Recorre el mayor numero posible de celdas alcanzables evitando pisar
    el objetivo durante la fase de exploracion para no terminar la partida
    prematuramente.

    Estrategia:
      1) DFS iterativo para explorar celdas alcanzables NO objetivo.
      2) Backtracking explicito para reconstruir una secuencia ejecutable.
      3) Al terminar, BFS desde la posicion actual hasta el objetivo.

    Ademas deja estadisticas en problem.explorationStats para facilitar
    el analisis
    """

    inicio = problem.getStartState()

    if problem.isGoalState(inicio):
        problem.explorationStats = {
            'steps': 0,
            'unique_cells': 1,
            'repetition_ratio': 0.0,
        }
        return []

    visitados = {inicio}
    acciones_recorrido = []
    posicion_actual = inicio

    # Pila DFS: [estado, sucesores_restantes]
    pila = [[inicio, list(problem.getSuccessors(inicio))]]

    while pila:
        actual, sucesores = pila[-1]

        siguiente_candidato = None
        while sucesores:
            estado_sucesor, accion_sucesora, _ = sucesores.pop(0)
            # No pisar el objetivo durante la exploracion para evitar un final prematuro.
            if problem.isGoalState(estado_sucesor):
                continue
            if estado_sucesor not in visitados:
                siguiente_candidato = (estado_sucesor, accion_sucesora)
                break

        if siguiente_candidato is not None:
            estado_sucesor, accion_sucesora = siguiente_candidato
            visitados.add(estado_sucesor)
            acciones_recorrido.append(accion_sucesora)
            posicion_actual = estado_sucesor
            pila.append([estado_sucesor, list(problem.getSuccessors(estado_sucesor))])
            continue

        # Si no hay sucesores validos, se hace backtracking al padre.
        pila.pop()
        if pila:
            estado_padre = pila[-1][0]
            accion_retroceso = None
            for sucesor, accion, _ in problem.getSuccessors(actual):
                if sucesor == estado_padre:
                    accion_retroceso = accion
                    break
            if accion_retroceso is not None:
                acciones_recorrido.append(accion_retroceso)
                posicion_actual = estado_padre

    # Al terminar la exploracion, se busca el objetivo desde la posicion actual.
    frontera = util.Queue()
    frontera.push((posicion_actual, []))
    vistos = {posicion_actual}

    camino_al_objetivo = []
    while not frontera.isEmpty():
        estado, camino = frontera.pop()
        if problem.isGoalState(estado):
            camino_al_objetivo = camino
            break

        for estado_sucesor, accion, _ in problem.getSuccessors(estado):
            if estado_sucesor not in vistos:
                vistos.add(estado_sucesor)
                frontera.push((estado_sucesor, camino + [accion]))

    acciones = acciones_recorrido + camino_al_objetivo

    # Reconstruye los estados recorridos para medir las celdas unicas visitadas.
    cursor_estado = inicio
    celdas_unicas_recorridas = {inicio}
    for accion in acciones:
        siguiente_estado = None
        for estado_sucesor, accion_sucesora, _ in problem.getSuccessors(cursor_estado):
            if accion_sucesora == accion:
                siguiente_estado = estado_sucesor
                break
        if siguiente_estado is None:
            break
        celdas_unicas_recorridas.add(siguiente_estado)
        cursor_estado = siguiente_estado

    pasos = len(acciones)
    celdas_unicas = len(celdas_unicas_recorridas)
    ratio_repeticion = (float(pasos) / celdas_unicas) if celdas_unicas > 0 else 0.0
    problem.explorationStats = {
        'steps': pasos,
        'unique_cells': celdas_unicas,
        'repetition_ratio': ratio_repeticion,
    }

    return acciones
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
exp = exploracion

