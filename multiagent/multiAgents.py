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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
	pacPos = tuple(newPos)
	oldFood = currentGameState.getFood().asList()
        #Calculate position of ghost from pacman  
    	for ghostState in newGhostStates:
      		#Assign ghost-postion.
      		ghostPos = ghostState.getPosition()
      		#Check if pacman and the ghost pos is the same/ they collide.
      		if ghostPos == pacPos:
            		return -100
          
    	#Calculate manhattan distance of food from pacman.
    	for food in oldFood:
      		if Directions.STOP in action:  
        		return -100
		
		dist = [manhattanDistance(food,pacPos)]
      		#Sort the manhattan dist list.
      		dist.sort()
      		value = dist[0]
    	return (-value)

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
	def minimaxcalc(gameState,pacagent,depth):
 	    # return the evaluation if game is won/lost or given depth is reached.
            if depth == self.depth or gameState.isWin() or gameState.isLose(): 
                return self.evaluationFunction(gameState)
	    #pacman max
            if pacagent == 0:  
                return max(minimaxcalc(gameState.generateSuccessor(pacagent, newState),1, depth) for newState in gameState.getLegalActions(pacagent))
            #ghost min
	    else:  
	        # calculate the next agent and increase depth.
                nextAgent = pacagent + 1  
                if gameState.getNumAgents() == nextAgent:
                    nextAgent = 0
                if nextAgent == 0:
                   depth += 1
                return min(minimaxcalc(gameState.generateSuccessor(pacagent, newState),nextAgent, depth) for newState in gameState.getLegalActions(pacagent))

        # max for root - pacman
        maximum = float("-inf")
        action = Directions.WEST
        for agentState in gameState.getLegalActions(0):
            eval_result = minimaxcalc(gameState.generateSuccessor(0,agentState),1, 0)
            if eval_result > maximum or maximum == float("-inf"):
                maximum = eval_result
                action = agentState

        return action
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
        #util.raiseNotDefined()
	
	#setting initial values as infinity
	value,action = self.alphaValue(gameState,float('-inf'),float('inf'),0,self.depth) 
	return action
    #for pacman	
    def alphaValue(self,state,alpha,beta,agentNumber,depth):
	if state.isWin() or state.isLose():
		return self.evaluationFunction(state),'none'
		
	val = float('-inf')
	actions = state.getLegalActions(agentNumber)
	bestAction = actions[0]
		
	for action in actions:
		successorState = state.generateSuccessor(agentNumber,action)
		previous_v = val
		# return the evaluation if game is won/lost or given depth is reached.
		if depth == 0 or successorState.isWin() or successorState.isLose(): 
			val = max(val,self.evaluationFunction(successorState))
		else:
			val = max(val,self.betaValue(successorState,alpha,beta,agentNumber+1,depth))
		#checking the pruning condition		
		if val > beta:	 
			return val,action
		alpha = max(alpha,val) 
		if val != previous_v:
			bestAction = action 
	return val,bestAction

    #for ghosts
    def betaValue(self,state,alpha,beta,agentNumber,depth):
	if state.isWin() or state.isLose():
		return self.evaluationFunction(state),'none'
	
	val = float('inf')
	actions = state.getLegalActions(agentNumber)
	flag = False
	for action in actions:
		
		successorState = state.generateSuccessor(agentNumber,action)
		if depth == 0 or successorState.isWin() or successorState.isLose():
	
			val = min(val,self.evaluationFunction(successorState))
		elif agentNumber == (state.getNumAgents() - 1): 
			if flag == False: 
				depth = depth -1
				flag=True
			#if the last depth is reached
			if depth == 0: 
				val = min(val,self.evaluationFunction(successorState))
			else:
				val = min(val,self.alphaValue(successorState,alpha,beta,0,depth)[0])
			
		else:	
			val = min(val,self.betaValue(successorState,alpha,beta,agentNumber+1,depth))
		#checking the pruning condition		
		if val < alpha: 
			return val
		beta = min(beta,val)

	return val	

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
        #util.raiseNotDefined()
        def expectimaxCalc(agent, depth, gameState):
	    # return the evaluation if game is won/lost or given depth is reached.
            if depth == self.depth or gameState.isLose() or gameState.isWin() : 
                return self.evaluationFunction(gameState)
            if agent == 0:  
                return max(expectimaxCalc(1, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent))
            else:  
		# expectimax for ghosts
                agentNextpos = agent + 1  
                if gameState.getNumAgents() == agentNextpos:
                    agentNextpos = 0
                if agentNextpos == 0:
                    depth += 1
		tempExpectimax = (expectimaxCalc(agentNextpos, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent))
                return sum(tempExpectimax) / float(len(gameState.getLegalActions(agent)))
        
        maxVal = float("-inf")
        action = Directions.WEST
        for agentState in gameState.getLegalActions(0):
            tempEval = expectimaxCalc(1, 0, gameState.generateSuccessor(0, agentState))
            if tempEval > maxVal or maxVal == float("-inf"):
                maxVal = tempEval
                action = agentState

        return action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
       
    newFoodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    pacmanPos = currentGameState.getPacmanPosition()
    currentScore = currentGameState.getScore()
    capsules = currentGameState.getCapsules()
    capScore = 0

    
    #Check if capsule list is not empty.
    if(len(capsules) != 0):
    #Use manhattan distance formula to Calculate the distance between pacman and capsules
      for capsule in capsules:
        capDist = min([manhattanDistance(pacmanPos,capsule)])
        if capDist == 0 :
          capScore = float(1)/capDist
        else:
          capScore = -100
        
    #Calculate distance between ghosts and pacman using Manhattan distance       
    for ghost in ghostStates:
      ghostPos = (ghost.getPosition()[0]),(ghost.getPosition()[1])
      ghostDist = manhattanDistance(pacmanPos, ghostPos)
    
    evalScore = currentScore  - (1.0/1+ghostDist)  + (1.0/1+capScore)
    
    return evalScore



# Abbreviation
better = betterEvaluationFunction

