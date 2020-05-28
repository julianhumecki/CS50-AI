import sys
# : is similar to { but it doesn't need to be closed
# if something is indented it indicates it is surrounded by {}
class Node():
    def __init__(self, state, action, goal):
        self.state = state
        self.action = action
        self.goal = goal

class StackFrontier():
    def __init__(self):
        self.frontier = [] #empty list
    #if you want to use the self keyword, it must be an argument to a method
    # in a class    
    def add(self, node):
        self.frontier.append(node)

    #loops through full list and checks if any node's state is 
    #the same as one that exists in the frontier
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    #checks if frontier is empty
    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            #throw an exception
            raise Exception("empty frontier")
        else:
            #indexing a list with -1 it gets you the last item in the list
            removed_node = self.frontier[-1]
            self.frontier.pop()
            return removed_node
    
#inherit all attributes from the StackFrontier
class QueueFrontier(StackFrontier):
    #override the remove function of the StackFrontier
    def remove(self):
        if(self.empty()):
            raise Exception("empty frontier")
        else:
            #remove the first element
            #frontier[1:] //all elements fron index 1 to len - 1 
            removed_node = self.frontier[0]
            self.frontier.pop(0)
            return removed_node


#main
queue = QueueFrontier()
node = Node(state=1,action=0,goal=3)
queue.add(node)
queue.add(node)
print(queue.remove().state)






    
