import numpy as np  
import random
import sys
import networkx as nx
from networkx.drawing.nx_agraph import write_dot
import matplotlib.pyplot as plt
import pandas as pd


def setNetwork(network):
    G = nx.MultiDiGraph()
    LocaltransitionMatrix = network[1]
    Localevents = network[0]
    for i in range(0,len(Localevents)):
        for e in range(0,len(Localevents[i])):
            G.add_edges_from([tuple(list(Localevents[i][e]))],weight=LocaltransitionMatrix[i][e][1],label=LocaltransitionMatrix[i][e])
    return G

def addToTab(activityList):
  tabStates = []
  if not any(d.get('Path') == str(activityList) for d in tabStates):
    tabStates.append({
      "Path" : str(activityList),
      "count":1,
      "stepCount": len(activityList)-1
    })
  else:
    for d in tabStates:
      if(d.get('Path') == str(activityList)):
        d['count'] = d['count'] + 1

def generateNetworks(numberOfNetworks):
  tabNetworks = []
  for i in range(0,numberOfNetworks):
    events = [[[]]]
    for x in range(numberStates):
        newState = []
        values = []
        count = 0
        event = x+1
        prob=60
        while count != 2 and event <= 9: # 2 to change by 4, the 2 in the for is to be switched to 8 (9 states)
            if random.randrange(100) < prob or event==x+2:
                transition = str(x+1)+str(event)
                newState.append(transition)
                count += 1
            event += 1
            prob -= 5
        nbTransitions = len(newState)
        #We can't use the last while as we need to know the total number of transition to get the same availability on each
        for p in range(0,nbTransitions):
            availability = 1/nbTransitions
            weight = random.randrange(1,10)
            #weight can't = 0
            if random.randrange(1,10) > 7:
              power = str(availability)+","+str(weight)+","+str(unstable)
            else:
              power = str(availability)+","+str(weight)+","+str(stable)
            values.append(power)
        if events == [[[]]]:
            events = [[newState],[values]]
        else:
            events[0].append(newState)
            events[1].append(values)
    tabNetworks.append(events)
  return tabNetworks
    #print(events)
#The output "events" gives for each iteration (100) the possible paths of a network

def activity(network):
  #Starting state
    i = 0
    while i != iteration:
      y = 0
      firstState ="1"
      activityList = [firstState]
      i += 1 
      while firstState != str(numberStates):
        pas = 0
        you = 1
        change = np.random.choice(events[y],replace=True,p=transitionMatrix[y])
        while pas != 1:
          if change == events[y][0]:
            activityList.append(events[y][0][-1])
            change = np.random.choice(events[y],replace=True,p=transitionMatrix[y])
          elif change == events[y][you]:
            newState = events[y][you][-1]
            firstState = newState
            activityList.append(newState)
            pas = 1
          else:
            you += 1
        y += 1
      addToTab(activityList)



#generateNetworks(100)

#States
states = ["1","2","3","4"]


#Sequence of events
events = [["11","12","13"],["22","23","24"],["33","34"]]

# Transition matrix
transitionMatrix = [[[0.1,20],[0.6,5],[0.6,3]],[[0.6,20],[0.6,5],[0.6,1]],[[0.6,30],[0.6,4],[0.6,2]],[[0.6,40],[0.6,6]]]


#Graph
G = nx.MultiDiGraph()

# initializing with same weight for every arcs
for e in transitionMatrix:
  for i in range(0,len(e)):
    e[i][0]= 1/len(e)


#Filling edges for the graph
for i in range(0,len(events)):
  for e in range(0,len(events[i])):
    G.add_edges_from([tuple(list(events[i][e]))],weight=transitionMatrix[i][e][1],label=transitionMatrix[i][e])


#if sum(transitionMatrix[0])+sum(transitionMatrix[1])+sum(transitionMatrix[1]) != 3:
#  sys.exit("Transition matrix doesn't have the awaited total")


#adding labels on edges
edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])


def findBestPath(network):
    pathsTab = []
    visitedNode = ["1"]
    currentPath = ["1"]
    currentPathCost = 0
    currentState = "1"
    finalState = "5"
    while currentState != finalState:
        shortestArc = ""
        weightNeighor = 0
        print("## CurrentState:"+currentState)
        print("## Going through neigbors:"+str(list(network.neighbors(currentState))))
        print("## Current Path:"+str(currentPath))
        for e in list(network.neighbors(currentState)):
            path2add = list.copy(currentPath)
            weightNeighor = network.get_edge_data(currentState,e)[0]['weight']
            if e not in visitedNode:
                path2add.append(e)
                pathsTab.append({
                    "path" : path2add,
                    "weight" : currentPathCost+weightNeighor})
                print("## Adding :"+str(path2add))
            if shortestArc == "":
                shortestArc = e
            else:
                if weightNeighor < network.get_edge_data(currentState,shortestArc)[0]['weight']:
                    shortestArc = e
        print("## shortestArc is:" +  str(shortestArc))
        
        currentPathCost += network.get_edge_data(currentState,shortestArc)[0]['weight']
        print("## CurrentPathCost is:" +  str(currentPathCost))
        change = False
        for e in pathsTab:
            if currentPathCost > e['weight']:
                currentPath = e['path']
                shortestArc = e['path'][len(e['path'])-1]
                change = True
                print("## I CHANGE MY PLANS :"+str(currentState))
        if change == False:
            currentPath.append(shortestArc)
        print("## I Choose :"+str(shortestArc))
        currentState = shortestArc
        visitedNode.append(shortestArc)
        print(pathsTab)
    pathsTab.append({
    "path" : currentPath,
    "weight" : currentPathCost
    })
    print(visitedNode)
    print(pathsTab)
    print(currentPathCost)
    return currentPath

numberStates = 2 #Total number of states
stable = 2
unstable = 6
tabNetwoks = generateNetworks(2)
network  = tabNetwoks[0]
mygraph = setNetwork(network)
activity(network)
print(tabNetwoks)
