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

from game import Agent, Actions
from pacman import GameState
import math

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
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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
        return successorGameState.getScore()

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
    Minimax agent (Q2)
    """

    def getAction(self, gameState):
        """Gets an action by Minimax-search, starting with maximizing player"""
        v, move = self.max_value(gameState)  
        return move

    def max_value(self, gameState: GameState, depth: int = 0, playerIdx: int = 0) -> str|int:
        if self.terminal_test(gameState, depth): # Check if finished
            return self.evaluationFunction(gameState), 'Up'

        # Initiate value and move (placeholders)
        v, move = -math.inf, 'Up'
        for a in gameState.getLegalActions(0):
            new_state = gameState.generateSuccessor(0, a)

            # Recurse to first Ghost (Min), same depth
            new_val, _ = self.min_value(new_state, depth, playerIdx+1)

            # If this value is higher, update action
            if new_val > v:
                v, move = new_val, a
        return v, move

    def min_value(self, gameState: GameState, depth: int, playerIdx: int = 1) -> str|int:
        if self.terminal_test(gameState, depth): # Check if finished
            return self.evaluationFunction(gameState), 'Up'

        # Initiate value and move (placeholders)
        v, move = math.inf, 'Up'
        for a in gameState.getLegalActions(playerIdx): # for all actions
            new_state = gameState.generateSuccessor(playerIdx, a) # get the new state

            # If we are last Ghost (Min), recurse to PacMan (Max)
            if playerIdx+1 == gameState.getNumAgents():
                new_val, _ = self.max_value(new_state, depth+1, 0) # increment depth, player=0
            # Else, we recurse to the next Ghost
            else:
                new_val, _ = self.min_value(new_state, depth, playerIdx+1) # same depth, increment player
            
            # If this value is lower, update action
            if new_val < v:
                v, move = new_val, a
        return v, move

    def terminal_test(self, gameState: GameState, depth: int):
        """
        Checks if state is terminal (win, loss or max depth)
        """
        return gameState.isWin() or gameState.isLose() or depth >= self.depth


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Minimax agent with alpha-beta pruning (Q3)
    """

    def getAction(self, gameState):
        """
        Gets an action by minimax-search using alpha-beta pruning, starting with maximizing player
        """
        v, move = self.max_value(gameState)  
        return move

    def max_value(self, gameState: GameState, alpha=-math.inf, beta=math.inf, depth: int = 0, playerIdx: int = 0) -> str|int:
        if self.terminal_test(gameState, depth): # Check if finished
            return self.evaluationFunction(gameState), 'Up'

        # Initiate value and move (placeholders)
        v, move = -math.inf, 'Up'
        for a in gameState.getLegalActions(0):
            new_state = gameState.generateSuccessor(0, a)

            # Recurse to first Ghost (Min), same depth
            new_val, _ = self.min_value(new_state, alpha, beta, depth, playerIdx+1)

            # If this value is higher, set new action and update beta
            if new_val > v:
                v, move = new_val, a
                alpha = max(alpha, v)

            # Check beta agains value
            if v > beta:
                return v, move
        return v, move

    def min_value(self, gameState: GameState, alpha=-math.inf, beta=math.inf, depth: int = 0, playerIdx: int = 1) -> str|int:
        if self.terminal_test(gameState, depth): # Check if finished
            return self.evaluationFunction(gameState), 'Up'

        # Initiate value and move (placeholders)
        v, move = math.inf, 'Up'
        for a in gameState.getLegalActions(playerIdx): # for all actions
            new_state = gameState.generateSuccessor(playerIdx, a) # get the new state

            # If we are last Ghost (Min), recurse to PacMan (Max)
            if playerIdx+1 == gameState.getNumAgents():
                new_val, _ = self.max_value(new_state, alpha, beta, depth+1, 0) # increment depth
            # Else, we recurse to the next Ghost
            else:
                new_val, _ = self.min_value(new_state, alpha, beta, depth, playerIdx+1) # increment player
            
            # If this value is lower, set new action and update beta
            if new_val < v:
                v, move = new_val, a
                beta = min(beta, v)

            # Check alpha against value
            if v < alpha:
                return v, move
        return v, move

    def terminal_test(self, gameState: GameState, depth: int):
        """
        Checks if state is terminal (win, loss or max depth)
        """
        return gameState.isWin() or gameState.isLose() or depth >= self.depth

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
