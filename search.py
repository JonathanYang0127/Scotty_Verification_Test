# [min nodes, max nodes, max pods per node, number of rounds], (number of nodes, number of pods per node)]
# State: (p_1, p_2, ..., p_n)
# Successor function: next((p_1, p_2, ..., p_n)) =
# 
# External Actions:
# 1. Zero out one of the nodes
# 2. Add a node
# 
# Triggers:
# 1. Add half of the resources from the state that doesn't satisfy the quorum to the state that has the least amount of resources.
#
# Quorum: A node has more pods than half the sum of the pods in all of the nodes.
# Check: Is there a harmful state after the trigger?
#
# Further improvement can be storing the sum 
# Didn't take account of symmetry

from util import Stack

def isUnstableState(state):
    #quorum
    num_of_nodes = state[len(state)-2]
    average = (sum([state[i] for i in range(num_of_nodes)]))//2
    for i in range(num_of_nodes):
        if(state[i]>average):
            return True
    return False

def getSuccessors(state, min_nodes, max_nodes):
    num_of_nodes = state[len(state)-2]
    num_of_rounds = state[len(state)-1]
    external_successors = []
    successors = []

    #External Actions
    #Zero out a node
    for i in range(num_of_nodes):
        if(state[i] != 0):
            external_successors.append([state[k] if k != i else 0 for k in range(len(state)-2)]+[num_of_nodes, num_of_rounds+1])
    
    #Add a node
    if(num_of_nodes < max_nodes):
        external_successors.append([state[k] for k in range(len(state)-2)]+[num_of_nodes+1, num_of_rounds+1])

    #Triggers
    for s in external_successors:
        if(sum([s[i] for i in range(num_of_nodes)])//2 >=1 and  isUnstableState(s)):
            #take half the resources of the maximum and add it to the minimum
            max_resources, min_resources = max(s[:-2]), min(s[:-2])
            max_index, min_index = s.index(max_resources), s.index(min_resources)
            temp = list(s)
            temp[max_index]-=(max_resources-min_resources)//2
            temp[min_index]+=(max_resources-min_resources)//2
            successors.append(temp)
        else:
            successors.append(list(s))
    return successors


def depthFirstSearch(min_nodes, max_nodes, max_pods_per_node, initialState, number_of_rounds):  
    #initialize state
    s = Stack();
    s.push(initialState)
    visited = set()
    while(not s.isEmpty()):
        expand = s.pop()
        if(expand[-1] > number_of_rounds):
            #checks if maximum depth we want to search is exceeded
            continue;
        if(tuple(sort(expand[:-1])) in visited):
            #This is a graph search, so no state needs to be visited more than once
            #Sorting makes algorithm more efficient by taking care of symmetry
            continue;
        visited.add(tuple(sort(expand[:-1])))
        print(expand)
        if(isUnstableState(expand)):
            #Found unstable state. We can terminate the search.
            return False
        for successor in getSuccessors(expand, min_nodes, max_nodes):
            s.push(successor)
    #No unstable states have been found
    return True
             

def createStartState(max_nodes, number_of_nodes, number_of_pods_per_node):
    return [number_of_pods_per_node if i<number_of_nodes else 0 for i in range(max_nodes)]+[number_of_nodes, 0]
    #second to last node is the number of nodes
    #last node is the number of depth

if __name__ == "__main__":
    min_nodes = 2
    max_nodes = 8
    max_pods_per_node = 5
    number_of_rounds = 4
    number_of_nodes = min_nodes
    number_of_pods_per_node = max_pods_per_node
    print(depthFirstSearch(min_nodes, max_nodes, max_pods_per_node, createStartState(max_nodes, number_of_nodes, number_of_pods_per_node), number_of_rounds))
    
