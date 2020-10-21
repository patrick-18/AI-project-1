import numpy as np
import copy

class Node:
    
    def __init__(self, my_state, my_depth, my_previous):
        self.state = my_state
        self.depth = my_depth
        self.previous = my_previous
        self.target = np.array([[1,2,3],[8,0,4],[7,6,5]])
        self.cost = self.f()
    
    ''' 
    规定最终状态为
    1    2    3
    8    0    4
    7    6    5
    其中0代表空格
    '''
    
    def __eq__(self, rhs):
        if rhs != None:
            flag = self.state == rhs.state
            return flag.all()
    
    def __gt__(self, rhs):
        return self.cost > rhs.cost
    
    def __lt__(self, rhs):
        return self.cost < rhs.cost

    def f(self):
        return self.depth + self.P() + 3 * self.S()

    def P(self):
        sum = 0
        for i in range(1,9):
            ind_c = np.argwhere(self.state == i)
            ind_c = ind_c[0]
            ind_t = np.argwhere(self.target == i)
            ind_t = ind_t[0]
            sum = sum + abs(ind_c[0] - ind_t[0]) + abs(ind_c[1] - ind_t[1])
        return sum

    def Q(self):
        sum = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != self.target[i][j]: sum = sum + 1
        return sum

    def S(self):
        if self.state[1][1] == 0: sum = 0
        else: sum = 1
        array = []
        for j in [0, 1, 2]:
            if(self.state[0][j] != 0): array.append(self.state[0][j])
        for i in [1, 2]:
            if(self.state[i][j] != 0): array.append(self.state[i][2])
        for j in [1, 0]:
            if(self.state[i][j] != 0): array.append(self.state[2][j])
        array.append(self.state[1][0])
        
        for i in range(len(array) - 1):
            for j in range(i + 1, len(array)):
                if(array[i] > array[j]): sum = sum + 2

        return sum

    def up(self):
        ind = np.argwhere(self.state == 0)
        if ind[0][0] == 0: return None
        else:
            i = ind[0][0]
            j = ind[0][1]
            next_state = copy.deepcopy(self.state)
            t = next_state[i][j]
            next_state[i][j] = next_state[i-1][j]
            next_state[i-1][j] = t
            nextNode = Node(next_state, self.depth + 1, self)
            return nextNode    

    def down(self):
        ind = np.argwhere(self.state == 0)
        if ind[0][0] == 2: return None
        else:
            i = ind[0][0]
            j = ind[0][1]
            next_state = copy.deepcopy(self.state)
            t = next_state[i][j]
            next_state[i][j] = next_state[i+1][j]
            next_state[i+1][j] = t
            nextNode = Node(next_state, self.depth + 1, self)
            return nextNode  

    def left(self):
        ind = np.argwhere(self.state == 0)
        if ind[0][1] == 0: return None
        else:
            i = ind[0][0]
            j = ind[0][1]
            next_state = copy.deepcopy(self.state)
            t = next_state[i][j]
            next_state[i][j] = next_state[i][j-1]
            next_state[i][j-1] = t
            nextNode = Node(next_state, self.depth + 1, self)
            return nextNode   

    def right(self):
        ind = np.argwhere(self.state == 0)
        if ind[0][1] == 2: return None
        else:
            i = ind[0][0]
            j = ind[0][1]
            next_state = copy.deepcopy(self.state)
            t = next_state[i][j]
            next_state[i][j] = next_state[i][j+1]
            next_state[i][j+1] = t
            nextNode = Node(next_state, self.depth + 1, self)
            return nextNode  
