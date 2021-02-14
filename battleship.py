# MODULES
import random
import numpy as np
import time


def inp_proof_int(prompt, range1, range2):
    """CHECKS INPUT FOR CORRECT PARAMETERS, SPECIFICALLY FOR INTEGERS"""
    while True:
        try:
            while True:
                var = int(input(prompt))
                if var in range(range1, range2):
                    break
                else:
                    print("Please enter a number from " + str(range1) + " to " + str(range2 - 1))
            return var
        except ValueError:
            print("Please enter a number from " + str(range1) + " to " + str(range2 - 1))


def inp_proof_str(prompt, list):
    """CHECKS INPUT FOR CORRECT PARAMETERS, SPECIFICALLY FOR STRINGS"""
    while True:
        try:
            while True:
                var = input(prompt)
                if var in list:
                    break
                else:
                    print("Please enter one of the following: ", end="")
                    for i in list:
                        print(i + " ", end="")
                    print()
            return var
        except ValueError:
            print("Please enter one of the following: ", end="")
            for i in list:
                print(i + " ", end="")
            print()


def board_interface(board):
    """CONVERTS ARRAY INTO A BOARD INTERFACE AND PRINT"""
    letter = ["A  ", "B  ", "C  ", "D  ", "E  ", "F  ", "G  ", "H  ", "I  ", "J  "]
    for i in range(len(board)):
        print(letter[i] + "  ", end="")
        for j in range(len(board[i])):
            if board[i][j] == 999:
                print("::" + " ", end="")
            elif board[i][j] == 888:
                print("CC" + " ", end="")
            elif board[i][j] == 777:
                print("XX" + " ", end="")
            elif board[i][j] == 666:
                print("SS" + " ", end="")
            elif board[i][j] == 0:
                print("  " + " ", end="")
            else:
                print(2 * str(board[i][j]) + " ", end="")
        print()
    print("\n     1  2  3  4  5  6  7  8  9  10")


def ship_selection_player(board, prompt):
    """MAIN SELECTION MECHANISM FOR THE PLAYER
            - PROMPTS USER FOR INPUTS
            - CONVERTS INPUTS TO VALUES USED BY OTHER FUNCTIONS"""
    print("------------------------------------------------------------------------------------------------------------"
          "----------\n"
          "\033[1m" + "It's time to set up your ship, " + "\033[4m" + prompt + "\033[1m" + ". Please keep in mind:" +
          "\033[0m" + "\n"
          " - Ships will be places based on their orientation\n"
          " - Horizontal ships will be placed relative to the left-most square\n"
          " - Vertical ships will be placed relative to the right-most square\n"
          " - Ships can not extend beyond the border and can not cross-over other ships")
    input("\nPress enter to continue")
    while True:
        ship_remaining = length_list[:]
        ship_used = []
        while len(ship_remaining) != 0:  # LOOPS WHILE THERE ARE STILL SHIPS TO BE PLACED
            print("----------------------------------------------------------------------------------------------------"
                  "------------------\n"
                  "\033[1m" + "These are the sizes of your remaining ships: " + "\033[0m")
            for i in range(len(ship_remaining)):
                print(" - " + str(ship_remaining[i]))
            print("\n" + "\033[1m" + "This is your current board: " + "\033[0m" + "\n")
            board_interface(board)
            while True:
                size = inp_proof_int("\n" + "Enter in the size of the ship you would like to place: ", 1, length + 1)
                if size in ship_remaining:
                    break
                else:
                    print("Invalid size")
            orientation = inp_proof_str("Choose the orientation for placing your ship (V = Vertical, H = Horizontal): ",
                                        ["V", "v", "H", "h"])
            if orientation == "V" or orientation == "v":
                orientation = 1
            elif orientation == "H" or orientation == "h":
                orientation = 0
            check = ship_check(size, orientation, board, 1)  # FUNCTION TESTS IF SHIP PLACEMENT IS POSSIBLE
            if check > 0:
                print("Please try again")
                continue
            else:
                pass
            remember = np.copy(board)
            ship_place(size, orientation, remember)
            print()
            board_interface(remember)
            check = inp_proof_str("\n" + "Is your ship positioned correctly (Y/N): ", ["Y", "y", "N", "n"])
            if check == "Y" or check == "y":
                ship_place(size, orientation, board)
                ship_used += [size]
                ship_remaining.pop(ship_remaining.index(size))
            if check == "N" or check == "n":
                print("Please try again")
        print("--------------------------------------------------------------------------------------------------------"
              "--------------\n"
              "\033[1m" + "All of your ships have been placed, here is your current board: " + "\033[0m" + "\n")
        board_interface(board)
        check = inp_proof_str("\nAre you happy with the positions of your ships? (Y/N, N to start over): ",
                              ["Y", "y", "N", "n"])
        if check == "Y" or check == "y":
            break
        elif check == "N" or check == "n":
            board = np.full((10, 10), 999, dtype=int)
            continue


def ship_selection_ai(board):
    """MAIN SELECTION MECHANISM USED BY THE AI"""
    ship_remaining = length_list[:]
    ship_used = []
    while len(ship_remaining) > 0:
        while True:
            size = random.randint(1, length)
            if size in ship_remaining:
                break
        orientation = random.randint(0, 1)
        check = ship_check(size, orientation, board, 0)
        if check == 0:
            ship_place(size, orientation, board)
            ship_used += [size]
            ship_remaining.pop(ship_remaining.index(size))


def ship_check(size, orientation, board, mode):
    """FUNCTION TO CHECK THE PLACEMENT OF SHIPS THE BOARD
            - ORIENTATION: 0 = HORIZONTAL  1 = VERTICAL
            - CHECKS FOR BORDER
            - CHECKS FOR CROSS-OVER ISSUES
            - MODE: 1 = PLAYER  0 = AI"""
    global x
    global y
    y_conv_u = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    y_conv_l = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    if mode == 1:
        x = inp_proof_int("Enter in the X value of where you want to place your ship (1 - 10): ", 1, 11) - 1
        y = inp_proof_str("Enter in the Y value of where you want to place your ship (A - J): ", y_conv_u + y_conv_l)
        if y.islower():
            y = y_conv_l.index(y)
        elif y.isupper():
            y = y_conv_u.index(y)
    elif mode == 0:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
    global check
    check = 0
    pos = 0
    check_coords = []
    for i in range(size):  # CHECKS FOR INTERSECTING SHIPS
        if orientation == 0:
            if not(-1 < y < 10) or not(-1 < (x + pos) < 10):
                check += 1
                print("\033[1m" + "Your ship intersected a border" + "\033[0m") if mode == 1 else print(end="")
                return check
            else:
                if 0 < board[y][x + pos] < 10:
                    check += 1
                    print("\033[1m" + "Your ship intersected another ship" + "\033[0m") if mode == 1 else print(end="")
                    check_coords += [[y, x + pos]]
        elif orientation == 1:
            if not(-1 < (y + pos) < 10) or not(-1 < x < 10):
                check += 1
                print("\033[1m" + "Your ship intersected a border" + "\033[0m") if mode == 1 else print(end="")
                return check
            else:
                if 0 < board[y + pos][x] < 10:
                    check += 1
                    print("\033[1m" + "Your ship intersected another ship" + "\033[0m") if mode == 1 else print(end="")
                    check_coords += [[y + pos, x]]
        pos += 1
    return check


def ship_place(size, orientation, board):
    """FUNCTION TO PLACE THE SHIPS ONTO THE BOARD"""
    pos = 0
    for i in range(size):
        if orientation == 0:
            board[y][x + pos] = size
        elif orientation == 1:
            board[y + pos][x] = size
        pos += 1


def shoot(mode, board, hidden, display, remain, ai_shoot):
    """FUNCTION TO EXECUTE A SINGLE TURN IN THE GAME"""
    while True:
        print("\nEnemy's board: \n") if mode == 1 else print(end="")
        board_interface(board) if mode == 1 else print(end="")
        y_conv_u = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        y_conv_l = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
        if mode == 1:  # PLAYER
            x = inp_proof_int("\nEnter in the X value of where you want to shoot (1 - 10): ", 1, 11) - 1
            y = inp_proof_str("Enter in the Y value of where you want to shoot (A - J): ", y_conv_u + y_conv_l)
            print()
            if y.islower():
                y = y_conv_l.index(y)
            elif y.isupper():
                y = y_conv_u.index(y)
        elif mode == 0:  # AI
            if ai_shoot is True:
                x = moves[-1][1]
                y = moves[-1][0]
            elif ai_shoot is False:
                x = moves[0][1]
                y = moves[0][0]
                moves.pop(0)
        if board[y][x] == 999:
            rememember = np.copy(board)
            rememember[y][x] = 888
            board_interface(rememember) if mode == 1 else print(end="")
            check = inp_proof_str("\nConfirmation (Y/N): ", ["Y", "y", "N", "n"]) if mode == 1 else "Y"
            if check == "Y" or check == "y":
                if hidden[y][x] != 999:
                    board[y][x] = 777
                    display[y][x] = 777
                elif hidden[y][x] == 999:
                    board[y][x] = 0
                    display[y][x] = 0
                if mode == 0:
                    print("\nPicking Coordinates") if ai_shoot is False else print(end="")
                    time.sleep(1) if ai_shoot is False else print(end="")
                print("\nResult : Enemy's board\n") if mode == 1 else print(end="")
                board_interface(board) if mode == 1 else print(end="")
                for i in remain:
                    count = np.count_nonzero(display == i)
                    if count == 0:
                        remain.remove(i)
                        for y in range(len(display)):
                            for x in range(len(display[y])):
                                if hidden[y][x] == i:
                                    display[y][x] = 666
                                    board[y][x] = 666
                        print("\nThe ship has been sunk") if ai_shoot is False else print(end="")
                        if mode == 0:
                            input("Press enter to continue") if mode == 1 else print(end="")
                            return True
                input("Press enter to continue") if mode == 1 else print(end="")
                break
            else:
                print("Please try again")
        else:
            print("\033[1m" + "The square you picked has already been revealed" + "\033[0m" + "\n"
                  "Please try again")


def ai_hunt(board, moves, ai_loop):
    """IF THERE ARE HITS ON THE BOARD, THE AI WILL SHOOT AROUND THE SQUARE UNTIL A SUNKEN ANNOUNCEMENT"""
    for i in range(len(board)):
        for j in range(len(board[i])):  # FIND THE HIT SPOT
            if board[i][j] == 777:
                y = i
                x = j
    while True:
        pos = 1
        while True:
            if -1 < (x - pos) < 10:
                if board[y][x - pos] == 999:
                    moves += [[y, x - pos]]
                    a = shoot(0, board_a_ai, hidden_a, hidden_a_ai_display, ship_remaining_ai, True)
                    board_interface(board) if ai_loop is True else print(end="")
                    time.sleep(0.5) if ai_loop is True else print(end="")
                    if a is True:
                        return
                    if board[y][x - pos] == 0:
                        break
                    elif board[y][x - pos] == 777:
                        pos += 1
                        continue
                break
            break
        pos = 1
        while True:
            if -1 < (x + pos) < 10:
                if board[y][x + pos] == 999:
                    moves += [[y, x + pos]]
                    a = shoot(0, board_a_ai, hidden_a, hidden_a_ai_display, ship_remaining_ai, True)
                    board_interface(board) if ai_loop is True else print(end="")
                    time.sleep(0.5) if ai_loop is True else print(end="")
                    if a is True:
                        return
                    if board[y][x + pos] == 0:
                        break
                    elif board[y][x + pos] == 777:
                        pos += 1
                        continue
                break
            break
        pos = 1
        while True:
            if -1 < (y - pos) < 10:
                if board[y - pos][x] == 999:
                    moves += [[y - pos, x]]
                    a = shoot(0, board_a_ai, hidden_a, hidden_a_ai_display, ship_remaining_ai, True)
                    board_interface(board) if ai_loop is True else print(end="")
                    time.sleep(0.5) if ai_loop is True else print(end="")
                    if a is True:
                        return
                    if board[y - pos][x] == 0:
                        break
                    elif board[y - pos][x] == 777:
                        pos += 1
                        continue
                break
            break
        pos = 1
        while True:
            if -1 < (y + pos) < 10:
                if board[y + pos][x] == 999:
                    moves += [[y + pos, x]]
                    a = shoot(0, board_a_ai, hidden_a, hidden_a_ai_display, ship_remaining_ai, True)
                    board_interface(board) if ai_loop is True else print(end="")
                    time.sleep(0.5) if ai_loop is True else print(end="")
                    if a is True:
                        return
                    if board[y + pos][x] == 0:
                        break
                    elif board[y + pos][x] == 777:
                        pos += 1
                        continue
                break
            break
        break


def ai_search(ship_remaining, board):
    """GENERATE A PROBABILITY BOARD SHOWING MOST LIKELY SQUARES FOR SHIP TO BE ON"""
    prob = np.full((10, 10), 0)
    for y in range(len(prob)):  # CALCULATES PROBABILITY
        for x in range(len(prob[y])):
            for i in ship_remaining:
                if board[y][x] == 999:

                    check = True  # CHECK HORIZONTALLY
                    for j in range(i):
                        if not -1 < (x + j) < 10:
                            check = False
                            break
                        if board[y][x + j] != 999:
                            check = False
                    if check is True:  # ADD HORIZONTALLY
                        for j in range(i):
                            prob[y][x + j] += 1

                    check = True  # CHECK VERTICALLY
                    for j in range(i):
                        if not -1 < (y - j) < 10:
                            check = False
                            break
                        if board[y - j][x] != 999:
                            check = False
                    if check is True:  # ADD VERTICALLY
                        for j in range(i):
                            prob[y - j][x] += 1

    caniddates = []  # PICKS A SQUARE WITH HIGHEST PROBABILITY
    max_coords = np.unravel_index(np.argmax(prob), prob.shape)
    max_val = prob[max_coords[0]][max_coords[1]]
    max_count = 0
    for i in range(len(prob)):
        for j in range(len(prob[i])):
            if prob[i][j] == max_val:
                max_count += 1
    for i in range(max_count):
        max_coords = np.unravel_index(np.argmax(prob), prob.shape)
        caniddates += [[max_coords[0], max_coords[1]]]
        prob[max_coords[0]][max_coords[1]] = -1

    final_coords = caniddates[random.randint(0, len(caniddates) - 1)]
    return [final_coords[0], final_coords[1]]


# GAME INTRODUCTION AND INSTRUCTIONS
print("----------------------------------------------------------------------------------------------------------------"
      "------\n" +
      "\033[1m" + "Let's play BattleShips" + "\033[0m")
length = inp_proof_int("How many ships would you like to play with? (1 - 9)", 1, 10)
print("Select your mode (1 or 2):\n"
      "  1) Player VS AI\n"
      "  2) Player VS Player")
mode = inp_proof_int("", 1, 3)
length_list = list(range(1, 1 + length))
win_condition = sum(length_list)
print("----------------------------------------------------------------------------------------------------------------"
      "------\n"
      "\033[1m" + "While I am setting up the boards, here are some basic information: " + "\033[0m" + "\n"
      "Instructions :\n"
      " - The board is arranged in a 10 by 10 grid\n"
      " - Each player will start out with 7 ships and will each arrange them on their respective boards\n"
      " - Once the game has start, each player will take turn firing shots at the other's board\n"
      " - Mark every shot as either a hit on an enemy ship, or a miss in the water\n"
      " - The game ends once either player loses all of their ships\n"
      "Legend :\n"
      " - :: marks a square as empty\n"
      " -    marks a square as a miss\n"
      " - XX marks a square as a hit\n"
      " - CC marks a square for confirmation")

input("\nPress enter to continue")

# PREPARING THE BOARDS
board_a = np.full((10, 10), 999, dtype=int)  # THE BOARD THAT PLAYER B/AI WILL BE SHOOTING AT
board_b = np.full((10, 10), 999, dtype=int)  # THE BOARD THAT PLAYER A WILL BE SHOOTING AT
hidden_a = np.full((10, 10), 999, dtype=int)  # THE BOARD THAT PLAYER A WILL PUT THEIR SHIPS ON
hidden_b = np.full((10, 10), 999, dtype=int)  # THE BOARD THAT PLAYER B/AI WILL PUT THEIR SHIPS ON

# MAIN SHIP PLACEMENT MECHANISM
print("-------------------------------------------------------------------------------------------------"
      "---------------------")
if mode == 1:  # PLAYER PLACEMENTS
    player_a = input("Enter your name: ")
    ship_selection_player(hidden_a, player_a)
    print("------------------------------------------------------------------------------------------------------------"
          "----------\n"
          "AI's Turn")
    for i in range(4):
        time.sleep(1)
        print("...")
    time.sleep(1)
    ship_selection_ai(hidden_b)
elif mode == 2:
    player_a = input("Enter player A's name:")
    player_b = input("Enter player B's name:")
    ship_selection_player(hidden_a, player_a)
    ship_selection_player(hidden_b, player_b)


# CHEAT SHEET
print("------------------------------------------------------------------------------------------------------------"
      "----------")
cheat = inp_proof_str("Do you want to enable cheat sheet? (Y/N): ", ["Y", "y", "N", "n"])

# BOARD DISPLAY
hidden_a_display = np.copy(hidden_a)
hidden_b_display = np.copy(hidden_b)

# AI STUFF
moves = []
board_a_ai = np.copy(board_a)
hidden_a_ai_display = np.copy(hidden_a)
ship_remaining_ai = length_list[:]

# AI LOOP
ai_moves = inp_proof_str("Would you like to watch the AI's moveset? (Y/N): ", ["Y", "y", "N", "n"])
print()
win = np.count_nonzero(board_a_ai == 666)
while win != win_condition:
    count = np.count_nonzero(board_a_ai == 777)
    while count == 0:
        coords = ai_search(ship_remaining_ai, board_a_ai)
        moves += [[coords[0], coords[1]]]
        shoot(0, board_a_ai, hidden_a, hidden_a_ai_display, ship_remaining_ai, True)
        win = np.count_nonzero(board_a_ai == 666)
        if win == win_condition:
            break
        board_interface(board_a_ai) if ai_moves in ["Y", "y"] else print(end="")
        time.sleep(0.5) if ai_moves in ["Y", "y"] else print(end="")
        win = np.count_nonzero(board_a_ai == 666)
        if win == win_condition:
            break
        count = np.count_nonzero(board_a_ai == 777)
    win = np.count_nonzero(board_a_ai == 666)
    if win == win_condition:
        break
    ai_hunt(board_a_ai, moves, True if ai_moves in ["Y", "y"] else False)
    win = np.count_nonzero(board_a_ai == 666)
    if win == win_condition:
        break
print("\nAI's moveset: ", moves) if ai_moves in ["Y", "y"] else print(end="")
input("\nPress enter to continue") if ai_moves in ["Y", "y"] else print(end="")

# OTHER VARIABLES
ship_remain_a = length_list[:]
ship_remain_b = length_list[:]

# MAIN GAME LOOP
print("----------------------------------------------------------------------------------------------------------------"
      "------\n"
      "Before starting, I will flip a coin to see who goes first:")
for i in range(2):
    time.sleep(1)
    print("...")
coin_flip = random.randint(0, 9)
first = "A" if coin_flip > 4 else "B"  # TEMP
if mode == 2:  # PLAYER VS PLAYER
    print("Player A gets to go first") if first == "A" else print("Player B gets to go first")
    input("Press enter to continue")
    win_b = np.count_nonzero(board_b == 666)
    win_a = np.count_nonzero(board_a == 666)
    while win_a != win_condition or win_b != win_condition:
        if first == "A":
            print("----------------------------------------------------------------------------------------------------"
                  "------------------\n"
                  "\033[1m" + player_a + "'s Turn \n" + "\033[0m")
            if cheat == "Y" or cheat == "y":
                print("Cheat Sheet Enabled:")
                board_interface(hidden_b)
            print("\nYour board\n")
            board_interface(hidden_a_display)
            shoot(1, board_b, hidden_b, hidden_b_display, ship_remain_b, False)
            win_b = np.count_nonzero(board_b == 666)
            if win_b == win_condition:
                break
            print("----------------------------------------------------------------------------------------------------"
                  "------------------\n"
                  "\033[1m" + player_b + "'s Turn" + "\033[0m")
            if cheat == "Y" or cheat == "y":
                print("Cheat Sheet Enabled:")
                board_interface(hidden_a)
            print("\nYour board\n")
            board_interface(hidden_b_display)
            shoot(1, board_a, hidden_a, hidden_a_display, ship_remain_a, False)
            win_a = np.count_nonzero(board_a == 666)
            if win_a == win_condition:
                break
        elif first == "B":
            print("----------------------------------------------------------------------------------------------------"
                  "------------------\n"
                  "\033[1m" + player_b + "'s Turn" + "\033[0m")
            if cheat == "Y" or cheat == "y":
                print("Cheat Sheet Enabled:")
                board_interface(hidden_a)
            print("\nYour board\n")
            board_interface(hidden_b_display)
            shoot(1, board_a, hidden_a, hidden_a_display, ship_remain_a, False)
            win_a = np.count_nonzero(board_a == 666)
            if win_a == win_condition:
                break
            print("----------------------------------------------------------------------------------------------------"
                  "------------------\n"
                  "\033[1m" + player_a + "'s Turn \n" + "\033[0m")
            if cheat == "Y" or cheat == "y":
                print("Cheat Sheet Enabled:")
                board_interface(hidden_b)
            print("\nYour board\n")
            board_interface(hidden_a_display)
            shoot(1, board_b, hidden_b, hidden_b_display, ship_remain_b, False)
            win_b = np.count_nonzero(board_b == 666)
            if win_b == win_condition:
                break
    if win_b == win_condition:
        print("----------------------------------------------------------------------------------------------------"
              "------------------\n"
              "\033[4m" + player_a + "\033[1m" + " have sunk all of " + "\033[4m" + player_b + "\033[1m" + "'s ships\n"
              + "Congratulations!\n" +
              "\033[4m" + player_a + "\033[1m" + " have won")
        exit()
    elif win_a == win_condition:
        print("----------------------------------------------------------------------------------------------------"
              "------------------\n"
              "\033[4m" + player_b + "\033[1m" + " have sunk all of " + "\033[4m" + player_a + "\033[1m" + "'s ships\n"
              + "Congratulations!\n" +
              "\033[4m" + player_b + "\033[1m" + " have won")
        exit()

elif mode == 1:  # PLAYER VS AI
    ai_hits = []
    print("You get to go first") if first == "A" else print("I get to go first")
    input("Press enter to continue")
    win_b = np.count_nonzero(board_b == 666)
    win_a = np.count_nonzero(board_a == 666)
    while win_a != win_condition or win_b != win_condition:  # WIN CONDITION
        if first == "A":
            print("----------------------------------------------------------------------------------------------------"
                  "------------------\n"
                  "\033[1m" + "Your turn \n" + "\033[0m")
            if cheat == "Y" or cheat == "y":
                print("Cheat Sheet Enabled:\n")
                board_interface(hidden_b)
            print("\nYour board\n")
            board_interface(hidden_a_display)
            shoot(1, board_b, hidden_b, hidden_b_display, ship_remain_b, False)
            win_b = np.count_nonzero(board_b == 666)
            if win_b == win_condition:
                break
            print("----------------------------------------------------------------------------------------------------"
                  "------------------\n"
                  "\033[1m" + "My turn \n" + "\033[0m")
            shoot(0, board_a, hidden_a, hidden_a_display, ship_remain_a, False)
            win_a = np.count_nonzero(board_a == 666)
            if win_a == win_condition:
                break
        elif first == "B":
            print("----------------------------------------------------------------------------------------------------"
                  "------------------\n"
                  "\033[1m" + "My Turn \n" + "\033[0m")
            shoot(0, board_a, hidden_a, hidden_a_display, ship_remain_a, False)
            win_a = np.count_nonzero(board_a == 666)
            if win_a == win_condition:
                break
            print("----------------------------------------------------------------------------------------------------"
                  "------------------\n"
                  "\033[1m" + "Your turn \n" + "\033[0m")
            if cheat == "Y" or cheat == "y":
                print("Cheat Sheet Enabled:\n")
                board_interface(hidden_b)
            print("\nYour board\n")
            board_interface(hidden_a_display)
            shoot(1, board_b, hidden_b, hidden_b_display, ship_remain_b, False)
            win_b = np.count_nonzero(board_b == 666)
            if win_b == win_condition:
                break
    if win_b == win_condition:
        print("----------------------------------------------------------------------------------------------------"
              "------------------\n"
              "\033[1m" + "You have sunk all of my ships\n" +
              "You have won\n"
              "Congratulations, " + "\033[4m" + player_a + "\033[1m" + "!")
        exit()
    elif win_a == win_condition:
        print("----------------------------------------------------------------------------------------------------"
              "------------------\n"
              "\033[1m" + "I have sunk all of your ships\n" +
              "I have won\n"
              "Yay me!")
        exit()
