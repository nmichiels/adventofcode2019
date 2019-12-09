from __future__ import division 
import numpy as np

file = open('input_6.txt', 'r')


data = np.loadtxt('input_6.txt', delimiter=')', dtype='str')


from anytree import Node, RenderTree, AsciiStyle, PreOrderIter
from anytree.search import find
from anytree.walker import Walker


tree = Node(data[0,0])

trees = [tree]


for i in range(data.shape[0]):

	# find parent
	parent = None
	for t in range(len(trees)):
		n = find(trees[t], lambda node: node.name == data[i,0])

		#if (n and not parent):
			#print("double parent")
		if (n):
			parent = n

	# if no parent yet, make new tree
	if not parent:
		# make new tree
		parent = Node(data[i,0])
		trees.append(parent)
	



	# find if child is already a subtree
	childIdx = -1
	for t in range(len(trees)):
		if trees[t].name == data[i,1]:
			childIdx = t
	if childIdx != -1:
		# subtree found, remove subtre and append to other tree
		child = trees.pop(childIdx)
		child.parent = parent
	else:
		# make new child
		child = Node(data[i,1], parent=parent)

		
w = Walker()
		
		
# part 1
total = 0
for node in PreOrderIter(trees[0]):
	nodes = w.walk(trees[0], node)
	total += (len(nodes[2]))
print("Part 1: ", total)	
	

# part 2
you = find(trees[0], lambda node: node.name == "YOU")
san = find(trees[0], lambda node: node.name == "SAN")
nodesToStep = w.walk(you, san)


print("Part 2: Walking from YOU to SAN in %d steps"%(len(nodesToStep[2])+len(nodesToStep[0])-2))

# n = find(trees[0], lambda node: node.name == 'L')	
# print(n)




