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

#Skyler Lee (HXL220052)
#Winston Shih (WXS190012
#12/1/2025

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
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
    "*** YOUR CODE HERE ***"
    from util import Stack

    start = problem.getStartState() # This is where we begin the search

    # If the start state is what we're already looking for, then we are done already
    if problem.isGoalState(start):
        return []

    # we need to travel so create a stack
    stack = Stack()
    # each entry in the stack stores Key-Value pair (state, path taken)
    stack.push((start, [])) # this is the node we just started with, didn't move yet so it's empty
    visited = set() # store visited nodes here

    # begin the traversal part
    while not stack.isEmpty():
        state, path = stack.pop()

        # don't visit nodes we already visited
        if state in visited:
            continue

        # if we got here we did not visit this yet
        visited.add(state)

        # is this what we are looking for in the final state
        if problem.isGoalState(state):
            return path # if so we found the path so return

        # we need to use the getSuccessors method as provided in the assignment
        # (there's a specific order we should push successors)
        for triple in problem.getSuccessors(state):
            successor = triple[0]
            action = triple[1]
            # we don't need stepcost
            # what possible paths can we go now
            if successor not in visited: # this is a path we did not go to yet
                stack.push((successor, path + [action])) # we didn't visit this yet so add this new path and push

    # stack is empty (so we went through every possible solutions) but we never found the goal state
    # so that means there is no solution
    return []


    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue

    # start with the initial state
    start = problem.getStartState()

    # if the initial state is what we're already looking for, then we found it
    if problem.isGoalState(start):
        return []

    queue = Queue()
    queue.push((start, [])) # push the (initial state, path) into the queue
    visited = set()
    visited.add(start)

    while not queue.isEmpty():
        state, path = queue.pop() # the next one to check

        # if this is what we are looking for, return the path for it
        if problem.isGoalState(state):
            return path

        # get the possible paths we can take
        for triple in problem.getSuccessors(state):
            successor = triple[0]
            action = triple[1]
            # we don't use stepcost
            if successor not in visited:
                # if we did not visit this yet, go and visit it
                visited.add(successor)
                queue.push((successor, path + [action]))
    return []


    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    # get the start state
    start = problem.getStartState()

    # if this is what we are looking for, return
    if problem.isGoalState(start):
        return []

    pq = PriorityQueue()
    # we push a pq entry <state, path, cost> with priority cost for the starting node
    pq.push((start, [], 0), 0)
    visited = set()

    while not pq.isEmpty():
        state, path, cost = pq.pop() # get the next entry

        # if we found the goal from this entry, return the path for it
        if problem.isGoalState(state):
            return path

        # if we did not visit this yet, go visit it
        if state not in visited:
            visited.add(state)

            # get the next possible paths
            for triple in problem.getSuccessors(state):
                successor = triple[0]
                action = triple[1]
                stepCost = triple[2]
                if successor not in visited:
                    # if we did not visit this possible path yet, go visit it
                    pq.push((successor, path + [action], cost + stepCost),
                            cost + stepCost)
    return []

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    # get the starting state
    start = problem.getStartState()
    # if this is goal state we already found our goal
    if problem.isGoalState(start):
        return []

    # pq stores <state, path, g>
    pq = PriorityQueue()
    # same as uniform cost but instead of using cost for pq priority, use heuristic
    pq.push((start, [], 0), heuristic(start, problem))

    # HashMap<State state, int value>
    hashMap = {start: 0}

    while not pq.isEmpty():
        # the next one to check
        state, path, g = pq.pop()

        # if this g isn't the best option then ignore
        thisState = 0
        if hashMap.get(state) is None:
            thisState = float('inf') # this state doesn't exist, so make it + infinity
        else:
            thisState = hashMap.get(state)

        # found better g?
        if g > thisState:
            continue

        # is this what we are looking for
        if problem.isGoalState(state):
            return path

        for triple in problem.getSuccessors(state):
            successor = triple[0]
            action = triple[1]
            stepCost = triple[2]

            g2 = g + stepCost # this is the new g after the step

            # but only go here if this is actually better
            thisSuccessor = 0
            if hashMap.get(successor) is None:
                thisSuccessor = float('inf') # hashmap doesn't have this successor so make it pos inf
            else:
                thisSuccessor = hashMap.get(successor)
            if g2 < thisSuccessor:
                hashMap[successor] = g2 # found better g value
                f = g2 + heuristic(successor, problem) # f = g + h
                pq.push((successor, path + [action], g2), f) # f is new pq cost

    return []

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
