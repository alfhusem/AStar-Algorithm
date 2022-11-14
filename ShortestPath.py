from Map import Map_Obj
task = 2
map_obj = Map_Obj(task)
start_pos, goal_pos, end_goal_pos, path_to_map = map_obj.fill_critical_positions(task)
print(start_pos, goal_pos, end_goal_pos, path_to_map)
int_map, str_map = map_obj.read_map(path_to_map)

class Search_Node():
    def __init__(self, pos):
        self.pos = pos #state
        self.g = arc_cost(start_pos, pos)
        self.h = arc_cost(pos, goal_pos)
        self.f = self.g + self.h
        self.parent = None
        self.kids = []

    def __str__(self):
        return str(self.pos)

    def gen_successors(self):
        result = []
        n1 = Search_Node([self.pos[0], self.pos[1] + 1])
        n2 = Search_Node([self.pos[0] + 1, self.pos[1]])
        n3 = Search_Node([self.pos[0], self.pos[1] - 1])
        n4 = Search_Node([self.pos[0] - 1, self.pos[1]])
        succ = [n1, n2, n3, n4]
        for node in succ:
            if map_obj.get_cell_value(node.pos) == 1:
                if self.parent is not None:
                    if self.parent.pos != node.pos:
                        node.parent = self
                        result.append(node)
                else:
                    node.parent = self
                    result.append(node)


        return result

#return distance between to points [x,y] and [a,b]
def arc_cost(pos1,pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

#param: Child- and Parent-node
def attach_and_eval(C,P):
    C.parent = P
    C.g = P.g + arc_cost(P.pos, C.pos)
    C.h = arc_cost(C.pos, goal_pos)
    C.f = C.g + C.h

def propagate_path_improvements(P):
    for C in P.kids:
        if P.g + arc_cost(P.pos, C.pos) < C.g:
            C.parent = P
            C.g = P.g + arc_cost(P.pos, C.pos)
            C.f = C.g + C.h
            propagate_path_improvements(C)

def best_first_search():
    closed = []
    open = []
    n0 = Search_Node(start_pos)
    open.append(n0)
    solution = False

    #Agenda
    while len(open) > 0:

        current = open.pop(0)
        closed.append(current)
        #if x is solution, return x SUCCEED
        if current.pos == end_goal_pos:
            return current, "SUCCESS"

        successors = current.gen_successors()
        for s in successors:
            for node in open + closed:
                if node.pos == s.pos:
                    #replaces s with old node in successors list
                    successors = [node if x == s else x for x in successors]
            current.kids.append(s)

            #check if s is in open or closed (could use state instead)
            pos_list = list(map(lambda a: a.pos, open + closed))
            if pos_list.count(s.pos) == 0:
                attach_and_eval(s, current)
                open.append(s)
                open.sort(key=lambda y: y.f) #ascending f value

            if current.g + arc_cost(current.pos, s.pos) < s.g: #found cheaper path to s
                print("HEY")
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

    result = ""
    for node in shortest_path:
        map_obj.replace_map_values(node.pos,9,end_goal_pos)
        result += str(node) + " "
    print(result)
    map_obj.show_map()
    #map_obj.print_map(int_map)