import random
import copy
import math


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

def MonteCarloDynamic(M, alive, t, Graph, T1 ,T2 ,T3):
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
            
    return (len(alive[t])/M)
                
def MonteCarloStatic(M, Graph, T1 ,T2 ,T3, part):
        r = 0
        for _ in range(M):
            MC_graph = {}
            copyOfGraph = copy.deepcopy(Graph)
            # iterate over all the edges and set their state
            for v1 in range(1, 21):
                for v2 in copyOfGraph[v1]:
                    if copyOfGraph[v1][v2] == 'O':
                        # random number
                        x = random.uniform(0, 1)
                        if float(x) <= float(math.e**(-0.5)):
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
        if part == "part1":      
            print("R(t) = {}".format(r/M, '.4f'))
        else:
            return float(r/M)
            

def main():
    M = 10000
    T1 = 10
    T2 = 14
    T3 = 20
    print("Terminals: T1 = {}, T2 = {}, T3 = {}".format(T1,T2,T3))
    "-------------Part 1-------------"
    print("\n\t\tpart 1")
    print('-'*40)
    MonteCarloStatic(M, Graph, T1, T2, T3,"part1")
    "-------------Part 2-------------"
    print("\n\t\tpart 2")
    print('-'*40)
    times = [0.1, 0.3, 0.5, 0.7, 0.9]
    alive = {0.1:[], 0.3:[], 0.5:[], 0.7:[], 0.9:[]}
    print('\n\ttime\t|\tstatic\t|\tdynamic')
    print('-'*50)
    dynamicRe = {}
    staticRe = {}
    for t in times:
        dynamic = float(MonteCarloDynamic(M, alive, t, Graph, T1, T2, T3))
        dynamicRe[t] = []
        dynamicRe[t].append((math.sqrt(1 - dynamic))/(math.sqrt(dynamic) * math.sqrt(M)))
        static = float(MonteCarloStatic(M, Graph, T1, T2, T3,""))
        staticRe[t] = []
        staticRe[t].append((math.sqrt(1 - static))/(math.sqrt(static) * math.sqrt(M)))
        print("\t{}\t|\t{}\t|\t{}".format(t, static, dynamic, ".1f", ".4f", ".4f"))
    "-------------Part 3-------------"
    print("\n\t\tpart 3")
    print('-'*40)
    print('\n\ttime\t|\t\tstatic\t\t|\t\tdynamic')
    print('-'*80)
    for t in times:
        print("\t{}\t|\t{}\t|\t{}".format(t, staticRe[t][0], dynamicRe[t][0], ".1f", ".4f", ".4f"))
    
if __name__ == "__main__":
    main()