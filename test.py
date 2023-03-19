import queue

matrice = [
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', 'O', ' ', ' ', ' ', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', 'V'],
[' ', 'O', ' ', ' ', ' ', ' ', ' ', ' ', '$', ' ', ' '],
[' ', ' ', ' ', 'O', ' ', ' ', ' ', ' ', '$', '$', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
]


def valid_move(board, my_head , moves):
    i = (len(board) - 1) - my_head[1]
    j = my_head[0]
    
    for move in moves:
        if move == "L":
            j -= 1
        elif move == "R":
            j += 1
        elif move == "U":
            i -= 1
        elif move == "D":
            i += 1   
        if not (0 <= i < len(board) and 0 <= j < len(board[0])):
            return False
        elif (board[i][j] == "V" or board[i][j] == "#" or board[i][j] == "$" or board[i][j] == "B"):
            return False
    return True


def find_end(board, my_head, moves):
    i = (len(board) - 1) - my_head[1]
    j = my_head[0]
    
    for move in moves:
        if move == "L":
            j -= 1
        elif move == "R":
            j += 1
        elif move == "U":
            i -= 1
        elif move == "D":
            i += 1   
    if (board[i][j] == "O"):
        print("Found: " + moves)
        add_path(matrice, [8, 9], moves)
        return True
    return False


def add_path(board, my_head, moves):
    i = (len(board) - 1) - my_head[1]
    j = my_head[0]
    
    for move in moves:
        if move == "L":
            j -= 1
        elif move == "R":
            j += 1
        elif move == "U":
            i -= 1
        elif move == "D":
            i += 1   
        board[i][j] = '+'
    return


moves = queue.Queue()
moves.put("")
add = ""

while not find_end(matrice, [8, 9], add):
    add = moves.get()
    for i in ["L", "R", "U", "D"]:
        put = add + i
        if valid_move(matrice, [8, 9], put):
            print(put)
            moves.put(put)

print("------------------------------------\n")
for row in matrice:
    print(row)
