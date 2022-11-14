from Map import Map_Obj
"""
Class representation for a node in the map. Initially sets the position, parent, kids, a state for quick searching, 
status and step cost. Also contains methods for setting and getting f, g, and h values.
"""
class Search_Node:
    # Code for initialization
    def __init__(self, pos, parent, step_to_cost):
        self.pos = pos
        self.parent = parent
        self.kids = []
        self.state = self.gen_state(pos)
        self.status = "open"
        self.step_to_cost = step_to_cost

    # While searching for node in a list it uses this method to compare two elements.
    def __eq__(self, othernode):
        return self.state == othernode.state

    # Adds a node to the kids list
    def addKid(self, othernode):
        self.kids.append(othernode)

    # Getters and setters for f, g, and h values. Is not initially set, but calculated when needed.
    def getfvalue(self):
        return self.f

    def setfvalue(self, gval, hval):
        self.f = gval + hval

    def getgvalue(self):
        return self.g

    def setgvalue(self, val):
        self.g = val

    def gethvalue(self):
        return self.h

    def sethvalue(self, val):
        self.h = val

    # Generates state for searching purposes. The state is just at string of the position
    def gen_state(self, pos):
        s = [str(i) for i in pos]
        return "".join(s)

    # A toString method used during development.
    def toString(self):
        return {"pos": self.pos, "f": self.f, "g": self.g, "h": self.h}


# Takes in two nodes and the goal. Main usage is to update the parent and change the f cost of a child node
def attach_and_eval(nodeC, nodeP, goalpos):
    nodeC.parent = nodeP  # Sets the parent of nodeC to be nodeP
    # Calculates and gets f, g and h values of the child node
    nodeC.setgvalue(nodeP.getgvalue() + nodeC.step_to_cost)
    nodeC.sethvalue(eval_h(nodeC.pos, goalpos))
    nodeC.setfvalue(nodeC.getgvalue(), nodeC.gethvalue())

# Iterates over a nodes children and changes their cost to the updated cheaper cost
def propogate_imporvment(node):
    for child in node.kids:
        if node.getgvalue() + eval_h(node.pos, child.pos) < child.getgvalue():
            child.parent = node
            child.setgvalue(node.getgvalue() + child.step_to_cost)
            child.setfvalue(child.getgvalue(), child.gethvalue())
            propogate_imporvment(child)

# Returns the manhattan distance between two positions
def eval_h(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Main function
def Astar(Map, startPos, goalPos):
    openNodes = []  # List containing all discovered nodes, but not yet closed
    closed = []  # List containing all discovered nodes which has been closed
    allnodes = []  # List containing all nodes generated regardless of status

    # Generate the starting node and adds it to openNodes and allnodes
    start_node = Search_Node(startPos, None, 1)
    start_node.setgvalue(0)
    start_node.sethvalue(eval_h(startPos, goalPos))
    start_node.setfvalue(start_node.getgvalue(), start_node.gethvalue())
    openNodes.append(start_node)
    allnodes.append(start_node)
    while len(openNodes) > 0:
        # Removes the first element of openNodes, changes the status to closed and adds it to closed
        current = openNodes.pop(0)
        current.status = "closed"
        closed.append(current)

        # checks if the current node is the goal by the position
        if current.pos == goalPos:
            path = []
            # Loops as long as the current node is not the start node. Adds currentnode to the pathlist
            while current.pos != startPos:
                path.append(current.pos)
                current = current.parent
            return path[::-1]  # Returns the reversed list and containing steps from start to end

        # Generates the children's positions and adds these to a list
        cur_x = current.pos[0]
        cur_y = current.pos[1]
        children_pos = [[cur_x - 1, cur_y], [cur_x + 1, cur_y], [cur_x, cur_y - 1], [cur_x, cur_y + 1]]

        # Iterates through the children
        for childPos in children_pos:
            childpos_cost = Map.get_cell_value(childPos)  # Gets the child's cell value

            if childpos_cost == -1:  # Checks if child is a wall and skips the node if it is
                continue

            # Creates the childnode since it is not a wall
            childnode = Search_Node(childPos, current, childpos_cost)

            # Checks if the childnode exists, if it does change the current child to the previously defined node
            if childnode in allnodes:
                index = allnodes.index(childnode)
                childnode = allnodes[index]
            else:
                allnodes.append(childnode)  # Adds the childnode to all nodes

            current.addKid(childnode)  # Adds the childnode as the kid of the current node

            # If the childnode is new, generate it's path values and add it to the open list
            if childnode not in openNodes and childnode not in closed:
                attach_and_eval(childnode, current, goalPos)
                openNodes.append(childnode)
                openNodes.sort(key=lambda x: x.f)  # Sort the openNodes list based on the f value

            # Checks if the current node is a better parrent to childNode
            elif current.g + eval_h(current.pos, childnode.pos) < childnode.g:
                attach_and_eval(childnode, current, goalPos)
                if childnode in closed:  # If the childnode is already closed, we need to change all its children
                    propogate_imporvment(childnode)

    return None  # The algorithm generated no valid path and returns none


def main():
    map_obj = Map_Obj(task=4)
    start = map_obj.get_start_pos()
    goal = map_obj.get_goal_pos()

    path = Astar(map_obj, start, goal)

    for pos in path:
        map_obj.replace_map_values(pos, 9, goal)

    map_obj.show_map()
    map_obj.print_map(map_obj.get_maps()[0])


main()
