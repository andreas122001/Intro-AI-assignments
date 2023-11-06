from multiAgents import MultiAgentSearchAgent
import util
import numpy as np
import math
from pacman import GameState
from game import Actions, Action

class MinimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState: GameState):
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

        return self.max_value(gameState)

        

    def max_value(self, gameState: GameState):
        if self.terminal_test(gameState): return self.evaluationFunction(gameState)
        v, move = -math.inf, 0
        for a in gameState.getLegalActions(0):
            new_state = gameState.generateSuccessor(0, a)
            new_val = self.min_value(new_state)
            if new_val > v:
                v, move = new_val, a
        return v, move

    def min_value(self, gameState: GameState):
        if self.terminal_test(gameState): return self.evaluationFunction(gameState)
        v, move = +math.inf, 0
        for a in gameState.getLegalActions(0):
            new_state = gameState.generateSuccessor(1, a)
            new_val = self.max_value(new_state)
            if new_val < v:
                v, move = new_val, a
        return move

    def terminal_test(self, gameState): 
        return gameState.isWin() or gameState.isLose()


class AlphaBetaAgent(MultiAgentSearchAgent):

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # v ← MAX-VALUE (state, −∞ +∞)
        # return the action a in Actions(state) with value v))
        pass

    def max_value(self, gameState: GameState, alpha: float, beta: float):
        # inputs: state, current state in game
        #     α, the value of the best alternative for max along the path to state
        #     β, the value of the best alternative for min along the path to state
        # if Terminal-Test(state) then return Utility(state)
        # v ← −∞
        # for each a in Actions(state) do
        #     v ← Max(v, MIN-VALUE(s,α, β))
        #     if v ≥ β then return v
        #     α ← Max(α, v)
        # return v
        pass

    def min_value(self, gameState: GameState, alpha: float, beta: float):
        # if Terminal-Test(state) then return Utility(state)
        # v ← +∞
        # for each a in Actions(state) do
        #     v ← Min(v, MAX-VALUE(s,α, β))
        #     if v ≤ α then return v
        #     β ← Min(β, v)
        # return v
        pass

    def terminal_test(self, gameState): 
        return gameState.isWin() or gameState.isLose()
    



class test:
    def getAction(self, gameState):
        move = self.max_value(gameState, depth=0, playerIdx=self.index)    
        print("FINAL:", move)
        return move

    def max_value(self, gameState: GameState, depth: int, playerIdx:int):
        if self.terminal_test(gameState, depth): 
            return self.evaluationFunction(gameState)

        print(f"MAX, Player: {playerIdx+1}/{gameState.getNumAgents()}, Depth: {depth}/{self.depth}")
        print(gameState.getLegalActions(playerIdx))

        v, move = -999999, 'Up'
        for a in gameState.getLegalActions(playerIdx):
            print(f"MAX, Player: {playerIdx+1}/{gameState.getNumAgents()}, Depth: {depth}/{self.depth}, Action: {a}")
            s = gameState.generateSuccessor(playerIdx, a)
            new_val = self.min_value(s, depth, playerIdx+1)
            print("New val:", new_val)
            if new_val > v:
                print(f"New move: {move}->{a}")
                v, move = new_val, a
        return move

    def min_value(self, gameState: GameState, depth: int, playerIdx: int):
        if self.terminal_test(gameState, depth): 
            return self.evaluationFunction(gameState)

        print(f"MIN, Player: {playerIdx+1}/{gameState.getNumAgents()}, Depth: {depth}/{self.depth}")
        print(gameState.getLegalActions(playerIdx))

        v, move = 999999, 'Up'
        for a in gameState.getLegalActions(playerIdx):
            print(f"MIN, Player: {playerIdx+1}/{gameState.getNumAgents()}, Depth: {depth}/{self.depth}, Action: {a}")
            s = gameState.generateSuccessor(playerIdx, a)

            new_val = self.max_value(s, depth+1, 0)
            # if playerIdx == gameState.getNumAgents():
            # else:
            #     new_val = self.min_value(s, depth, playerIdx+1)
            print("New val:", new_val)
            if new_val < v:
                print(f"New move: {move}->{a}")
                v, move = new_val, a
        return move

    def terminal_test(self, gameState: GameState, depth: int):
        if gameState.isWin() or gameState.isLose() or depth > self.depth:
            print(f"Win: {gameState.isWin()}, Lose: {gameState.isLose()}, Depth: {depth>self.depth}")
            return True
        return False