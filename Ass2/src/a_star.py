from heapq import heappush, heappop

class Node:
    def __init__(self, state, parent, cost):
        self.state = tuple(state)
        self.parent = parent
        self.f_score = float('inf')
        self.g_score = float('inf')
        self.cost = cost
        self.kids = []

    def __gt__(self, node2):
        return self.f_score > node2.f_score

    def __eq__(self, other):
        return self.state == other.state if other != None else False

    # For debugging
    def __str__(self):
        return '-'.join(map(str, self.state)) + " f_score=" + str(self.f_score)

    def __repr__(self):
        return '-'.join(map(str, self.state)) + " f_score=" + str(self.f_score) + " g_score=" + str(self.g_score) + " cost=" + str(self.cost)


class Bfs:
    def __init__(self, board):
        self.board = board

    # Returns position in board of character c
    def find_state(self, c):
        return [[i1, i2] for i1, lst in enumerate(self.board) for i2, elem in enumerate(lst) if c == elem][0]

    # Manhatten distance
    def heuristic_function(self, node):
        return abs(node.state[0] - self.goal_state[0]) + abs(node.state[1] - self.goal_state[1])

    def reconstruct_path(self, current):
        path = []
        while current != None:
            path.append(current)
            current = current.parent
        return path

    def generate_node(self, state, parent, cost):
        node = Node(state, parent, cost)
        node.g_score = parent.g_score + self.arc_cost(parent, node)
        node.f_score = node.g_score + self.heuristic_function(node)
        return node

    def generate_successors(self, node):
        x = node.state[0]
        y = node.state[1]
        succs = []
        # Add successors from left, right, up and/or down, omit if at edge of board or the node is an obstacle
        if x > 0 and self.board[x - 1][y] != "#":
            succs.append(self.generate_node([x - 1, y], node, 1))
        if x < len(self.board) - 1 and self.board[x + 1][y] != "#":
            succs.append(self.generate_node([x + 1, y], node, 1))
        if y > 0 and self.board[x][y - 1] != "#":
            succs.append(self.generate_node([x, y - 1], node, 1))
        if y < len(self.board[0]) - 1 and self.board[x][y + 1] != "#":
            succs.append(self.generate_node([x, y + 1], node, 1))

        return succs

    # Change parent of child
    def attach_and_eval(self, child, parent):
        child.parent = parent
        child.g_score = parent.g_score + self.arc_cost(parent, child)
        child.f_score = child.g_score + self.heuristic_function(child)

    # Cost to go from x to y, assumes x is parent of y.
    # Parameter x not really neccessary. For a more general implementation of the algorithm,
    # one would check the path from x to y and then calculate the distance.
    def arc_cost(self, x, y):
        return y.cost

    def propagate_path_improvements(self, node):
        for c in node.kids:
            if node.g_score + self.arc_cost(node, c) < c.g_score:
                self.attach_and_eval(c, node)
                self.propagate_path_improvements(c)

    def best_first_search(self):
        closed_set = []
        open_set = []

        # Define goal state
        self.goal_state = tuple(self.find_state("B"))

        # Define start node
        start = Node(self.find_state("A"), None, 1)
        start.g_score = 0
        start.f_score = self.heuristic_function(start)

        # Add start node to the open set and save its state for later lookup
        heappush(open_set, start)
        states = {}
        states[start.state] = start

        while open_set:
            current = heappop(open_set)
            closed_set.append(current)
            states[current.state] = current

            if current.state == self.goal_state:
                return self.reconstruct_path(current)

            succs = self.generate_successors(current)
            for succ in succs:
                if succ.state in states:
                    succ = states[succ.state]
                current.kids.append(succ)

                if succ not in open_set and succ not in closed_set:
                    self.attach_and_eval(succ, current)
                    heappush(open_set, succ)
                elif current.g_score + self.arc_cost(current, succ) < succ.g_score:
                    self.attach_and_eval(succ, current)
                    if succ in closed_set:
                        self.propagate_path_improvements(succ)
        return None  # Algorithm could not find shortest path

def read_board(path):
    f = open(path, "r")
    lines = f.readlines()
    f.close()
    for i, line in enumerate(lines):
        lines[i] = line.strip("\n")
    return lines

def run(path):
    board = read_board(path)
    bfs = Bfs(board)
    res = bfs.best_first_search()
    if res == None:
        print("Could not find a path from A to B")
        return

    # Add solution to board
    for node in res:
        if board[node.state[0]][node.state[1]] in ['A', 'B']:
            continue
        myList = list(board[node.state[0]])
        myList[node.state[1]] = 'o'
        myString = ''.join(myList)
        board[node.state[0]] = myString

    # Print result
    print(path)
    for line in board:
        print(line)

# Running task 1
for board in ["../boards/board-1-1.txt",
              "../boards/board-1-2.txt",
              "../boards/board-1-3.txt",
              "../boards/board-1-4.txt"]:
    run(board)
    print("")
