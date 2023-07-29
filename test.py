import random
import copy

class Sudoku:
    board = []
    board2 = []
    solved_board = []
    
    def __init__(self,level):
        self.board = [
            [0 ,0 ,0  ,0 ,0 ,0  ,0 ,0 ,0],
            [0 ,0 ,0  ,0 ,0 ,0  ,0 ,0 ,0],
            [0 ,0 ,0  ,0 ,0 ,0  ,0 ,0 ,0],

            [0 ,0 ,0  ,0 ,0 ,0  ,0 ,0 ,0],
            [0 ,0 ,0  ,0 ,0 ,0  ,0 ,0 ,0],
            [0 ,0 ,0  ,0 ,0 ,0  ,0 ,0 ,0],

            [0 ,0 ,0  ,0 ,0 ,0  ,0 ,0 ,0],
            [0 ,0 ,0  ,0 ,0 ,0  ,0 ,0 ,0],
            [0 ,0 ,0  ,0 ,0 ,0  ,0 ,0 ,0]
        ]
        self.board2 = [
            [0 ,0 ,0  ,0 ,0 ,0  ,0 ,0 ,0],
            [0 ,0 ,0  ,0 ,0 ,0  ,0 ,0 ,0],
            [0 ,0 ,0  ,0 ,0 ,0  ,0 ,0 ,0],

            [0 ,0 ,0  ,0 ,0 ,0  ,0 ,0 ,0],
            [0 ,0 ,0  ,0 ,0 ,0  ,0 ,0 ,0],
            [0 ,0 ,0  ,0 ,0 ,0  ,0 ,0 ,0],

            [0 ,0 ,0  ,0 ,0 ,0  ,0 ,0 ,0],
            [0 ,0 ,0  ,0 ,0 ,0  ,0 ,0 ,0],
            [0 ,0 ,0  ,0 ,0 ,0  ,0 ,0 ,0]
        ]
        self.full_board()
        self.solved_board = copy.deepcopy(self.board)
        k = 0
        if level == "Beginner":
            k = 43
        elif level == "Medium":
            k = 50
        else:
            k = 55
        #while True:
        count = 0
        while count <= k:  
            i = random.randint(0,8)
            j = random.randint(0,8)
            if self.board[i][j] != 0:
                self.board[i][j] = 0
                count += 1        
        if self.check_unique():
            print("Right")
        else:
            print("Wrong")

    def insert(self, x, y, value):
        self.board[x][y] = value

    def printBoard(self):
        for row in range(9):
            for col in range(9):  
                print(self.board[row][col], end = " ")     
                if col % 3 == 2:
                    print("  ", end = "")             
            print("")
            if row % 3 == 2:
                print("")

    def is_valid(self, board, i, j, value):
        for index in range(9):
            if board[index][j] == value or board[i][index] == value:
                return False
        row = i // 3 * 3
        col = j // 3 * 3
        for m in range(row, row + 3):
            for n in range(col, col + 3):
                if board[m][n] == value:
                    return False
        return True

    def solve_board(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for k in range(1, 10):
                        if self.is_valid(board, i, j, k):
                            board[i][j] = k
                            if self.solve_board(board):
                                return True
                            board[i][j] = 0
                    return False
        return True

    def solve_board2(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for k in range(9, 0, -1):
                        if self.is_valid(board, i, j, k):
                            board[i][j] = k
                            if self.solve_board(board):
                                return True
                            board[i][j] = 0
                    return False
        return True

    def full_board(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    for k in range(1, 10):
                        k = random.randint(1,9)
                        if self.is_valid(self.board, i, j, k):
                            self.board[i][j] = k
                            if self.full_board():
                                return True
                            self.board[i][j] = 0
                    return False
        return True
        
    #check if the pluzze has only solution 
    def check_unique(self):
        board1 = copy.deepcopy(self.board)
        board2 = copy.deepcopy(self.board)
        self.solve_board(board1)
        self.solve_board2(board2)
        return board1 == board2

    def is_legal_move(self, i, j, k):
        return self.solved_board[i][j] == k
#printBoard(create_board())
