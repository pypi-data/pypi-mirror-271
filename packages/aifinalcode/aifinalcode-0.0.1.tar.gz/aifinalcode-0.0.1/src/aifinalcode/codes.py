def puzzle():
    code = """
class Solution:
    def solve(self, board):
        def get_paths(self, dict):
            cnt = 0 
            while True:
                current_nodes = [x for x in dict if dict[x] == cnt]
                if len(current_nodes) == 0: 
                    return -1

                for node in current_nodes:
                    next_moves = self.find_next(node)
                    for move in next_moves:
                        if move not in dict:
                            dict[move] = cnt + 1
                        if move == (0, 1, 2, 3, 4, 5, 6, 7, 8):
                            return cnt + 1 
                cnt += 1
        
        def find_next(self, node):
            moves = {
                0: [1, 3],
                1: [0, 2, 4],
                2: [1, 5],
                3: [0, 4, 6],
                4: [1, 3, 5, 7],
                5: [2, 4, 8],
                6: [3, 7],
                7: [4, 6, 8],
                8: [5, 7],
            }

            results = []
            pos_0 = node.index(0)
            for move in moves[pos_0]:
                new_node = list(node)
                new_node[move], new_node[pos_0] = new_node[pos_0], new_node[move]
                results.append(tuple(new_node))
            return results
        
        dict = {}
        flatten = []
        for i in range(len(board)):
            flatten += board[i]
        flatten = tuple(flatten)

        dict[flatten] = 0

        if flatten == (0, 1, 2, 3, 4, 5, 6, 7, 8):
            return 0

        return get_paths(self, dict)

ob = Solution() 
matrix = [
    [3, 1, 2],
    [4, 7, 5],
    [6, 8, 0]
]
print(ob.solve(matrix))
"""
    return code.strip()

def queen():
    code = """
print("Enter the number of queens")
N = int(input())

# Create a chessboard NxN matrix with all elements set to 0
board = [[0] * N for _ in range(N)]

def is_safe(i, j):
    # Checking vertically and horizontally
    for k in range(N):
        if board[i][k] == 1 or board[k][j] == 1:
            return False

    # Checking diagonally
    for k in range(N):
        for l in range(N):
            if (k + l == i + j or k - l == i - j) and board[k][l] == 1:
                return False

    return True

def solve_n_queens(n):
    if n == 0:
        return True

    for i in range(N):
        for j in range(N):
            if not is_safe(i, j):
                continue

            if board[i][j] != 1:
                board[i][j] = 1
            if solve_n_queens(n - 1):
                return True
            board[i][j] = 0

    return False

# Check if a solution exists
if solve_n_queens(N):
    print("Solution exists. Placements of queens:")
    for row in board:
        print(row)
else:
    print("No solution exists.")
"""
    return code.strip()

def bfs():
    code = """
# Python3 Program to print BFS traversal
# from a given source vertex. BFS(int s)
# traverses vertices reachable from s.
from collections import defaultdict

# This class represents a directed graph
# using adjacency list representation
class Graph:

    # Constructor
    def __init__(self):

        # default dictionary to store graph
        self.graph = defaultdict(list)

        # function to add an edge to graph
        # Make a list visited[] to check if a node is already visited or not
    def addEdge(self,u,v):
        self.graph[u].append(v)
        self.visited=[]

    # Function to print a BFS of graph
    def BFS(self, s):

        # Create a queue for BFS
        queue = []

        # Add the source node in

        # visited and enqueue it
        queue.append(s)
        self.visited.append(s)

        while queue:

            # Dequeue a vertex from
            # queue and print it
            s = queue.pop(0)
            print (s, end = " ")

            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then add it
            # in visited and enqueue it
            for i in self.graph[s]:
                if i not in self.visited:
                    queue.append(i)
                    self.visited.append(s)

# Driver code

# Create a graph given in
# the above diagram
g = Graph()
g.addEdge(0, 1)
g.addEdge(0, 2)
g.addEdge(1, 2)
g.addEdge(2, 0)
g.addEdge(2, 3)
g.addEdge(3, 3)

print ("Following is Breadth First Traversal"
                  " (starting from vertex 2)")

g.BFS(2)
"""
    return code.strip()

def dfs():
    code = """
# Python3 program to print DFS traversal
# from a given graph
from collections import defaultdict

# This class represents a directed graph using
# adjacency list representation
class Graph:

    # Constructor
    def __init__(self):

        # Default dictionary to store graph
        self.graph = defaultdict(list)

    # Function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    # A function used by DFS
    def DFSUtil(self, v, visited):

        # Mark the current node as visited
        # and print it
        visited.add(v)
        print(v, end=' ')

        # Recur for all the vertices
        # adjacent to this vertex
        for neighbour in self.graph[v]:
            if neighbour not in visited:
                self.DFSUtil(neighbour, visited)

    # The function to do DFS traversal. It uses
    # recursive DFSUtil()
    def DFS(self, v):

        # Create a set to store visited vertices
        visited = set()

        # Call the recursive helper function
        # to print DFS traversal
        self.DFSUtil(v, visited)

# Driver's code
if __name__ == "__main__":
    g = Graph()

    g.addEdge(0, 1)
    g.addEdge(0, 2)
    g.addEdge(1, 2)
    g.addEdge(2, 0)
    g.addEdge(2, 3)
    g.addEdge(3, 3)

    print("Following is Depth First Traversal (starting from vertex 2)")

    # Function call
    g.DFS(2)
"""
    return code.strip()

def waterjug():
    code = """
from collections import deque

def Solution(a, b, target):
    m = {}
    isSolvable = False
    path = []

    q = deque()

    #Initializing with jugs being empty
    q.append((0, 0))

    while (len(q) > 0):

        # Current state
        u = q.popleft()
        if ((u[0], u[1]) in m):
            continue
        if ((u[0] > a or u[1] > b or
             u[0] < 0 or u[1] < 0)):
            continue
        path.append([u[0], u[1]])

        m[(u[0], u[1])] = 1

        if (u[0] == target or u[1] == target):
            isSolvable = True

        if (u[0] == target):
            if (u[1] != 0):
                path.append([u[0], 0])
        else:
            if (u[0] != 0):
                path.append([0, u[1]])

        sz = len(path)
        for i in range(sz):
            print("(", path[i][0], ",", path[i][1], ")", end=" ")

        break

        q.append([u[0], b]) # Fill Jug2
        q.append([a, u[1]]) # Fill Jug1

        for ap in range(max(a, b) + 1):
            c = u[0] + ap
            d = u[1] - ap

            if (c == a or (d == 0 and d >= 0)):
                q.append([c, d])

            c = u[0] - ap
            d = u[1] + ap

            if ((c == 0 and c >= 0) or d == b):
                q.append([c, d])

        q.append([a, 0])

        q.append([0, b])

    if (not isSolvable):
        print("Solution not possible")

if __name__ == '__main__':

    Jug1, Jug2, target = 4, 3, 2
    print("Path from initial state "
          "to solution state ::")

    Solution(Jug1, Jug2, target)
"""
    return code.strip()

def tictactoe():
    code = """
import numpy as np
import random
from time import sleep

def create_board():
    return np.zeros((3, 3), dtype=int)

def possibilities(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i, j] == 0]

def random_place(board, player):
    selection = possibilities(board)
    if selection:
        current_loc = random.choice(selection)
        board[current_loc] = player
    return board

def check_win(board, player):
    return any(np.all(board == player, axis=0) | # Check rows
               np.all(board == player, axis=1) | # Check columns
               np.all(np.diag(board) == player) | # Check main diagonal
               np.all(np.diag(np.fliplr(board)) == player)) # Check secondary diagonal

def evaluate(board):
    for player in [1, 2]:
        if check_win(board, player):
            return player
    return -1 if np.all(board != 0) else 0

def play_game():
    board, winner, counter = create_board(), 0, 1
    print(board)
    sleep(2)

    while winner == 0:
        for player in [1, 2]:
            board = random_place(board, player)
            print(f"Board after {counter} move")
            print(board)
            sleep(2)
            counter += 1
            winner = evaluate(board)
            if winner != 0:
                break

    return winner

# Driver Code
print("Winner is:", play_game())
"""
    return code.strip()

def astar():
    code = """
def aStarAlgo(start_node, stop_node):
    open_set = {start_node}
    closed_set = set()
    g = {start_node: 0}
    parents = {start_node: start_node}

    while open_set:
        n = min(open_set, key=lambda x: g[x] + heuristic(x))

        if n == stop_node or n not in Graph_nodes:
            break

        open_set.remove(n)
        closed_set.add(n)

        for (m, weight) in get_neighbors(n):
            if m not in open_set and m not in closed_set:
                open_set.add(m)
                parents[m] = n
                g[m] = g[n] + weight
            elif m in open_set and g[m] > g[n] + weight:
                g[m] = g[n] + weight
                parents[m] = n
                if m in closed_set:
                    closed_set.remove(m)
                open_set.add(m)

    if n == stop_node:
        path = []
        while parents[n] != n:
            path.append(n)
            n = parents[n]
        path.append(start_node)
        path.reverse()
        print('Path found: {}'.format(path))
        return path
    else:
        print('Path does not exist!')
        return None

def get_neighbors(v):
    if v in Graph_nodes:
        return Graph_nodes[v]
    else:
        return []

def heuristic(n):
    H_dist = {
        'A': 11, 'B': 6, 'C': 5, 'D': 7, 'E': 3, 'F': 6, 'G': 5,
        'H': 3, 'I': 1, 'J': 0
    }
    return H_dist[n]

Graph_nodes = {
    'A': [('B', 6), ('F', 3)],
    'B': [('A', 6), ('C', 3), ('D', 2)],
    'C': [('B', 3), ('D', 1), ('E', 5)],
    'D': [('B', 2), ('C', 1), ('E', 8)],
    'E': [('C', 5), ('D', 8), ('I', 5), ('J', 5)],
    'F': [('A', 3), ('G', 1), ('H', 7)],
    'G': [('F', 1), ('I', 3)],
    'H': [('F', 7), ('I', 2)],
    'I': [('E', 5), ('G', 3), ('H', 2), ('J', 3)],
}

aStarAlgo('A', 'J')
"""
    return code.strip()

def memoryastar():
    code = """
import heapq

def heuristic(n):
    H_dist = {
        'A': 11, 'B': 6, 'C': 5, 'D': 7, 'E': 3,
        'F': 6, 'G': 5, 'H': 3, 'I': 1, 'J': 0
    }
    return H_dist[n]

def get_neighbors(node):
    if node in Graph_nodes:
        return Graph_nodes[node]
    else:
        return []

def memory_bounded_a_star(start_node, stop_node, memory_limit):
    open_set = []
    closed_set = set()
    g = {start_node: 0}
    parents = {start_node: start_node}

    # f-cost is g(n) + heuristic(n)
    f_cost = {start_node: g[start_node] + heuristic(start_node)}

    heapq.heappush(open_set, (f_cost[start_node], start_node))

    while open_set:
        _, n = heapq.heappop(open_set)

        if n == stop_node or n not in Graph_nodes:
            break

        closed_set.add(n)

        for (m, weight) in get_neighbors(n):
            if m not in closed_set:
                new_g = g[n] + weight

                if m not in g or new_g < g[m]:
                    g[m] = new_g

                    parents[m] = n
                    f_cost[m] = g[m] + heuristic(m)

                    if f_cost[m] <= memory_limit:
                        heapq.heappush(open_set, (f_cost[m], m))

        if n == stop_node:
            path = []
            while parents[n] != n:
                path.append(n)
                n = parents[n]
            path.append(start_node)
            path.reverse()
            print('Path found: {}'.format(path))
            return path
        else:
            print('Path does not exist within the memory limit.')
            return None

# Rest of the code remains the same as the A* algorithm example

Graph_nodes = {
    'A': [('B', 6), ('F', 3)],
    'B': [('A', 6), ('C', 3), ('D', 2)],
    'C': [('B', 3), ('D', 1), ('E', 5)],
    'D': [('B', 2), ('C', 1), ('E', 8)],
    'E': [('C', 5), ('D', 8), ('I', 5), ('J', 5)],
    'F': [('A', 3), ('G', 1), ('H', 7)],
    'G': [('F', 1), ('I', 3)],
    'H': [('F', 7), ('I', 2)],
    'I': [('E', 5), ('G', 3), ('H', 2), ('J', 3)],
}

memory_bounded_a_star('A', 'J', memory_limit=20)
"""
    return code.strip()

def minimax():
    code = """
import math

def minimax(curDepth, nodeIndex, maxTurn, scores, targetDepth):
    # base case: targetDepth reached
    if curDepth == targetDepth:
        return scores[nodeIndex]

    if maxTurn:
        return max(minimax(curDepth + 1, nodeIndex * 2, False,
                           scores, targetDepth),
                   minimax(curDepth + 1, nodeIndex * 2 + 1, False,
                           scores, targetDepth))
    else:
        return min(minimax(curDepth + 1, nodeIndex * 2, True,
                           scores, targetDepth),
                   minimax(curDepth + 1, nodeIndex * 2 + 1, True,
                           scores, targetDepth))

# Driver code
scores = [3, 5, 2, 9, 12, 5, 23, 23]
treeDepth = math.log2(len(scores))

print("The optimal value is:", end=" ")
print(minimax(0, 0, True, scores, treeDepth))
"""
    return code.strip()

def alphabeta():
    code = """
# Initial values of Alpha and Beta
MAX, MIN = 1000, -1000

# Returns optimal value for the current player
# (Initially called for root and maximizer)
def minimax(depth, nodeIndex, maximizingPlayer, values, alpha,
beta):
    # Terminating condition, i.e.,
    # leaf node is reached
    if depth == 3:
        return values[nodeIndex]

    if maximizingPlayer:
        best = MIN
        # Recur for left and right children
        for i in range(0, 2):
            val = minimax(depth + 1, nodeIndex * 2 + i, False,
                          values, alpha, beta)
            best = max(best, val)
            alpha = max(alpha, best) # Alpha Beta Pruning
            if beta <= alpha:
                break
        return best
    else:
        best = MAX
        # Recur for left and right children
        for i in range(0, 2):
            val = minimax(depth + 1, nodeIndex * 2 + i, True,
                          values, alpha, beta)
            best = min(best, val)
            beta = min(beta, best)
            # Alpha Beta Pruning
            if beta <= alpha:
                break

        return best

# Driver Code
if __name__ == "__main__":
    values = [3, 5, 6, 9, 1, 2, 0, -1]
    print("The optimal value is:", minimax(0, 0, True, values, MIN,
                                           MAX))
"""
    return code.strip()

def chess():
    code = """
import chess
import chess.svg
import os
import platform

def display_board(board, filename='chessboard.svg'):
    svg_content = chess.svg.board(board=board)
    with open(filename, 'w') as f:
        f.write(svg_content)
    return filename

def open_svg_file(filename):
    system = platform.system()
    if system == 'Windows':
        os.system("start " + filename)
    elif system == 'Linux':
        os.system("xdg-open " + filename)
    elif system == 'Darwin':
        os.system("open " + filename)

def player_move():
    move_uci = input("Enter your move (in UCI format, e.g., 'e2e4'): ")
    return chess.Move.from_uci(move_uci)

def ai_move(board, depth=2):
    best_move = None
    best_eval = float('-inf')

    for move in board.legal_moves:
        board.push(move)
        eval = -minimax(board, depth-1, False)
        board.pop()

        if eval > best_eval:
            best_eval = eval
            best_move = move

    return best_move

def minimax(board, depth, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, False)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, True)
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval

def evaluate_board(board):
    # Simple evaluation function (counts material)
    evaluation = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            evaluation += piece_value(piece)
    return evaluation

def piece_value(piece):
    if piece.piece_type == chess.PAWN:
        return 1
    elif piece.piece_type == chess.KNIGHT:
        return 3
    elif piece.piece_type == chess.BISHOP:
        return 3
    elif piece.piece_type == chess.ROOK:
        return 5
    elif piece.piece_type == chess.QUEEN:
        return 9
    elif piece.piece_type == chess.KING:
        return 1000
    return 0

def main():
    board = chess.Board()

    while not board.is_game_over():
        svg_file = display_board(board)
        open_svg_file(svg_file)

        # Player move
        move = player_move()
        if move in board.legal_moves:
            board.push(move)
        else:
            print("Invalid move. Try again.")
            continue

        # AI move
        if not board.is_game_over():
            ai_move_result = ai_move(board)
            board.push(ai_move_result)

        svg_file = display_board(board)
        open_svg_file(svg_file)
        print("Game over. Result: {}".format(board.result()))

if __name__ == "__main__":
    main()
"""
    return code.strip()

def sudoku():
    code = """
def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))

def is_valid(board, row, col, num):
    # Check if the number is already in the row or column
    if num in board[row] or num in [board[i][col] for i in range(9)]:
        return False

    # Check if the number is already in the 3x3 grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True

def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def solve_sudoku(board):
    empty_location = find_empty_location(board)

    if not empty_location:
        return True  # Board is filled, puzzle is solved

    row, col = empty_location

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):
                return True  # If the rest of the board can be solved

            # If placing the current number doesn't lead to a solution, backtrack
            board[row][col] = 0

    return False  # No number fits, need to backtrack further

def main():
    # Example Sudoku board (0 represents an empty cell)
    sudoku_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    print("Sudoku Puzzle:")
    print_board(sudoku_board)

    if solve_sudoku(sudoku_board):
        print("\nSolved Sudoku:")
        print_board(sudoku_board)
    else:
        print("\nNo solution exists.")

if __name__ == "__main__":
    main()
"""
    return code.strip()

def constraint():
    code = '''
    #pip install python-constraint
from constraint import Problem, AllDifferentConstraint

def constraint_function(variables, domains, assignments):
    # Define your constraints here
    # Example: variables[0] + variables[1] == variables[2]
    return True

def main():
    # Create a problem instance
    problem = Problem()

    # Add variables to the problem
    problem.addVariable('a', range(1, 5))
    problem.addVariable('b', range(2, 4))
    problem.addVariable('c', range(1, 3))

    # Add a constraint function to the problem
    problem.addConstraint(constraint_function, ['a', 'b', 'c'])

    # Optionally, add an "All Different" constraint
    problem.addConstraint(AllDifferentConstraint(), ['a', 'b', 'c'])

    # Solve the problem
    solutions = problem.getSolutions()

    # Print the solutions
    for solution in solutions:
        print(solution)

if __name__ == "__main__":
    main()
'''
    return code.strip()

def unification():
    code = '''
class Unifier:
    def __init__(self):
        self.substitution = {}

    def unify(self, term1, term2):
        self.substitution = {}
        if self.unify_terms(term1, term2):
            print("Unification successful. Substitution:")
            self.display_substitution()
        else:
            print("Unification failed.")

    def unify_terms(self, term1, term2):
        if term1 == term2:
            return True
        elif self.is_variable(term1):
            return self.unify_variable(term1, term2)
        elif self.is_variable(term2):
            return self.unify_variable(term2, term1)
        elif isinstance(term1, list) and isinstance(term2, list):
            return self.unify_lists(term1, term2)
        elif isinstance(term1, tuple) and isinstance(term2, tuple):
            return self.unify_tuples(term1, term2)
        else:
            return False

    def unify_variable(self, variable, term):
        if variable in self.substitution:
            return self.unify_terms(self.substitution[variable], term)
        elif term in self.substitution:
            return self.unify_terms(variable, self.substitution[term])
        else:
            self.substitution[variable] = term
            return True

    def unify_lists(self, list1, list2):
        if len(list1) != len(list2):
            return False
        for t1, t2 in zip(list1, list2):
            if not self.unify_terms(t1, t2):
                return False
        return True

    def unify_tuples(self, tuple1, tuple2):
        if len(tuple1) != len(tuple2):
            return False
        for t1, t2 in zip(tuple1, tuple2):
            if not self.unify_terms(t1, t2):
                return False
        return True

    def is_variable(self, term):
        return isinstance(term, str) and term.islower()

    def display_substitution(self):
        for variable, value in self.substitution.items():
            print(f"{variable} = {value}")
'''
    return code.strip()

def forwardchaining():
    code = '''
global facts
global is_changed
is_changed = True
facts = [["vertebrate", "duck"], ["flying", "duck"], ["mammal", "cat"]]
def assert_fact(fact):
    global facts
    global is_changed
    if not fact in facts:
        facts += [fact]
        is_changed = True
    while is_changed:
        is_changed = False
        for A1 in facts:
            if A1[0] == "mammal":
                assert_fact(["vertebrate", A1[1]])
            if A1[0] == "vertebrate":
                assert_fact(["animal", A1[1]])
            if A1[0] == "vertebrate" and ["flying", A1[1]] in facts:
                assert_fact(["bird", A1[1]])
    print("Inferred Facts are:")
    print(facts)
'''
    return code.strip()

def backwardchaining():
    code = '''
global facts
global is_changed
is_changed = True
facts = [["vertebrate", "duck"], ["flying", "duck"], ["mammal", "cat"]]

def assert_fact(fact):
    global facts
    global is_changed
    if fact not in facts:
        facts.append(fact)
        is_changed = True

def backward_chain(goal):
    global facts
    global is_changed
    while is_changed:
        is_changed = False
        if goal in [fact[0] for fact in facts]:
            return True
        for A1 in facts:
            if goal == "vertebrate" and A1[0] == "mammal":
                assert_fact(["vertebrate", A1[1]])
            if goal == "animal" and A1[0] == "vertebrate":
                assert_fact(["animal", A1[1]])
            if goal == "bird" and A1[0] == "vertebrate" and ["flying", A1[1]] in facts:
                assert_fact(["bird", A1[1]])
    return False

# Prompt the user for input
goal = input("Enter the goal: ")

try:
    result = backward_chain(goal)
    if result:
        print(f"The goal '{goal}' can be satisfied.")
    else:
        print(f"The goal '{goal}' cannot be satisfied.")
except BackwardChainingError as e:
    print("Backward chaining failed:", e)
    print("Supported facts for the goal are:")
    print(facts)
'''
    return code.strip()

def objectdetection():
    code = '''
Download the MobileNetSSD_deploy.prototxt and
MobileNetSSD_deploy.caffemodel files from the MobileNetSSD GitHub
repository. Place these files in the directory models in your
script.
Run the below command in cmd:
pip install opencv-python

import cv2
net = cv2.dnn.readNetFromCaffe(
    r'D:\2023 - 2024\AI\Lab Manual\models\MobileNetSSD_deploy.prototxt',
    r'D:\2023 - 2024\AI\Lab Manual\models\MobileNetSSD_deploy.caffemodel'
)

def detect_objects(image):
    # Resize the image for processing
    resized = cv2.resize(image, (300, 300))
    blob = cv2.dnn.blobFromImage(resized, 0.007843, (300, 300), 127.5)
    # Set the input to the model
    net.setInput(blob)
    # Run forward pass to get detection results
    detections = net.forward()
    # Loop over the detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        # Filter out weak detections by confidence threshold
        if confidence > 0.2:
            class_id = int(detections[0, 0, i, 1])
            confidence = confidence * 100
            # Get bounding box coordinates
            box = detections[0, 0, i, 3:7] * [image.shape[1], image.shape[0], image.shape[1], image.shape[0]]
            (startX, startY, endX, endY) = box.astype("int")
            # Draw the bounding box and label on the image
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
            label = f"Class {class_id}: {confidence:.2f}%"
            cv2.putText(image, label, (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image

# Load the input image
image_path = r'D:\2023 - 2024\AI\Lab Manual\child.jpeg'
image = cv2.imread(image_path)
# Detect objects in the image
result_image = detect_objects(image)
# Display the result
cv2.imshow('Object Detection', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
    return code.strip()

def classicalplanning():
    code = '''
class Action:
    def __init__(self, name, preconditions, effects):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects

    def __str__(self):
        return self.name

class State:
    def __init__(self, robot_location, destination_reached):
        self.robot_location = robot_location
        self.destination_reached = destination_reached

    def __str__(self):
        return f"Robot Location: {self.robot_location}, Destination Reached: {self.destination_reached}"

class Problem:
    def __init__(self, initial_state, goal_state, actions):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.actions = actions

    def classical_planning(self):
        plan = []
        current_state = self.initial_state

        while not current_state.destination_reached:
            applicable_actions = [action for action in self.actions if action.preconditions(current_state)]

            if not applicable_actions:
                print("No plan found.")
                return None

            chosen_action = applicable_actions[0]
            plan.append(chosen_action)
            current_state = chosen_action.effects(current_state)

        return plan

# Define actions
def move_action(preconditions, effects):
    def action(state):
        if preconditions(state):
            return effects(state)
        else:
            return state
    return action

# Define initial and goal states
initial_state = State(robot_location='RoomA', destination_reached=False)
goal_state = State(robot_location='RoomC', destination_reached=True)

# Define actions
move_to_room_b = Action(
    name='MoveToRoomB',
    preconditions=lambda state: state.robot_location == 'RoomA',
    effects=move_action(
        preconditions=lambda state: state.robot_location == 'RoomA',
        effects=lambda state: State(robot_location='RoomB', destination_reached=False)
    )
)

move_to_room_c = Action(
    name='MoveToRoomC',
    preconditions=lambda state: state.robot_location == 'RoomB',
    effects=move_action(
        preconditions=lambda state: state.robot_location == 'RoomB',
        effects=lambda state: State(robot_location='RoomC', destination_reached=True)
    )
)

# Define the planning problem
problem = Problem(initial_state, goal_state, actions=[move_to_room_b, move_to_room_c])

# Run classical planning algorithm
result_plan = problem.classical_planning()

# Print the resulting plan
if result_plan:
    print("Plan:")
    for action in result_plan:
        print(action)
'''

    return code.strip()

def expertsystem():
    code = """
class SymptomChecker:
    def __init__(self):
        self.symptoms = set()
    
    def add_symptom(self, symptom):
        self.symptoms.add(symptom)
    
    def diagnose(self):
        if 'fever' in self.symptoms and 'cough' in self.symptoms:
            return "You may have a respiratory infection. Common treatments include rest and staying hydrated. If symptoms persist, consult a healthcare professional."
        elif 'headache' in self.symptoms and 'nausea' in self.symptoms:
            return "You might be experiencing migraines. Consider managing stress, maintaining a regular sleep schedule, and keeping a headache diary. Consult a doctor for further evaluation."
        elif 'chest pain' in self.symptoms and 'shortness of breath' in self.symptoms:
            return "You could be at risk of a heart-related issue. Seek immediate medical attention. Avoid strenuous activities and consult a cardiologist for further evaluation."
        elif 'abdominal pain' in self.symptoms and 'vomiting' in self.symptoms:
            return "These symptoms may indicate a gastrointestinal problem. Avoid spicy and fatty foods, and stay hydrated. If symptoms persist, consult a gastroenterologist for proper diagnosis."
        elif 'joint pain' in self.symptoms and 'fatigue' in self.symptoms:
            return "These symptoms may be related to arthritis. Consider gentle exercises, hot/cold therapy, and over-the-counter pain relievers. Consult with a rheumatologist for evaluation."
        elif 'skin rash' in self.symptoms and 'itching' in self.symptoms:
            return "These symptoms may be indicative of an allergic reaction or skin condition. Avoid known allergens and use over-the-counter creams for relief. Consult a dermatologist for further evaluation."
        elif 'frequent urination' in self.symptoms and 'thirst' in self.symptoms:
            return "You may have symptoms of diabetes. Monitor your blood sugar levels, maintain a healthy diet, and stay hydrated. Consult a healthcare professional for a blood sugar test and further guidance."
        elif 'confusion' in self.symptoms and 'memory loss' in self.symptoms:
            return "These symptoms could be signs of neurological issues. Ensure a healthy diet, exercise regularly, and get enough sleep. Consult a neurologist for further evaluation and advice."
        elif 'muscle weakness' in self.symptoms and 'fatigue' in self.symptoms:
            return "Muscle weakness and fatigue may be related to various conditions, including autoimmune disorders. Get adequate rest, maintain a balanced diet, and consult a doctor for proper diagnosis and treatment."
        else:
            return "Not enough information for diagnosis. Please consult a healthcare professional for a thorough evaluation."

if __name__ == "__main__":
    expert_system = SymptomChecker()
    print("Enter symptoms one by one (press Enter after each symptom). Type 'done' when finished.")
    while True:
        symptom = input("Symptom: ").lower()
        if symptom == 'done':
            break
        expert_system.add_symptom(symptom)
    result = expert_system.diagnose()
    print(result)
    """
    return code.strip()

def irisclassification():
    code = """
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_iris

# Load and explore data
iris = load_iris()
data = pd.DataFrame(data=np.c_[iris['data'], iris['target']], columns=iris['feature_names'] + ['target'])
print("Data Preview:")
print(data.head())

# Prepare data
X = data.drop('target', axis=1)
y = data['target']

# Accept input for test size and random state
test_size = float(input("Enter the test size (e.g., 0.2 for 20% test size): "))
random_state = int(input("Enter the random state: "))

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the k-NN classifier
knn_classifier = KNeighborsClassifier(n_neighbors=3)
knn_classifier.fit(X_train_scaled, y_train)

# Make predictions
y_pred = knn_classifier.predict(X_test_scaled)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred, target_names=iris['target_names'])

# Display results
print("\nModel Evaluation:")
print(f"Accuracy: {accuracy:.2f}")
print("\nClassification Report:")
print(classification_rep)
    """
    return code.strip()

def getname():
    return [
        "puzzle",
        "queen",
        "bfs",
        "dfs",
        "waterjug",
        "tictactoe",
        "astar",
        "memoryastar",
        "minimax",
        "alphabeta",
        "chess",
        "sudoku",
        "constraint",
        "unification",
        "forwardchaining",
        "backwardchaining",
        "objectdetection",
        "classicalplanning",
        "expertsystem",
        "irisclassification"
    ]
