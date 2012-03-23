import networkx as nx
import matplotlib.pyplot as plt
import random
import AtoB
from mayavi import mlab
import numpy

def Kwalk(G,node,length,numOfRandomWalks):
	"""
	Syntax : Kwalk(G,node,length,numOfRandomWalks)
	where :
		G is Graph
		Node denotes 'from Node' to start a random walk
		length denotes k_walk_length
		numOfRandomWalks denotes the number of randomwalks from a node

	Flagger is a Global Dictionary containing the information about the flags associated with each node. 			
	"""
	global Flagger
	while numOfRandomWalks > 0 :
		temp_node = node
		temp_length = length
		while temp_length > 0 :
			neighbors = G.neighbors(temp_node)
			choice = random.choice(neighbors)	
			temp_length = temp_length - 1
			temp_node = choice
			try :
				Flagger[choice] +=1
			except KeyError :
				Flagger[choice] = 1
		numOfRandomWalks-=1				
			
def Correctness_Of_DominatingSet(G,length,NumOfRandomWalk,DominatingSet):
	for node in G.nodes():
		probability = Probality_Of_Hiting_A_Dominating_Set(G,node,length,NumOfRandomWalk,DominatingSet)
		if ( probability < 0.4 ) : 
			return False	
	return True

def Probality_Of_Hiting_A_Dominating_Set(G,node,length,numOfRandomWalks,DominatingSet):

	NoOfHits = 0
	temp_numOfRandomWalks = numOfRandomWalks

	while numOfRandomWalks > 0 :
		temp_node = node
		if node in DominatingSet :
			NoOfHits +=1
		else :		
			temp_length = length
			while temp_length > 0 :
				neighbors = G.neighbors(temp_node)
				choice = random.choice(neighbors)	
				temp_length = temp_length - 1
				temp_node = choice
				if choice in DominatingSet :
					NoOfHits +=1
					break 			
		numOfRandomWalks-=1
	
	numOfRandomWalks = temp_numOfRandomWalks
	probability = float(NoOfHits)/numOfRandomWalks
	return probability


def Plot_Graph(G,highlight_nodes):
	"""
	Syntax : Plot_Graph(G,highlight_nodes)
	where :
		G is Graph.
		highlight_nodes is set of nodes which needs to be highlighted.
	"""
	
	pos=nx.spring_layout(G) # positions for all nodes
	nx.draw_networkx_nodes(G,pos,
	                       nodelist=G.nodes(), #[i[1] for i in Flag_Node_Pair[lenght_set:]],
	                       node_color='r',
	                       node_size=50,
        	               alpha=0.8)
	nx.draw_networkx_nodes(G,pos,
	                       nodelist=highlight_nodes, #[i[1] for i in Flag_Node_Pair[:lenght_set]],
	                       node_color='b',
	                       node_size=50,
	                       alpha=0.8)
	labels={}
	for i in G.nodes():
		labels[i] = str(i)
	nx.draw_networkx_labels(G,pos,labels,font_size=8)
	nx.draw_networkx_edges(G,pos,width=0.5,alpha=0.5)
	plt.show() 

#m*n denotes the grid size 
m=10
n=10

#numOfRandomWalks denotes the number of randomwalks from a node
numOfRandomWalks = 200000

#Flagger is a dictionary denotes the no of flags for each node in the Graph
Flagger = {}

#k_walk_length denotes the lenght of the walk you want to take from each node.
k_walk_length = 20

#Length of the Dominating Set
lenght_set = 4

#Dominating Set
DominatingSet = []

#Grid Network
G=nx.grid_2d_graph(m,n)

#From each node take a random walk of specified k_walk_length,numOfRandomWalks
for node in G.nodes():
	#Function call Kwalk(G,node,k_walk_length,numOfRandomWalks)
	Kwalk(G,node,k_walk_length,numOfRandomWalks)
	

# Flag_Node_Pair = [ ( Number of Flags,Node ) , ( , ) ..............]
Flag_Node_Pair = Flagger.items()
total=sum(Flagger.values())
s =[]
for i in range(m):
	x = []
	for j in range(n):
		x.append(Flagger[(i,j)]*600/float(total))
	s.append(x)
m = numpy.array([i for i in s ])
mlab.barchart(m)
mlab.show()
"""
for i in range(len(Flag_Node_Pair)):
	Flag_Node_Pair[i] = (Flag_Node_Pair[i][1],Flag_Node_Pair[i][0])

#Sorting the Flag_Node_Pair, to find the nodes which have most frequently visited !

Flag_Node_Pair.sort()
Flag_Node_Pair.reverse()


for length_set in range(1,len(Flag_Node_Pair)):
	DominatingSet = [i[1] for i in Flag_Node_Pair[:length_set]] 
	if Correctness_Of_DominatingSet(G,k_walk_length,numOfRandomWalks,DominatingSet) :
		break
Plot_Graph(G,DominatingSet)

x = input("tell me something : ")
#-------------------------------------------------------------------------------------------------------------------------------------

#NodePairs in G
Nodes = G.nodes()
NodePairs = []
length_set = 10

for i in range(len(Nodes)) :
	for j in range(i+1,len(Nodes)):
		NodePairs.append((Nodes[i],Nodes[j]))

#Flagger in intersection centrality
Flagger = {}
length = len(NodePairs)

print "hello"
count = 0
for i in NodePairs:
	count+=1 
	pathA = []
	pathB = []
	print "Completed", float(count)/length	
	hit = AtoB.findHit(G,i[0],i[1], pathA, pathB)
	try :
		Flagger[hit] +=1
	except KeyError :
		Flagger[hit] = 0

# Flag_Node_Pair = [ ( Number of Flags,Node ) , ( , ) ..............]

Flag_Node_Pair = Flagger.items()

for i in range(len(Flag_Node_Pair)):
	Flag_Node_Pair[i] = (Flag_Node_Pair[i][1],Flag_Node_Pair[i][0])

Flag_Node_Pair.sort()
Flag_Node_Pair.reverse()
#highlight_nodes = [i[1] for i in Flag_Node_Pair[:length_set]]
#Plot_Graph(G,highlight_nodes)

total=sum(Flagger.values())
s =[]
for i in range(m):
	x = []
	for j in range(n):
		x.append(Flagger[(i,j)]/float(20))
	s.append(x)
m = numpy.array([i for i in s ])
mlab.barchart(m)
mlab.show()
#-----------------------------------------------------------------------------------------------------------------------------------
"""
