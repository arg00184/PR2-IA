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
    start = problem.getStartState()
    if problem.isGoalState(start):
        return []

    frontier = util.Stack()
    frontier.push((start, []))
    visited = set()

    while not frontier.isEmpty():
        state, path = frontier.pop()

        if state in visited:
            continue

        visited.add(state)

        if problem.isGoalState(state):
            return path

        for successor, action, _ in reversed(problem.getSuccessors(state)):
            if successor not in visited:
                frontier.push((successor, path + [action]))

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
    start = problem.getStartState()
    if problem.isGoalState(start):
        return []

    frontier = util.PriorityQueue()
    frontier.push((start, [], 0), heuristic(start, problem))
    best_cost = {start: 0}

    while not frontier.isEmpty():
        state, path, cost_so_far = frontier.pop()

        if cost_so_far > best_cost.get(state, float('inf')):
            continue

        if problem.isGoalState(state):
            return path

        for successor, action, step_cost in problem.getSuccessors(state):
            new_cost = cost_so_far + step_cost
            if new_cost < best_cost.get(successor, float('inf')):
                best_cost[successor] = new_cost
                priority = new_cost + heuristic(successor, problem)
                frontier.push((successor, path + [action], new_cost), priority)

    return []


def exploracion(problem: SearchProblem) -> List[Directions]:
    """
    Recorre el mayor nÃºmero posible de celdas alcanzables evitando pisar
    el objetivo durante la fase de exploraciÃ³n para no terminar la partida
    prematuramente.

    Estrategia:
      1) DFS iterativo para explorar celdas alcanzables NO objetivo.
      2) Backtracking explÃ­cito para reconstruir una secuencia ejecutable.
      3) Al terminar, BFS desde la posiciÃ³n actual hasta el objetivo.

    AdemÃ¡s deja estadÃ­sticas en problem.explorationStats para facilitar
    el anÃ¡lisis de desempeÃ±o solicitado en la prÃ¡ctica.
    """

    start = problem.getStartState()

    if problem.isGoalState(start):
        problem.explorationStats = {
            'steps': 0,
            'unique_cells': 1,
            'repetition_ratio': 0.0,
        }
        return []

    visited = {start}
    traversal_actions = []
    current_position = start

    # Pila DFS: [estado, sucesores_restantes]
    stack = [[start, list(problem.getSuccessors(start))]]

    while stack:
        current, successors = stack[-1]

        next_candidate = None
        while successors:
            succ_state, succ_action, _ = successors.pop(0)
            # No pisar el objetivo durante exploraciÃ³n para evitar fin prematuro.
            if problem.isGoalState(succ_state):
                continue
            if succ_state not in visited:
                next_candidate = (succ_state, succ_action)
                break

        if next_candidate is not None:
            succ_state, succ_action = next_candidate
            visited.add(succ_state)
            traversal_actions.append(succ_action)
            current_position = succ_state
            stack.append([succ_state, list(problem.getSuccessors(succ_state))])
            continue

        # Sin nuevos sucesores vÃ¡lidos: backtrack al padre.
        stack.pop()
        if stack:
            parent_state = stack[-1][0]
            reverse_action = None
            for s, a, _ in problem.getSuccessors(current):
                if s == parent_state:
                    reverse_action = a
                    break
            if reverse_action is not None:
                traversal_actions.append(reverse_action)
                current_position = parent_state

    # Al terminar la exploraciÃ³n, ir al objetivo desde posiciÃ³n actual.
    frontier = util.Queue()
    frontier.push((current_position, []))
    seen = {current_position}

    path_to_goal = []
    while not frontier.isEmpty():
        state, path = frontier.pop()
        if problem.isGoalState(state):
            path_to_goal = path
            break

        for succ_state, action, _ in problem.getSuccessors(state):
            if succ_state not in seen:
                seen.add(succ_state)
                frontier.push((succ_state, path + [action]))

    actions = traversal_actions + path_to_goal

    # Reconstruye estados recorridos para medir celdas Ãºnicas visitadas.
    state_cursor = start
    unique_path_cells = {start}
    for action in actions:
        next_state = None
        for succ_state, succ_action, _ in problem.getSuccessors(state_cursor):
            if succ_action == action:
                next_state = succ_state
                break
        if next_state is None:
            break
        unique_path_cells.add(next_state)
        state_cursor = next_state

    steps = len(actions)
    unique_cells = len(unique_path_cells)
    repetition_ratio = (float(steps) / unique_cells) if unique_cells > 0 else 0.0
    problem.explorationStats = {
        'steps': steps,
        'unique_cells': unique_cells,
        'repetition_ratio': repetition_ratio,
    }

    return actions


def exploration(problem):
    "Compatibilidad con posibles referencias previas en inglÃ©s." 
    return exploracion(problem)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
exp = exploracion

