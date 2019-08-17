# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        #print("scores: {0}".format(scores))
        bestScore = max(scores)
        #print("bestScore: {0}".format(bestScore))
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        #print("bestIndices: {0}".format(bestIndices))
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        #print("chosenIndex: {0}".format(chosenIndex))

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #return successorGameState.getScore()
        if successorGameState.isWin():
            return float('inf')
        successorScore = successorGameState.getScore()
        score = successorScore

        # The distance to the nearest food
        distanceToFood = float('inf')
        for foodPos in newFood.asList():
            distanceTemp = util.manhattanDistance(newPos, foodPos)
            if distanceTemp < distanceToFood:
                distanceToFood = distanceTemp
        score -= distanceToFood - 4

        # penalty to stay in the same position
        if newPos == currentGameState.getPacmanPosition():
            score -= 2

#        # if the current action direction is same as previous direction,
#        # add 1 score
#        if action == currentGameState.getPacmanState().configuration.getDirection():
#            score += 1

        scareTime = 0
        # # Compute the average scared Time
        # # if pacman has bullet, the avg scared time should be positive and
        # # pacman should chase the scared ghost
        # avgScareTime = 0
        # for index, scareTime in enumerate(newScaredTimes):
        #     # ghostStateConf = newGhostStates[index].configuration
        #     # ghostStatePos = ghostStateConf.pos
        #     avgScareTime += scareTime
        # avgScareTime = len(newScaredTimes)
        # scareTime = avgScareTime
        # score += scareTime

        # Compute the sum of scared Time
        # if pacman has bullet, the avg scared time should be positive and
        # pacman should chase the scared ghost
        sumScareTime = 0
        for index, scareTime in enumerate(newScaredTimes):
            # ghostStateConf = newGhostStates[index].configuration
            # ghostStatePos = ghostStateConf.pos
            sumScareTime += scareTime
        scareTime = sumScareTime
        score += scareTime

        # If pacman has no bullet, pacman should be away from the ghosts
        # The distance to the nearest ghost
        distanceToGhost = float('inf')
        for ghost in newGhostStates:
            ghostPos = ghost.getPosition()
            distanceTemp = util.manhattanDistance(newPos, ghostPos)
            if distanceTemp < distanceToGhost:
                distanceToGhost = distanceTemp
        if 0 == scareTime:
            if distanceToGhost <= 3:
                score += distanceToGhost + 3
        else:
            score -= distanceToGhost

        return score

        # The sum distance to all the food
        # successorScore = successorGameState.getScore()
        # distanceToNearestFood = float('inf')
        # for foodPos in newFood:
        #     distanceTemp = util.manhattanDistance(newPos, foodPos)
        #     if distanceTemp < distanceToNearestFood:
        #         distanceToNearestFood = distanceTemp
        # score = successorScore + distanceToNearestFood
        # if newPos == currentGameState.getPacmanPosition():
        #     score -= 2
        # return score


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
