# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        stateList = self.mdp.getStates()
        for iteration in range(self.iterations):
            stateValueList = []
            # Store values
            for state in stateList:
                if self.mdp.isTerminal(state):
                    stateValueList.append(None)
                    continue
                stateValueList.append(self.getMaxValue(state)[0])

            # Update values
            for index, state in enumerate(stateList):
                if stateValueList[index] != None:
                    self.values[state] = stateValueList[index]


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def getMaxValue(self, state):
        validActionList = self.mdp.getPossibleActions(state)
        valueList = []
        for action in validActionList:
            q_value = self.computeQValueFromValues(state, action)
            valueList.append(q_value)
        max_value = max(valueList)
        max_index = valueList.index(max_value)
        return max_value, max_index

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        successorList = self.mdp.getTransitionStatesAndProbs(state, action)
        q_values = 0
        for successor in successorList:
            nextState = successor[0]
            reward = self.mdp.getReward(state, action, nextState)
            probability = successor[1]
            value = 0
            if not self.mdp.isTerminal(nextState):
                value = self.values[nextState]
            q_values += probability * (reward + self.discount * value)
        return q_values

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None
        max_value, max_index = self.getMaxValue(state)
        validActionList = self.mdp.getPossibleActions(state)
        return validActionList[max_index]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        stateList = self.mdp.getStates()
        for iteration in range(self.iterations):
            state = stateList[iteration%len(stateList)]
            if self.mdp.isTerminal(state):
                continue
            self.values[state] = self.getMaxValue(state)[0]

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def getPredecessorMap(self, stateList):
        predecessorMap = {}
        for state in stateList:
            if self.mdp.isTerminal(state):
                continue
            for action in self.mdp.getPossibleActions(state):
                for successor in  self.mdp.getTransitionStatesAndProbs(state, action):
                    nextState = successor[0]
                    if nextState not in predecessorMap.keys():
                        predecessorMap[nextState] = set()
                    predecessorMap[nextState].add(state)
        return predecessorMap


    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        stateList = self.mdp.getStates()
        # compute predecessorMap
        predecessorMap = self.getPredecessorMap(stateList)
        priorityQueue = util.PriorityQueue()
        # Get the initial diff for priorituQueue
        for state in stateList:
            if self.mdp.isTerminal(state):
                continue
            max_value, _ = self.getMaxValue(state)
            diff = abs(max_value - self.values[state])
            priorityQueue.push(state, -diff)

        for iteration in range(self.iterations):
            if priorityQueue.isEmpty():
                return
            state = priorityQueue.pop()
            if not self.mdp.isTerminal(state):
                self.values[state] = self.getMaxValue(state)[0]
            for predecessor in predecessorMap[state]:
                max_value, _ = self.getMaxValue(predecessor)
                diff = abs(self.values[predecessor] - max_value)
                if diff > self.theta:
                    priorityQueue.update(predecessor, -diff)
