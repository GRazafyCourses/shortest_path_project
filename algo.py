import numpy as np  
import random
import sys
import networkx as nx
from networkx.drawing.nx_agraph import write_dot
import matplotlib.pyplot as plt
import matplotlib.animation
import pandas as pd
import seaborn.apionly as sns

fig, ax = plt.subplots(figsize=(6,4))

def setNetwork(network):
    localGraph = nx.MultiDiGraph()
    LocaltransitionMatrix = network[1]
    Localevents = network[0]
    for i in range(0,len(Localevents)):
        for e in range(0,len(Localevents[i])):
            listValue = list(LocaltransitionMatrix[i][e].split(","))
            listValue = list(map(float, listValue))            
            localGraph.add_edges_from([tuple(list(Localevents[i][e]))],weight=listValue[1],label=listValue)
    
    return localGraph

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

def changeWeight(network,networkList):
  LocaltransitionMatrix = networkList[1]
  Localevents = networkList[0]
  for i in range(0,len(Localevents)):
    for e in range(0,len(Localevents[i])):
      for u,v,d in network.edges(data=True):
        #print("listValue[1]: " +str(d['label'][1]))
        #print("[listValue[1]-listValue[2]: " +str(d['label'][1]-d['label'][2]))
        #print("[listValue[1]+listValue[2]: " +str(d['label'][1]+d['label'][2]))
        newWeight = random.choice([d['label'][1]-d['label'][2],d['label'][1]+d['label'][2],d['label'][1]])
        if newWeight <= 0.0:
          newWeight = 1.0
        #print(d)
        #print("newWeight: " +str(newWeight))
        d['weight'] = newWeight
  return network

def generateNetworks(numberOfNetworks):
  tabNetworks = []
  for i in range(0,numberOfNetworks):
    events = [[[]]]
    for x in range(numberStates-1):
        newState = []
        values = []
        count = 0
        event = x+1
        prob=60
        #count != 2 and
        while event <= numberStates: # 2 to change by 4, the 2 in the for is to be switched to 8 (9 states)
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
            weight = random.randrange(1,9)
            #weight can't = 0
            if p == 0:
              power = str(availability)+",9"+","+str(stable)
            elif random.randrange(1,10) > 7:
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

def activity(network,i): # add a parameter iteration to access choose i times (uncomment i and while)
    # i = 0
    # while i != iteration:
      print("RAW NETWORK" + str(network.edges.data()))
      firstState ="1"
      activityList = [firstState]
      # i += 1 
      while int(firstState) != numberStates:
        desiredState = 0
        choice = 1000.0 # huge number to access the first if below, changed afterwards
        #Search for every possibility
        for e in list(network.neighbors(firstState)):
          weight = network.get_edge_data(firstState,e)[0]['weight']
          if choice > weight:
            choice = weight
            desiredState = e
          
        firstState = desiredState
        activityList.append(desiredState)
        network = changeWeight(network,i)
        print(network.edges.data())
      print(activityList)

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


numberStates = 4 #Total number of states
stable = 2
unstable = 6
#tabNetworks = generateNetworks(2)
#network  = tabNetworks[0]
#print(network)
#mygraph = setNetwork(network)
#pos = nx.spring_layout(mygraph)
#adding labels on edges
edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])
idx_colors = sns.cubehelix_palette(5, start=.5, rot=-.75)[::-1]
idx_weights = [3,2,1]
sequence_of_letters = "".join(['2', '3', '4'])

def update(num):
    ax.clear()
    i = num // 3
    j = num % 3 + 1

    triad = sequence_of_letters[i:i+3]
    path = ["1"] + ["".join(sorted(set(triad[:k + 1]))) for k in range(j)]

    # Background nodes
    nx.draw_networkx_edges(mygraph, pos=pos, ax=ax, edge_color="gray")
    null_nodes = nx.draw_networkx_nodes(mygraph, pos=pos, nodelist=set(mygraph.nodes()) - set(path), node_color="white",  ax=ax)
    null_nodes.set_edgecolor("black")

    # Query nodes
    query_nodes = nx.draw_networkx_nodes(mygraph, pos=pos, nodelist=path, node_color=idx_colors[:len(path)], ax=ax)
    query_nodes.set_edgecolor("white")
    nx.draw_networkx_labels(mygraph, pos=pos, labels=dict(zip(path,path)),  font_color="white", ax=ax)
    edgelist = [path[k:k+2] for k in range(len(path) - 1)]
    nx.draw_networkx_edges(mygraph, pos=pos, edgelist=edgelist, width=idx_weights[:len(path)], ax=ax)

    # Scale plot ax
    ax.set_title("Frame %d:    "%(num+1) +  " - ".join(path), fontweight="bold")
    ax.set_xticks([])
    ax.set_yticks([])

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



#ani = matplotlib.animation.FuncAnimation(fig, update, frames=6, interval=1000, repeat=True)
#plt.show()
count = 0
for i in generateNetworks(1):
  count+= 1
  mygraph = setNetwork(i)
  activity(mygraph,i)
  print(count)
