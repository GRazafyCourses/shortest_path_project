import numpy as np
import random
import sys
import networkx as nx
from networkx.drawing.nx_agraph import write_dot
import matplotlib.pyplot as plt
import pandas as pd


tabStates = []


def addToTab(activityList):
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
sys.stdout=open("out.txt","w")
#w to clean the output file
print ( )
sys.stdout.close()
for i in range(numberofNetworks):
    events = [[]]
    for x in range(9):
        newState = []
        count = 0
        event = x+1
        prob=60
        while count != 4 and event <= 10:
            if random.randrange(100) < prob or event==x+2:
                transition = str(x+1)+str(event)
                newState.append(transition)
                count += 1
            event += 1
            prob -= 5
        if events == [[]]:
            events = [newState]
        else:
            events.append(newState)
    sys.stdout=open("out.txt","a")
    #a to append
    print (events)
    sys.stdout.close()
    #print(events)
#The output "events" gives for each iteration (100) the possible paths of a network


def activity(iteration):
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
numberStates = len(states)

#Sequence of events
events = [["11","12","13"],["22","23","24"],["33","34"]]

# Transition matrix
transitionMatrix = [[0.1,0.6,0.3],[0.1,0.7,0.2],[0.15,0.85]]

#Graph
G = nx.MultiDiGraph()


for e in transitionMatrix:
  for i in range(0,len(e)):
    e[i] = 1/len(e)

#Filling edges for the graph
for i in range(0,len(events)):
  for e in range(0,len(events[i])):
    G.add_edges_from([tuple(list(events[i][e]))],weight=transitionMatrix[i][e])


#if sum(transitionMatrix[0])+sum(transitionMatrix[1])+sum(transitionMatrix[1]) != 3:
#  sys.exit("Transition matrix doesn't have the awaited total")


#adding labels on edges
edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])



# parameter to know the number of iterations (1 in order to make it work properly with 1 iteration )
activity(500)


#### Sorting the tab and creating a dataFrame ####
tabStates = sorted(tabStates, key = lambda i: i['stepCount'],reverse=False)

dfStates = pd.DataFrame(tabStates)
print(dfStates)


#### Creating a subset to compare the number of steps #####
subdfStates = dfStates[['count','stepCount']] 
subdfStates = subdfStates.groupby(['stepCount']).sum()
subdfStates.plot(kind='bar').get_figure()



print(transitionMatrix)

#print the Graph
#pos=nx.spring_layout(G)
#write_dot(G,'graph.dot')
#nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,)
#nx.draw(G,pos)
#plt.show()
