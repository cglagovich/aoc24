'''
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn

aq,cg,yn
aq,vc,wq
co,de,ka
co,de,ta
co,ka,ta
de,ka,ta
kh,qp,ub
qp,td,wh
tb,vc,wq
tc,td,wh
td,wh,yn
ub,vc,wq

What are we looking for?
small circles of computers X, Y, Z, where X-Y, Y-Z, X-Z have connections

How does a human solve this?
Build the graph and look for loops of length 3
How do you find loops of length 3?
For each node (which starts with a 't'), traverse its neighbors up to depth 3 until you find the root node again
DFS recursive

My solution double counts certain things.
- For each set, I count each way you can get from start to start, giving 2x as many sets.
- If a set contains multiple t* nodes, I count each t* node separately

Solve this by returning the paths that form 3-circles and then uniquifying them

I solved part1 in a weird way, since 3-way FCN is a special case -- it forms a ring.

For part2, I need to find the largest FCN in the graph.
How would you brute force this? 
Calculate the largest FCN for each start node
For each start node S:
    The largest FCN containing S is the FCN which has S, and all neighbors NS of S, where all NS are connected to S and other NS.
    You could not add any other neighbor of S which is still connected with the others
    
This could be tricky, because you need to remove neighbors of S from the graph if they disconnect the FCN

A fully connected graph of n nodes is a graph where each node N is of order (n-1).
Algorithm:
Build a graph of S and all neighbors of S.
While not all nodes have degree (size(graph) - 1), remove the node with the lowest degree.

'''
def dfs(nodedict, startname, curname, depth, curpath, allpaths):
    if depth == 0:
        if curname == startname:
            allpaths.add('-'.join(sorted(curpath)))
        return
    
    for nextname in node_dict[curname].neighbors:
        dfs(nodedict, startname, nextname, depth-1, curpath + [nextname], allpaths)

def nsets(nodedict, startname, depth=3):
    allpaths = set()

    dfs(nodedict, startname, startname, depth, curpath=[], allpaths=allpaths)
    return allpaths

def solvep1(node_dict):
    filtered_names = list(filter(lambda x: x.startswith('t'), [k for k in node_dict.keys()]))
    allsets = set()
    for name in filtered_names:
        thissets = nsets(node_dict, name)
        allsets |= thissets

    return len(allsets)


def fcn(node_dict, start_node):
    def order(nodeset, node_dict):
        '''
        Returns a sorted list of [(order0, name0), ...] for each
        node in nodeset
        '''
        orders = []
        for n in nodeset:
            thisorder = len(nodeset & set(node_dict[n].neighbors))
            orders.append((thisorder, n))
        return sorted(orders, key=lambda x: x[0])

    # Before pruning, fcnnodes are all neighbors of the start node
    fcnnodes = set([start_node])
    fcnnodes |= set(node_dict[start_node].neighbors)

    orders = order(fcnnodes, node_dict)
    while 1:
        orders = order(fcnnodes, node_dict)
        if all(o[0] == (len(orders) - 1) for o in orders):
            break
        lowest_order = orders[0][1]
        fcnnodes.remove(lowest_order)

    return fcnnodes

def solvep2(node_dict):
    '''
    Return the sorted, joined nodes which constitute the largest
    fully-connected network in the graph.
    '''
    max_fcn = set()
    for name in node_dict.keys():
        fcn_nodes = fcn(node_dict, name)
        if len(fcn_nodes) > len(max_fcn):
            max_fcn = fcn_nodes

    return ','.join(sorted(max_fcn))


from collections import namedtuple
Node = namedtuple('Node', ['name', 'neighbors'])

import sys
fname = sys.argv[1]
edges = [e.strip() for e in open(fname).readlines()]
node_name_set = set([a for edge in edges for a in edge.split('-')])
node_dict = {name: Node(name=name, neighbors=[]) for name in node_name_set}

# build graph
for edge in edges:
    s0, s1 = edge.split('-')
    node_dict[s0].neighbors.append(s1)
    node_dict[s1].neighbors.append(s0)


print('part 1:', solvep1(node_dict))
print('part 2:', solvep2(node_dict))