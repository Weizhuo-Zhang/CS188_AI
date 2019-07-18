# myAgents.py
# ---------------
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

from game import Agent
from searchProblems import PositionSearchProblem

import util
import time
import search

"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
def createAgents(num_pacmen, agent='MyAgent'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]

class MyAgent(Agent):
    """
    Implementation of your agent.
    """
    __goalList = []

    def getAction(self, state):
        """
        Returns the next action the agent will take
        """

        "*** YOUR CODE HERE ***"
        # TODO 1. store the optimal path in cache
        start = time.time()
        action = None
        #######################################################################
        # TODO Trial one: if some agents have same target, first come first get.
        #       If the target just be taken by another agents, choose another
        #       target
        # foodList = state.getFood().asList()
        # hasFoodBeenEaten = (None != self.goalState) and \
        #                    (self.goalState not in foodList)
        # if ([] == self.actionList) or hasFoodBeenEaten:
        #######################################################################

        #######################################################################
        # TODO Trial two: if some agents have same target, choose the min cost
        #       agent, other agent searching for another food.
        if ([] == self.actionList):
            if (None != self.goalState):
                self.removeGoalList(self.goalState)
            startPosition = state.getPacmanPosition(self.index)
            problem = ClosestFoodSearchProblem(
                        state,
                        self.index,
                        self.getGoalList())
            #self.actionList = search.breadthFirstSearch(problem)
            #self.actionList = search.uniformCostSearch(problem)
            self.actionList =\
                search.aStarSearch(problem, foodHeuristic)
            self.goalState = problem.getGoalState()
            self.appendGoalList(self.goalState)
            #print("AAA")
            #print(self.goalState)
            #print(self.getGoalList())
        action = self.actionList.pop(0)
        end = time.time()
        print('time cost {:5.2f}ms'.format((end-start)*1000))
        return action
        #######################################################################

#        if ([] == self.actionList):
#            startPosition = state.getPacmanPosition(self.index)
#            #walls = state.getWalls()
#            problem = ClosestFoodSearchProblem(state, self.index)
#            self.goalState = problem.goalState
#            self.actionList = search.breadthFirstSearch(problem)
#        action = self.actionList.pop(0)
#        end = time.time()
#        print('time cost {:5.2f}ms'.format((end-start)*1000))
#        return action

    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """

        "*** YOUR CODE HERE"
        self.actionList = []
        self.goalState = None

    @classmethod
    def removeGoalList(cls, goalState):
        cls.__goalList.remove(goalState)

    @classmethod
    def appendGoalList(cls, goalState):
        cls.__goalList.append(goalState)

    @classmethod
    def getGoalList(cls):
        return cls.__goalList

"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""

class ClosestDotAgent(Agent):

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition(self.index)
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState, self.index)


        "*** YOUR CODE HERE ***"
        return search.breadthFirstSearch(problem)

    def getAction(self, state):
        return self.findPathToClosestDot(state)[0]

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state

        "*** YOUR CODE HERE ***"
        foodList = self.food.asList()
        return (state in foodList)

class ClosestFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to the closest food.
    """
    def __init__(self, gameState, agentIndex, goalList):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE
        self.goalState = None
        self.goalList = goalList

    def isGoalState(self, state):
        foodList = self.food.asList()
        if ((state not in self.goalList) and (state in foodList)):
            self.goalState = state
            return True
        else:
            return False

    def getGoalState(self):
        return self.goalState

def foodHeuristic(state, problem):
    position = state
    foodList = problem.food.asList()
    minDistance = 999999
    nearestFoodPosition = position
    for foodPosition in foodList:
        tempDistance = util.manhattanDistance(position, foodPosition)
        if tempDistance < minDistance:
            minDistance = tempDistance
            nearestFoodPosition = foodPosition
    return minDistance
