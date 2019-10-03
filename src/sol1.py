import random
import copy


## A Dictionary that Describes to given Graph
Graph = {1:{2:'O', 5:'O', 8:'O'}, 2:{1:'O', 3:'O', 10:'O'}, 3:{2:'O', 4:'O', 12:'O'},
         4:{3:'O', 5:'O', 14:'O'}, 5:{1:'O', 4:'O', 6:'O'}, 6:{5:'O', 7:'O', 15:'O'},
         7:{6:'O', 8:'O', 17:'O'}, 8:{1:'O', 7:'O', 9:'O'}, 9:{8:'O', 10:'O', 18:'O'},
         10:{2:'O', 9:'O', 11:'O'}, 11:{10:'O', 12:'O', 19:'O'}, 12:{3:'O', 11:'O', 13:'O'},
         13:{12:'O', 14:'O', 20:'O'}, 14:{4:'O', 13:'O', 15:'O'}, 15:{6:'O', 14:'O', 16:'O'},
         16:{15:'O', 17:'O', 20:'O'}, 17:{7:'O', 16:'O', 18:'O'}, 18:{9:'O', 17:'O', 19:'O'},
         19:{11:'O', 18:'O', 20:'O'}, 20:{13:'O', 16:'O', 19:'O'}}

def searchPath(graph, start, end, path=[]):
    path = path + [start]
    if start not in graph:
        return False
    if start == end:
        return True
    for i in graph[start]:
        if i not in path:
            if searchPath(graph, i, end, path):
                return True
    return False

def MonteCarlo(M, P, Graph, T1 ,T2 ,T3):
    for p in P:
        print('\t'+format(p, '.2f'), end='\t|\t')
        for m in M:
            r = 0
            for _ in range(m):
                copyOfGraph = copy.deepcopy(Graph)
                MC_graph = {}
                # iterate over all the edges and set their state
                for v1 in range(1, 21):
                    for v2 in copyOfGraph[v1]:
                        if copyOfGraph[v1][v2] == 'O':
                            # random number
                            x = random.uniform(0, 1)
                            if float(x) <= float(p):
                                copyOfGraph[v1][v2] = 'UP' #each edge is represented twice
                                copyOfGraph[v2][v1] = 'UP'
                                if v1 not in MC_graph:
                                    MC_graph[v1] = []
                                MC_graph[v1].append(v2)
                                if v2 not in MC_graph:
                                    MC_graph[v2] = []
                                MC_graph[v2].append(v1)
                            else:
                                copyOfGraph[v1][v2] = 'DOWN'
                                copyOfGraph[v2][v1] = 'DOWN'
                         
        
                # check if one vertex is connected to the other two, if it is so the system is up
                if (searchPath(MC_graph, T3, T1) and searchPath(MC_graph, T3, T2))  or (
                    searchPath(MC_graph, T2, T1) and searchPath(MC_graph, T2, T3)) or (
                    searchPath(MC_graph, T1, T2) and searchPath(MC_graph, T1, T3)):
                        r = r + 1
                    
            print(format(r/m, '.4f'), end='\t|\t')
            if m == 10000:
                print()           
     
     
def main():
    P = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]
    M = [1000, 10000]
    T1 = 10
    T2 = 14
    T3 = 20
    print("Terminals: T1 = {}, T2 = {}, T3 = {}".format(T1,T2,T3))
    print('\tP\t|\tM=1000\t|\tM=10000')
    print('-'*50)
    MonteCarlo(M, P, Graph, T1, T2, T3)     
     
     
if __name__ == "__main__":
    main()
     
