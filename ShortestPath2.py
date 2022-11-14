from Map import Map_Obj

task = 4
map_obj = Map_Obj(task)
start_pos, goal_pos, end_goal_pos, path_to_map = map_obj.fill_critical_positions(task)
int_map, str_map = map_obj.read_map(path_to_map)

"""
Search Node class for representing tiles in the map, initialized with position and cost"""
class Search_Node():
    # initialization
    def __init__(self, pos, cost):
        self.pos = pos #state
        self.g = arc_cost(start_pos, pos)
        self.h = arc_cost(pos, goal_pos)
        self.f = self.g + self.h
        self.parent = None
        self.kids = []
        self.cost = cost

    # string method for printing, used during development
    def __str__(self):
        return str(self.pos)

    # generates all successors/children to this node
    def gen_successors(self):
        result = []
        children_pos = [[self.pos[0], self.pos[1] + 1], [self.pos[0] + 1, self.pos[1]],
                       [self.pos[0], self.pos[1] - 1], [self.pos[0] - 1, self.pos[1]]]
        for child_pos in children_pos:
            child_cost = map_obj.get_cell_value(child_pos)

            if child_cost > -1: #checks if child is not a wall
                child_node = Search_Node(child_pos, child_cost)

                if self.parent is not None:
                    if self.parent.pos != child_pos:
                        child_node.parent = self
                        result.append(child_node)
                else:
                    child_node.parent = self
                    result.append(child_node)

        return result

# returns the manhattan distance between to points [x,y] and [a,b]
def arc_cost(pos1,pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# updates parent and change the f cost of a child node
# param: Child- and Parent-node
def attach_and_eval(C,P):
    C.parent = P
    C.g = P.g + C.cost
    C.h = arc_cost(C.pos, goal_pos)
    C.f = C.g + C.h

# iterates over a nodes children and updates their cost if a cheaper path is found
def propagate_path_improvements(P):
    for C in P.kids:
        if P.g + arc_cost(P.pos, C.pos) < C.g:
            C.parent = P
            C.g = P.g + C.cost
            C.f = C.g + C.h
            propagate_path_improvements(C)

# A* main function
def best_first_search():
    closed = []
    open = []
    n0 = Search_Node(start_pos, 1)
    open.append(n0)

    #A genda
    while len(open) > 0:

        current = open.pop(0)
        closed.append(current)

        # if current node is a solution, return the node
        if current.pos == end_goal_pos:
            return current, "SUCCESS"

        successors = current.gen_successors()
        # iterate through child nodes
        for s in successors:
            for node in open + closed:
                if node.pos == s.pos:
                    # replaces s with old node in successors list
                    successors = [node if current == s else current for current in successors]
            current.kids.append(s)

            # check if s is in open or closed (could use state instead)
            pos_list = list(map(lambda a: a.pos, open + closed))
            if pos_list.count(s.pos) == 0:
                attach_and_eval(s, current)
                open.append(s)
                open.sort(key=lambda y: y.f) # ascending f value

            elif current.g + arc_cost(current.pos, s.pos) < s.g: # found cheaper path to s

                attach_and_eval(s, current)
                if closed.count(s) > 0:
                    propagate_path_improvements(s)


"""Main"""
solution, status = best_first_search()
print(status)
if solution is not None:
    x = solution
    shortest_path = []
    while x.parent is not None:
        shortest_path.append(x.parent)
        x = x.parent

    # display result
    for node in shortest_path:
        map_obj.replace_map_values(node.pos,9,end_goal_pos)
    map_obj.show_map()
