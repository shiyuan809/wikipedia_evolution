import snap
import numpy as np
import parser2
import matplotlib.pyplot as plt
from matplotlib import pylab
from pylab import *
import pickle

#total no. of nodes

#Use snap default to get number of nodes and edges

def Get_Out_Degree_Distribution(G):
	Deg_dist = snap.TIntPrV()
	snap.GetOutDegCnt(G, Deg_dist)

	degree = np.empty((1,0))
	count = np.empty((1,0))

	for node_degree_pr in Deg_dist:

		if node_degree_pr.GetVal1() > 0:

			degree = np.append(degree,node_degree_pr.GetVal1())

			count = np.append(count,node_degree_pr.GetVal2())

	'''
	plt.figure(1)
	plt.scatter(degree,count,s=25, c = 'b', marker = 'o')
	plt.yscale('log')	
	plt.xscale('log')
	plt.xlabel('Out-Degree')
	plt.ylabel('No. of Nodes')
	pylab.show()
	'''



def Get_In_Degree_Distribution(G):
	Deg_dist = snap.TIntPrV()
	snap.GetInDegCnt(G, Deg_dist)

	degree = np.empty((1,0))
	count = np.empty((1,0))

	for node_degree_pr in Deg_dist:

		if node_degree_pr.GetVal1() > 0:

			degree = np.append(degree,node_degree_pr.GetVal1())

			count = np.append(count,node_degree_pr.GetVal2())

	'''
	plt.figure(1)
	plt.scatter(degree,count,s=25, c = 'b', marker = 'o')

	plt.yscale('log')	
	plt.xscale('log')
	plt.xlabel('In-Degree')
	plt.ylabel('No. of Nodes')
	pylab.show()
	'''



#largest connected component
def Get_Connected_Components(G):
	Components = snap.TCnComV()
	snap.GetWccs(G, Components)

	for CnCom in Components:
		print("Size of component: %d" % CnCom.Len())

def diameter(G):
	G_sub = snap.GetMxWcc(G)
	d = snap.GetBfsEffDiam(G_sub, 100, False)
	return d

def main():
	G = parser2.processor(addr='enwiki.link_snapshot.2001-03-01.csv')
	#G = parser2.processor(addr='enlink_snapshot.2004-03-01.csv')
	
	#Get_Connected_Components(G)

	Get_Out_Degree_Distribution(G)
	Get_In_Degree_Distribution(G)

	print("Estimated diameter is %d"%diameter(G))

	print("average degree is %f"%(G.GetEdges()*2/G.GetNodes()))

	with open('G_save', 'wb') as handle:
		pickle.dump(G, handle)



if __name__ == '__main__':
    main()


