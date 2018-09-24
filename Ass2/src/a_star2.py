from a_star import Bfs


# Inherits A* implementation from task 1
class Bfs2(Bfs):

    # Maps from value to cost, A and B are assumed a cost of 0
    def map_to_cost(self, c):
        dict = {
            "w": 100,
            "m": 50,
            "f": 10,
            "g": 5,
            "r": 1,
            "A": 0,
            "B": 0
        }
        return dict[c]

    # Override to include correct cost
    def generate_successors(self, current):
        x = current.state[0]
        y = current.state[1]
        succs = []
        # Add successors from left, right, up and/or down, omit if at edge of board
        if x > 0:
            c = self.board[x - 1][y]
            succs.append(self.generate_node([x - 1, y], current, self.map_to_cost(c)))
        if x < len(self.board) - 1:
            c = self.board[x + 1][y]
            succs.append(self.generate_node([x + 1, y], current, self.map_to_cost(c)))
        if y > 0:
            c = self.board[x][y - 1]
            succs.append(self.generate_node([x, y - 1], current, self.map_to_cost(c)))
        if y < len(self.board[0]) - 1:
            c = self.board[x][y + 1]
            succs.append(self.generate_node([x, y + 1], current, self.map_to_cost(c)))

        return succs

def read_board(path):
    f = open(path, "r")
    lines = f.readlines()
    f.close()
    for i, line in enumerate(lines):
        lines[i] = line.strip("\n")
    return lines

def run(path):
    board = read_board(path)
    bfs = Bfs2(board)
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

# Uncomment for running program

for board in ["../boards/board-2-1.txt",
              "../boards/board-2-2.txt",
              "../boards/board-2-3.txt",
              "../boards/board-2-4.txt"]:
    run(board)
    print("")

