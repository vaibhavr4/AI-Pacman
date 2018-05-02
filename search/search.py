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
	
def commonSearch(problem,nodeDataStructure):
    
  start_state=problem.getStartState()
  start_node=[start_state,[],0]
  #print "START NODE:",start_node  
  nodeDataStructure.push(start_node)
  pathCoordinateList=[] 
    
  while nodeDataStructure:
    current_node=nodeDataStructure.pop()  
    # check if current node is the goal node, if yes return the path   
    if (problem.isGoalState(current_node[0])):
        return current_node[1]
    #to avoid revisiting an already visited node
    if current_node[0] in pathCoordinateList:
      pass
    else:
      # get the child list of current node if not already visited	
      child_list=problem.getSuccessors(current_node[0])
      
      for child in child_list:
	#for each child in the child list add the corresponding node along with previous visited paths to the data structure(Stack/Queue)
	nodeDataStructure.push((child[0], current_node[1]+ [child[1]], child[2]))
  	
      pathCoordinateList += [current_node[0]]
        
  return []    

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    nodeDataStructure=util.Stack()
    path = commonSearch(problem,nodeDataStructure)
    #print "PATH:",path
    return path

    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    nodeDataStructure=util.Queue() 
    path = commonSearch(problem,nodeDataStructure)
    #print "PATH:",path
    return path

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    def cost(current_node):
    #return the cost of the node for Unifor cost search
	 
        return problem.getCostOfActions(current_node[1])
    #here cost is always 1, since for each step of pacman agent the cost incurred is 1. hence should return same score as bfs
    nodeDataStructure=util.PriorityQueueWithFunction(cost) 
    path = commonSearch(problem,nodeDataStructure)
    #print "PATH:",path
    return path

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    def cost_astar(current_node):
    # here the heuristic which is used to compute Astar (Manhattan/ Euclidean dist) is used from searchAgents package
    # which takes two parameters the position and the problem
        cost=problem.getCostOfActions(current_node[1])+heuristic(current_node[0],problem)
        return cost
  
    nodeDataStructure=util.PriorityQueueWithFunction(cost_astar) 
    path = commonSearch(problem,nodeDataStructure)
    #print "PATH:",path
    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
