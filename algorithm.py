import node
import copy
import numpy as np
import heapq

class Algorithm:
    
    def __init__(self):
        self.start = []
        self.openList = []
        self.closedList = []
        self.solution = []
        self.startNode = None
        self.haveSolution = False
        self.targetNode = node.Node(np.array([[1,2,3],[8,0,4],[7,6,5]]), 0, None)


    def get_start(self, array: list):
        for i in range(3):
            self.start.append([])
            for j in range(3):
                self.start[i].append(array[3 * i + j])
        self.startNode = node.Node(np.array(self.start), 0, None)
    
    def have_solution(self):
        if self.startNode == None: self.haveSolution = False
        else:
            array = []
            state = self.startNode.state
            for j in [0, 1, 2]:
                if(state[0][j] != 0): array.append(state[0][j])
            for i in [1, 2]:
                if(state[i][j] != 0): array.append(state[i][2])
            for j in [1, 0]:
                if(state[i][j] != 0): array.append(state[2][j])
            for j in [0, 1]:
                if(state[1][j] != 0): array.append(state[1][j])
            inverse = 0
            for i in range(len(array) - 1):
                for j in range(i + 1, len(array)):
                    if(array[i] > array[j]): inverse = inverse + 1
            self.haveSolution = (inverse % 2 == 0)
    
    def search(self):
        if self.startNode == None: self.solution = []
        elif not self.haveSolution: self.solution = []
        else:
            sum = 0
            heapq.heapify(self.openList)
            heapq.heappush(self.openList, self.startNode)
            while self.openList != []:
                self.bestNode = heapq.heappop(self.openList)
                sum += 1
                # print(sum)
                self.closedList.append(self.bestNode)
                if(self.targetNode == self.bestNode):
                    break
                else:
                    successor = []
                    successor.append(self.bestNode.up())
                    successor.append(self.bestNode.down())
                    successor.append(self.bestNode.left())
                    successor.append(self.bestNode.right())
                for i in range(4):
                    if successor[i] == None: continue
                    elif successor[i] == self.bestNode.previous: continue
                    else:
                        # heapq.heappush(self.openList, successor[i])
                        '''
                        ind = find(self.openList, successor[i])
                        if ind != -1:
                            if successor[i].depth < self.openList[ind].depth:
                                self.openList.pop(ind)
                                heapq.heappush(self.openList, successor[i])
                            else: continue
                        elif find(self.closedList, successor[i]) != -1:
                            ind = find(self.closedList, successor[i])
                            if successor[i].depth < self.closedList[ind].depth:
                                self.closedList.pop(ind)
                            else: continue
                        else:
                            heapq.heappush(self.openList, successor[i])
                        '''
                        
                        if successor[i] in self.openList:
                            old = self.openList[self.openList.index(successor[i])]
                            if successor[i].depth < old.depth:
                                self.openList.remove(old)
                                heapq.heappush(self.openList, successor[i])
                            else: continue
                        elif successor[i] in self.closedList:
                            old = self.closedList[self.closedList.index(successor[i])]
                            if successor[i].depth < old.depth:
                                self.closedList.remove(old)
                            else: continue
                        else: 
                            heapq.heappush(self.openList, successor[i])
                            

            current = self.bestNode
            while current.previous != None:
                self.solution.append(current.state.flatten().tolist())
                current = current.previous
            self.solution.reverse()


def find(mylist, node):
    for i in range(len(mylist)):
        if mylist[i] == node: return i
    return -1



