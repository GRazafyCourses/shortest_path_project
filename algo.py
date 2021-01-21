import numpy as np  
import random
import sys
import networkx as nx
from networkx.drawing.nx_agraph import write_dot
import matplotlib.pyplot as plt
import matplotlib.animation
import pandas as pd
from ast import literal_eval
from CustomException import NotEnoughPathsException

fig, ax = plt.subplots(figsize=(6,4))

stable = 1
unstable = 2


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
        newWeight = random.choice([d['label'][1]-d['label'][2],d['label'][1]+d['label'][2],d['label'][1]])
        if newWeight <= 0.0:
          newWeight = 1.0
        d['weight'] = newWeight
  return network

def generateNetworks(numberOfNetworks,numberStates):
  tabNetworks = []
  for i in range(0,numberOfNetworks):
    events = [[[]]]
    for x in range(numberStates-1):
        newState = []
        values = []
        count = 0
        event = x+1
        prob=80
        #count != 2 and
        while event <= numberStates: # 2 to change by 4, the 2 in the for is to be switched to 8 (9 states)
            if random.randrange(100) < prob or event==x+2:
                transition = [str(x+1),str(event)]
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


def activity(network,i,numberStates): # add a parameter iteration to access choose i times (uncomment i and while)
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



#tabNetworks = generateNetworks(2)
#network  = tabNetworks[0]
#print(network)
#mygraph = setNetwork(network)
#pos = nx.spring_layout(mygraph)
#adding labels on edges
edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])

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

def fitness(path,graph):
  total_cost = 0
  try:
    total_cost = sum([graph[path[i]][path[i+1]][0]['weight'] for i in range(len(path)-1)])
  except KeyError:
    print("KeyError with the path : "+str(path))
  
  number_hops = len(path)

  return number_hops*10+total_cost

def normalize_fitness(fitness_paths_tab):
  fitness_sum = 0
  fitness_sum_final = 0
  for e in fitness_paths_tab:
    fitness_sum += 1/e["fitness"]
  for e in fitness_paths_tab:
    # (1/fitness)/(1/sumOfFitness) to use the roulette wheel selection in a minimization problem
    e["fitness"] =(1/e["fitness"])/fitness_sum
  for e in fitness_paths_tab:
    fitness_sum_final += e["fitness"]
  #verification that the normalization worked


def select_best_path(tab_paths,graph,number_paths,selected_paths_cross):
  fitness_paths_tab = []

  if (len(tab_paths)<number_paths):
    raise NotEnoughPathsException("the number of paths is inferior to the size of initial population")


  for path in tab_paths:
    fitness_paths_tab.append({
                    "path" : literal_eval(path),
                    "fitness" : fitness(literal_eval(path),graph)})

  #Normalization 
  normalize_fitness(fitness_paths_tab)
  

  for i in range(number_paths):
    #roulette selection
    selected_path = random.choices(fitness_paths_tab, [d['fitness'] for d in fitness_paths_tab], k=1)
    if selected_path[0]['path'] in selected_paths_cross:
      i -= 1
    else:
      # deleted the selected path so it won't be selected again
      fitness_paths_tab = [i for i in fitness_paths_tab if not (i['path'] == selected_path)] 
      selected_paths_cross.append(selected_path[0]['path'])
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


def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3

def cross(indivA,indivB):
  listIntersect = intersection(indivA,indivB)
  pointCrossover = 1
  if len(listIntersect) > 1:
    pointCrossover = int(random.choice(listIntersect))
  new_indivA = np.append(indivA[:pointCrossover],indivB[pointCrossover:])
  new_indivB = np.append(indivB[:pointCrossover],indivA[pointCrossover:])
  return [list(new_indivA),list(new_indivB)]

def accepts(g, path,numberStates):
    return all(map(g.has_edge, path, path[1:])) and path[len(path)-1] == numberStates

def crossover(selected_population,graph,numberStates):
  newGeneration = []
  sortList = []


  for individual in range(0,len(selected_population)):
      for i in range(individual+1,len(selected_population)):
        #test if the intersection is possible
        if intersection(selected_population[individual],selected_population[i]):
          #generation of new individual and adding them to the previous population
          for e in cross(selected_population[individual],selected_population[i]):
            if e not in newGeneration:
              newGeneration.append(e)

  for newInd in newGeneration:
    if accepts(graph,newInd,numberStates):
      sortList.append({
        "path" : newInd,
        "fitness" : fitness(newInd,graph)})
  for oldInd in selected_population:
    if not any(d.get('path') == oldInd for d in sortList):
      sortList.append({
        "path" : oldInd,
        "fitness" : fitness(oldInd,graph)})

  sortList = sorted(sortList,key = lambda i: i['fitness'])

  return sortList


'''A recursive function to print all paths from 'u' to 'd'. 
visited[] keeps track of vertices in current path. 
path[] stores actual vertices and path_index is current index in path[]'''
def allPathsUtil(network, u, d, visited, path,AllPaths): 
  # Mark the current node as visited and store in path 
  visited[int(u)]= True
  path.append(u) 
  # If current vertex is same as destination, then print 
  # current path[] 
  if u == d:
    AllPaths.append(str(path)) 
  else: 
    # If current vertex is not destination 
    # Recur for all the vertices adjacent to this vertex 
    for i in network.neighbors(u): 
      if visited[int(i)]== False: 
        allPathsUtil(network,str(i), d, visited, path,AllPaths)               
    # Remove current vertex from path[] and mark it as unvisited 
  path.pop() 
  visited[int(u)]= False


  
def mutation(crossPathList,graph,probaMutation):
  node2remove = ''
  for path in crossPathList:
    for i in range(0,len(path)):
      if (random.random() < probaMutation):
        if i != 0 and i != len(path['path'])-1:
          setCommonNeigh = set(graph.successors(path['path'][i-1])).intersection(graph.predecessors(path['path'][i+1]))
          try:
            setCommonNeigh.remove(path['path'][i])
          except KeyError:
            print("path['path'][i] : "+path['path'][i])
          if len(setCommonNeigh) > 0 and not graph.has_edge(path['path'][i-1],path['path'][i+1]):
            selectedMutation = int(random.choice(list(setCommonNeigh)))
            path['path'][i] = str(selectedMutation)
            path['fitness'] = fitness(path['path'],graph)
          elif graph.has_edge(path['path'][i-1],path['path'][i+1]):
            node2remove = path['path'][i]
    if node2remove != '':
      path['path'].remove(node2remove)
      node2remove = ''


def maxFitness(resGATab):
  maxPossible = 200000000
  for res in resGATab:
    if res['fitness'] < maxPossible:
      maxPossible = res['fitness']
  return maxPossible

# numberGraph = 5
# numberStates = 9
# tabNetwork = generateNetworksNoNb(numberGraph)

# selected_paths_cross = []
# resTabGA = []
# resNumberGA = []
# for i in range(numberGraph):
#   AllPaths = []
#   path = []
#   visited = [0]*(numberStates+1)
#   mygraph = setNetwork(tabNetwork[i])
#   allPathsUtil(mygraph,"1",str(numberStates),visited,path,AllPaths)
#   print("###########################Select best paths ###################")
#   print(mygraph.edges) 
#   print(AllPaths)
#   print(selected_paths_cross)
#   select_best_path(AllPaths,mygraph,5,selected_paths_cross)
#   print(selected_paths_cross)

# for j in range(15):
#   print("###########################Crossover###################")
#   resTabGA = crossoverNoNb(selected_paths_cross,mygraph)
#   mutation(resTabGA,mygraph,0.1)
#   resNumberGA.append(maxFitness(resTabGA))
# print(resNumberGA)

resNumberGA = [] 
def main(numberGraph,mutationRate,paramNumberStates,numberIterationCrossover):
  tabNetwork = generateNetworks(numberGraph,paramNumberStates)
  resTabGA = []


  for i in range(0,numberGraph):
    visited = [0]*(paramNumberStates+1)
    path = []
    AllPaths = []
    selected_paths_cross = []
    mygraph = setNetwork(tabNetwork[i])
    allPathsUtil(mygraph,"1",str(paramNumberStates),visited,path,AllPaths)
    select_best_path(AllPaths,mygraph,8,selected_paths_cross)
    localRes = []
    for j in range(0,numberIterationCrossover):
      resTabGA = crossover(selected_paths_cross,mygraph,paramNumberStates)
      mutation(resTabGA,mygraph,mutationRate)
      localRes.append(maxFitness(resTabGA))
    resNumberGA.append(localRes)

main(10,0.5,20,100)
print(resNumberGA)
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("A test graph")
for i in range(len(resNumberGA)):
    plt.plot([i for i in range(len(resNumberGA[0]))],[resNumberGA[i][j] for j in range(len(resNumberGA[i]))],label = 'id %s'%i)
plt.legend()
plt.show()

