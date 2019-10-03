import random
import copy
import math
import matplotlib.pyplot as plt


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

def tableprint(alive, M):
    print ('\t{}\t|\t{}'.format('time','system life'))
    print('-' * 40)
    for i,j in alive.items():
        R=len(j)/M
        print ('\t{}\t \t{}'.format(i,R))
    time=[i for i,j in alive.items()]
    system_life=[len(j)/M for i,j in alive.items()]
    plt.plot(time,system_life,color='red',marker="+")
    plt.title("2.A graph")
    plt.xlabel("time")
    plt.ylabel("system life")
    plt.show()

def MonteCarlo(M, alive, times, Graph, T1 ,T2 ,T3):
    for t in times:
        for _ in range(M):
            MC_graph = {}
            copyOfGraph = copy.deepcopy(Graph)
            # iterate over all the edges and set their state
            for v1 in range(1, 21):
                for v2 in copyOfGraph[v1]:
                    if copyOfGraph[v1][v2] == 'O':
                        # random number
                        x = random.uniform(0,1)
                        copyOfGraph[v1][v2] = -1 * math.log(x)
                        copyOfGraph[v2][v1] = -1 * math.log(x)
                        if float(copyOfGraph[v1][v2]) > float(t):
                            if v1 not in MC_graph:
                                MC_graph[v1] = []
                            MC_graph[v1].append(v2)
                            if v2 not in MC_graph:
                                MC_graph[v2] = []
                            MC_graph[v2].append(v1)
            system_life = 0
            # check if one vertex is connected to the other two, if it is so the system is up
            if (searchPath(MC_graph, T3, T1) and searchPath(MC_graph, T3, T2)):
                system_life = 1 - (1 - math.e**((-t**3) * (copyOfGraph[20][13] * copyOfGraph[20][16] * copyOfGraph[20][19]))) 
            elif (searchPath(MC_graph, T2, T1) and searchPath(MC_graph, T2, T3)):
                system_life = 1 - (1 - math.e**((-t**3) * (copyOfGraph[14][4] * copyOfGraph[14][13] * copyOfGraph[14][15])))
            elif (searchPath(MC_graph, T1, T2) and searchPath(MC_graph, T1, T3)):
                system_life = 1 - (1 - math.e**((-t**3) * (copyOfGraph[10][2] * copyOfGraph[10][9] * copyOfGraph[10][11])))
                                               
            if (float(system_life) > float(t)):
                alive[t].append(system_life)
            
    tableprint(alive, M)
    
def main():
    times = [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1]
    alive={0:[],0.05:[],0.1:[],0.15:[],0.2:[],0.25:[],0.3:[],0.35:[],0.4:[],0.45:[],0.5:[],0.55:[],0.6:[],0.65:[],0.7:[],0.75:[],0.8:[],0.85:[],0.9:[],0.95:[],1:[]}
    M = 10000
    T1 = 10
    T2 = 14
    T3 = 20
    print("Terminals: T1 = {}, T2 = {}, T3 = {}".format(T1,T2,T3))
    MonteCarlo(M, alive, times, Graph, T1, T2, T3)     


if __name__ == "__main__":
    main()