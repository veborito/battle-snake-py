# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import math
import queue
import time
from a_star_utils import Node, make_graph, h, path, a_star, start_node, end_node

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "veborito",  # TODO: Your Battlesnake Username
        "color": "#00cc00",  # TODO: Choose color
        "head": "snail",  # TODO: Choose head
        "tail": "mlh-gene",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

# fonctions utiles

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if  my_head["x"] == board_width - 1:
        is_move_safe["right"] = False
        if my_head["y"] == board_height - 1:
            is_move_safe["up"] = False
        elif my_head["y"] == 0:
            is_move_safe["down"] = False
    elif my_head["x"] == 0:
        is_move_safe["left"] = False
        if my_head["y"] == board_height - 1:
            is_move_safe["up"] = False
        elif my_head["y"] == 0:
            is_move_safe["down"] = False
    elif my_head["y"] == board_height - 1:
        is_move_safe["up"] = False
    elif my_head["y"] == 0:
        is_move_safe["down"] = False


    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']
    my_body_set = set()
    for el in my_body:
        my_body_set.add((el["x"], el["y"]))
    if (my_head["x"] + 1, my_head["y"]) in my_body_set:
        is_move_safe["right"] = False 
    if (my_head["x"] - 1, my_head["y"]) in my_body_set:
        is_move_safe["left"] = False
    if (my_head["x"], my_head["y"] + 1) in my_body_set:
        is_move_safe["up"] = False
    if (my_head["x"], my_head["y"] - 1) in my_body_set:
        is_move_safe["down"] = False
    

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    snakes = game_state['board']['snakes']
    ennemies_curr_pos = set()
    for snake in snakes :
        if snake['name'] != game_state['you']['name']:
            for position in snake['body']:
                ennemies_curr_pos.add((position['x'], position['y']))
    
    if (my_head["x"] + 1, my_head["y"]) in ennemies_curr_pos:
        is_move_safe["right"] = False 
    if (my_head["x"] - 1, my_head["y"]) in ennemies_curr_pos:
        is_move_safe["left"] = False
    if (my_head["x"], my_head["y"] + 1) in ennemies_curr_pos:
        is_move_safe["up"] = False
    if (my_head["x"], my_head["y"] - 1) in ennemies_curr_pos:
        is_move_safe["down"] = False

    # ---------------------- CREATION D'UNE MATRICE REPRESENTANT L'ETAT DE LA PARTIE ------------------------
     
    matrice = [[' ' for i in range(board_width)] 
               for i in  range(board_height)]   
    my_head_x = my_head["x"]
    my_head_y = my_head["y"]
    matrice[(board_height - 1) - my_head_y][my_head_x] = 'B'  # pour avoir la position au bon endroit dans la matrice
    for snake in snakes :
        if snake['name'] == game_state['you']['name']:
            for position in snake['body'][1:]:
                matrice[(board_height - 1) - position['y']][position['x']] = '$'
    for snake in snakes :
        if snake['name'] != game_state['you']['name']:
            ennemy_head = snake["body"][0]
            matrice[(board_height - 1) - ennemy_head["y"]][ennemy_head["x"]] = 'V'
            for position in snake['body'][1:]:
                matrice[(board_height - 1) - position['y']][position['x']] = '#'
                

    # ---------------------------------- NEAREST FOOD -------------------------
    
    food =  game_state['board']['food']
    nearest_cherry = math.inf
    nearest_cherry_coord = (0,0)
    for cherry in food:
        distance_cherry = (abs(my_head_x - cherry['x']) + abs(my_head_y - cherry['y']))
        if nearest_cherry > distance_cherry:
            nearest_cherry_coord = (cherry['x'], cherry['y'])
            nearest_cherry = distance_cherry
    
    matrice[(board_height - 1) - nearest_cherry_coord[1]][nearest_cherry_coord[0]] = 'O'

    # ------------------- A STAR ALGO IMPLEMENTATION ---------------------
    
    graph = make_graph(matrice)
    start = start_node(graph)
    end = end_node(graph)
    if start != False and end != False:
        for row in graph:
            for node in row:
                node.update_neighbors(graph)

        a_star_res = a_star(graph, start, end)
        if a_star_res != False:
            path_list = path(a_star_res, end)
            path_list.reverse()
            n_matrice = [[ node.state for node in row] for row in graph]
            for row in n_matrice:
                print (row)
            moves = []
            for i in range(len(path_list) - 1):
                if path_list[i][0] > path_list[i + 1][0]:
                    moves.append("up")
                elif path_list[i][0] < path_list[i + 1][0]:
                    moves.append("down")
                elif path_list[i][1] > path_list[i + 1][1]:
                    moves.append("left")
                elif path_list[i][1] < path_list[i + 1][1]:
                    moves.append("right")
                    
            next_move = moves[0]
            print(f"MOVE {game_state['turn']}: {next_move}")
            return {"move": next_move}
    
    
    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}


    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)
    
    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
