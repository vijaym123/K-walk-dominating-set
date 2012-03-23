import matplotlib.pyplot as plt
import random
import networkx as nx
import math
import numpy
import pdb
import pickle
import time 
import bisect


#Actual Algorithm starts here. Previous Modules are used for analysis purposes.

def findHit(G, A, B, pathA, pathB):
	'''
	G: Graph which is undergoing machine learning
	A: Vertex #1
	B: Vertex #2
	pathA: contains the drunkard walk starting from A
	pathB: contains the drunkard walk starting from B
	Takes 2 vertices A and B from a graph G. Takes a random walk starting from A and takes another random walk starting from B and simultaneously builds the paths. If an intersection is found, the path is established and the corresponding intersection is returned. pathA and pathB are also dynamically updated.
	'''
	walkerA = A #walkers(robots) that take a random walk from given vertices
	walkerB = B

	pathA.append(A) #actual paths that the walkers take
	pathB.append(B)

	while( True ):
		walkerAAdj = G.neighbors(walkerA) #Adjacent vertices for current vertex
		#walkerAAdj.remove('flags')

		walkerBAdj = G.neighbors(walkerB)
		#walkerBAdj.remove('flags')

		randA = random.choice(walkerAAdj) #select one node from the set of neighbors of walkerA and walkerB and assign them to randA and randB respectively
		randB = random.choice(walkerBAdj)
		
		pathA.append(randA) #add the randomly selected edge to the set
		if randA not in pathB: #if randA is already in pathB, then the intersection has occured and there is no need to append randB to pathB. If we append randB to pathB, then there is a chance that we might get two intersection points if randB is also in pathA.
			pathB.append(randB)

		if (randA not in pathB and randB not in pathA): #If the sets are disjoint, then there is no common point that both the walkers now. So, proceed one step further for the next loop
			walkerA = randA
			walkerB = randB
		else:
			break #this implies that the intersection has occured and the infinite while loop should exit. Now, pathA and pathB are the components of the 2-Raw Random Walk

	if pathA[-1] in pathB: #if the last element of pathA is in pathB, then randA must have been the intersection point. Hence, set hit = randA = pathA[-1]
		hit = pathA[-1]
	else:
		hit = pathB[-1] #if the last element of pathB is in pathA, then randB must have been the intersection point. Hence, set hit = randB = pathB[-1]

	return hit

def createPath(pathA, pathB, hit):
	'''
	pathA: drunkard WALK starting from A
	pathB: drunkard WALK starting from B
	hit: the point at which hit has occured.
	Given two paths pathA and pathB and the intersection point hit, then this function integrates them into a path and returns the path. This path may contain cycles and must be removed.
	'''
	Path = []

	Path.extend(pathA[:pathA.index(hit)]) #calculate the index of the hit point and append the nodes in pathA to Path, excluding the hit point
	Path.extend(pathB[pathB.index(hit)::-1]) #calculate the index of the hit point and append the nodes in pathB to Path, including the hit point and IN REVERSE DIRECTION
	return Path

def findPath(G,A,B):
	'''
	A: Vertex #1
	B: Vertex #2
	This function takes in 2 vertices A and B in a graph G. It finds a path from A to B through the method of random walks. It returns the path and the intersection node of the random walk. 
	'''
	
	pathA = []
	pathB = []

	hit = findHit(G, A, B, pathA, pathB) #Take a random walk and stop when an intersection occurs. Return the intersection point.
	Path = createPath(pathA, pathB, hit) #Create a path from A to B. This path may contain cycles too.
	Path = removeCycles(Path) #Remove all the cycles from the current path.
	G[hit]['flags'] += 1 #Flag the hit point at every stage, rather than only for the minimum path case
	return Path, hit

def removeCycles(Path):
	'''
	Given a path, this function removes all the cycles and returns the acyclic path
	'''
	i = 0 #i is the walker
	while i < len(Path): #the length of the path keeps on decreasing as the control flow of the program progresses
		for j in range(len(Path) - 1, i,-1): #move j from the last position to the (i+1)th position, when the path[i] and path[j] are the same, this indicates a cycle. Hence, remove the nodes in between them (inclusive of either end).
			if Path[j] == Path[i]:
				del(Path[i:j])
				break
		i += 1
	return Path


def adamicwalk(G,a,b,path_a,path_b):
	global Degree_Node	

	path_a.append(a)
	path_b.append(b)		

	Flagger_a = {}
	Flagger_b = {}

	while True :
		maxdegree = -1
		maxnode = None
		neighbors_a = Degree_Node[a][1]
		for i in neighbors_a:
			if(maxdegree<Degree_Node[i][0]):
				maxdegree=Degree_Node[i][0]
				maxnode=i

		while Flagger_a.has_key(maxnode):
			try:
				maxnode = neighbors_a.pop() #the neighbor with the next highest degree is NOT being chosen here.
			except IndexError:
				print "Empty =>> Exiting abruptly ...don't know how to handle this case....yet"
				exit()
		path_a.append(maxnode)
		Flagger_a[maxnode] = 1 

		if Flagger_b.has_key(maxnode):
			return maxnode

		a = maxnode

		neighbors_b = Degree_Node[b][1]
		maxdegree = -1
		maxnode = None	
		for i in neighbors_b:
			if(maxdegree<Degree_Node[i][0]):
				maxdegree=Degree_Node[i][0]
				maxnode=i
	
		while Flagger_b.has_key(maxnode):
			try:
				maxnode = neighbors_b.pop() #the neighbor with the next highest degree is NOT being chosen here.
			except IndexError:
				print "Empty =>> Exiting abruptly ...don't know how to handle this case....yet"
				exit()
		path_b.append(maxnode)
		Flagger_b[maxnode] = 1
		
		if Flagger_a.has_key(maxnode):
			return maxnode
		b = maxnode

def testadamic(G,a,b):
	path_a = []
	path_b = []
	hit = adamicwalk(G,a,b,path_a,path_b)
	return createPath(path_a, path_b, hit)				

