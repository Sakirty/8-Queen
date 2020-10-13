from queens import queen #import the queen class
import random
import numpy # for board
from math import exp,log
import random
from statistics import mean

def create_board():
    start_baord = [] 
    for i in range(8):
        start_baord.append(queen(random.randint(0,7),i))
    return start_baord

def print_state(the_queens):
    board = numpy.zeros(shape=(8,8))
        #board[1] = [2,3]
    for items in the_queens:
        board[items.get_row()][items.get_col()] = 1
    print(board)

def find_heu(the_queens): # the queens -> list, return total conflicts of curr map
    heu = 0 # reset the heu
    for i in range(len(the_queens)):
        for j in range(i+1,len(the_queens)):
            if the_queens[i].conflict_queens(the_queens[j]):
                heu+=1
    return heu

######SA########
global steps
steps = 0
global heuristic
heuristic = 0
#######FC#######
global steps_fc
steps_fc = 0
global heuristic_fc
heuristic_fc = 0
#######SA#######
global steps_sa
steps_sa = 0
global heuristic_sa
heuristic_sa = 0
global t_sa
t_sa = 0
global big_t
big_t = 1
##############
# hillclimb_sa
# choose the best state of its neighbors
def hillclimb_sa(currboard): # pick greatest neighbor
    global steps
    global heuristic
    nextboard, tempboard = [], []
    curr_heu = find_heu(currboard)
    best_heu = curr_heu # set as best heu now
    for i in range(len(currboard)):
        nextboard.append(currboard[i])
        tempboard.append(currboard[i])
    for i in range(len(currboard)):
        if i>0:
            tempboard[i-1] = queen(currboard[i-1].get_row(),currboard[i-1].get_col())
        tempboard[i] = queen(0,tempboard[i].get_col())
        for j in range(len(currboard)):
            temp_heu = find_heu(tempboard)
            if(temp_heu<best_heu):
                best_heu = temp_heu
                for k in range(len(currboard)):
                    nextboard[k] = queen(tempboard[k].get_row(),tempboard[k].get_col())
            if(tempboard[i].get_row()!=(len(currboard)-1)):
                tempboard[i].move()
    # check if we have a better board
    if(best_heu == curr_heu):
        # no progress, restart, ++counters
        steps = 0
        nextboard = create_board()
        heuristic = find_heu(nextboard)
    else:
        heuristic = best_heu
    steps+=1
    return nextboard

# First-choice hill climbing implements stochastic hill climbing by generating successors randomly until one is generated that is better than the current state.
# chooses the first better state from randomly generated neighbors.
def hillclimb_fc(currboard):
    global steps_fc
    global heuristic_fc
    nextboard, tempboard = [], []
    curr_heu = find_heu(currboard)
    best_heu = curr_heu # set as best heu now
    for i in range(len(currboard)): # copy and paste currboard to 2 others
        nextboard.append(currboard[i])
        tempboard.append(currboard[i])
    aaa = False
    for i in range(len(currboard)):
        if i>0:
            tempboard[i-1] = queen(currboard[i-1].get_row(),currboard[i-1].get_col())
        tempboard[i] = queen(0,tempboard[i].get_col())
        for j in range(len(currboard)):
            temp_heu = find_heu(tempboard)
            if(temp_heu<best_heu):
                best_heu = temp_heu
                for k in range(len(currboard)):
                    nextboard[k] = queen(tempboard[k].get_row(),tempboard[k].get_col())
                aaa = True
                break # break if we find a better value, no more moves
            if(tempboard[i].get_row()!=(len(currboard)-1)):
                tempboard[i].move()
        if aaa:
            break # same, if we found a better value break, this is only used for bread nested loop
    # check if we have a better board
    if(best_heu == curr_heu):
        # no progress, restart, ++counters
        steps_fc = 0
        nextboard = create_board()
        heuristic_fc = find_heu(nextboard)
    else:
        heuristic_fc = best_heu
    steps_fc+=1
    return nextboard

def schedule(t): 
    if t == 0:
        t = 0.0001 #avoid returning +infinity
    return (-1000)*log(t/100)
# set temperature, T, used shcedule(t), where t is the time, to change the value of T
def sim_anneal(currboard):
    global steps_sa
    global heuristic_sa
    global t_sa
    global big_t
    nextboard, tempboard = [],[]
    curr_heu = find_heu(currboard)
    best_heu = curr_heu
    for i in range(len(currboard)):
        nextboard.append(currboard[i])
        tempboard.append(currboard[i])
    big_t = schedule(t_sa) # calculate T(TEMPERATURE) t++, T--
    aaa = False
    if big_t!=0:
        for i in range(len(currboard)):
            if i>0:
                tempboard[i-1] = queen(currboard[i-1].get_row(),currboard[i-1].get_col())
            tempboard[i] = queen(0,tempboard[i].get_col())
            for j in range(len(currboard)):
                temp_heu = find_heu(tempboard)
                if(temp_heu<best_heu):# if there is a better move, take
                    best_heu = temp_heu
                    for k in range(len(currboard)):
                        nextboard[k] = queen(tempboard[k].get_row(),tempboard[k].get_col())
                    aaa = True
                    break
                else: #check if we take this bad move, as T++, prob--
                    delta_e =  best_heu - temp_heu #deltaE need to be negative
                    if(random.random()>exp(delta_e/big_t)): #take this bad move
                        best_heu = temp_heu
                        for k in range(len(currboard)):
                            nextboard[k] = queen(tempboard[k].get_row(),tempboard[k].get_col())
                        aaa = True
                        break
                if(tempboard[i].get_row()!=(len(currboard)-1)):
                    tempboard[i].move()
                if aaa:
                    break
        heuristic_sa = find_heu(nextboard)
        t_sa+=1 # increment the time
    # when big_t == 0
    else:
        # no progress, restart, ++counters
        steps_sa = 0
        t_sa = 0 #reset time
        nextboard = create_board()
        heuristic_sa = find_heu(nextboard)
    steps_sa+=1
    return nextboard

######MAIN########
sahc = []
fchc = []
sa = []
for hho in range(100):
    # create board*3
    get_board = create_board()
    get_board1 = [None]*len(get_board)
    get_board2 = [None]*len(get_board)
    for i in range(len(get_board)):
        get_board1[i] = get_board[i]
        get_board2[i] = get_board[i]
    #sa hill climb
    current_heu = find_heu(get_board)
    while(current_heu!=0):
        get_board = hillclimb_sa(get_board)
        current_heu = heuristic
    #print_state(get_board)
    #print(steps)
    sahc.append(int(steps))
    #fc hill climb
    current_heu1 = find_heu(get_board1)
    while(current_heu1!=0):
        get_board1 = hillclimb_fc(get_board1)
        current_heu1 = heuristic_fc
    #print_state(get_board1)
    #print(steps_fc)
    fchc.append(int(steps_fc))
    #sa
    current_heu2 = find_heu(get_board2)
    while(current_heu2!=0):
        get_board2 = sim_anneal(get_board2)
        current_heu2 = heuristic_sa
    #print_state(get_board1)
    #print(steps_sa)
    sa.append(int(steps_sa))
print(mean(sahc))
print(mean(fchc))
print(mean(sa))